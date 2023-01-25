
import random
from collections import defaultdict
import torch.nn as nn
import torch
from torch.autograd import Variable
from torch.nn import init
from Model.Aggregators import MeanAggregator
from Model.Encoders import Encoder
import numpy as np
from Model.My_Loss import My_Loss
from Model.sec_Model import sec_Model
from Model.thi_model import thi_Model
from Model.fir_Model import fir_Model
from Model.fou_Model import fou_Model


class Model(nn.Module):
    def __init__(self, enc, fir, sec, thi, fou):
        super(Model, self).__init__()
        self.fir = fir
        self.sec = sec
        self.thi = thi
        self.fou = fou
        self.enc = enc
        self.xent = nn.CrossEntropyLoss()
        self.weight = nn.Parameter(torch.FloatTensor(4, enc.embed_dim))
        init.xavier_uniform(self.weight)

    def forward(self, nodes):
        embeds = self.enc(nodes)
        scores = self.weight.mm(embeds)
        scores = torch.softmax(scores, dim=0)
        # (256*4)
        result = []
        _max = scores.data.numpy().argmax(axis=1)
        for id, score in enumerate(scores):
            if _max[id] == 0:
                result.append(self.fir(score))
            elif _max[id] == 1:
                result.append(self.sec(score))
            elif _max[id] == 2:
                result.append(self.thi(score))
            elif _max[id] == 3:
                result.append(self.fou(score))
        return torch.cat(scores, Variable(torch.FloatTensor(result), requires_grad=False))


def f(a):
    return float(a)


def getinfo():
    num_nodes = 3344
    num_feats = 3472
    feat_data = np.zeros((num_nodes, num_feats))
    labels = np.empty((num_nodes, 1), dtype=np.int64)
    node_map = {}
    label_map = {}
    with open("feature_labels.txt") as fp:
        for i, line in enumerate(fp):
            info = line.strip().split()
            feat_data[i, :] = list(map(f, info[0:-1]))
            node_map[info[0]] = i
            if not info[-1] in label_map:
                label_map[info[-1]] = len(label_map)
            labels[i] = label_map[info[-1]]
    adj_lists = defaultdict(set)
    print(adj_lists)
    with open("adjlist.txt") as fp:
        for i, line in enumerate(fp):
            info = line.strip().split()
            paper1 = node_map[info[0]]
            paper2 = node_map[info[1]]
            adj_lists[paper1].add(paper2)
            adj_lists[paper2].add(paper1)
    return feat_data, labels, adj_lists


def train():

    np.random.seed(1)
    random.seed(1)
    num_nodes = 3344
    feat_data, labels, adj_lists = getinfo()
    features = nn.Embedding(3344, 3472)
    features.weight = nn.Parameter(torch.FloatTensor(feat_data), requires_grad=False)
    agg1 = MeanAggregator(features, cuda=True)
    enc1 = Encoder(features, 1433, 128, adj_lists, agg1, gcn=True, cuda=False)
    agg2 = MeanAggregator(lambda nodes: enc1(nodes).t(), cuda=False)
    enc2 = Encoder(lambda nodes: enc1(nodes).t(), enc1.embed_dim, 128, adj_lists, agg2,
                   base_model=enc1, gcn=True, cuda=False)
    enc1.num_samples = 5
    enc2.num_samples = 5
    optimizer = torch.optim.Adam(enc2.parameters(), lr=0.01)
    model = Model(enc2, fir_Model(), sec_Model(), thi_Model(), fou_Model())
    rand_indices = np.random.permutation(num_nodes)
    for batch in range(100):
        optimizer.zero_grad()
        batch_nodes = rand_indices[:256]
        pre_batch_nodes = model(batch_nodes)
        loss = My_Loss(pre_batch_nodes, Variable(torch.LongTensor(labels[np.array(batch_nodes)])))
        loss.backward()
        optimizer.step()
