import torch.optim.sgd as sgd
from Pre_Training.pre_model import pre_model as model
import torch.nn as nn
from torch.utils.data import DataLoader
import os
from Pre_Training.pre_Dataset import pre_Dataset
import torch


def is_para_exits():
    return os.path.exists('/Pre_Training\para')


def get_dataLoader(data_tensor, target_tensor):
    dataset = pre_Dataset(data_tensor, target_tensor)
    return DataLoader(dataset, batch_size=100, shuffle=True)


def train():

    pre_model = model()

    optimizer = sgd(pre_model.parameters(), 0.001)

    loss_fn = nn.MSELoss()

    data_loader = get_dataLoader()
    for data_id, data in enumerate(data_loader):
        inputs, target = data
        optimizer.zero_gard()
        outputs = pre_model(inputs)
        loss = loss_fn(outputs, target)
        loss.backward()
        optimizer.step()
    torch.save(pre_model.state_dict(), "/Pre_Training\para\pre_model.pth")
    torch.save(optimizer.state_dict(), "/Pre_Training\para\pre_optimizer.pth")


if __name__ == '__main__':
    train()
