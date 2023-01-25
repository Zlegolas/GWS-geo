import torch.nn as nn
import numpy as np


class My_Loss(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, output, tagers):
        sum = 0.0
        for i in len(output):
            outputs = output.data.numpy()
            tars = tagers.data.numpy()
            out_index_list = outputs.argmax(outputs, dim=0)
            tars_index_list = tars.argmax(outputs, dim=0)
            sum+=tars_index_list[0]-out_index_list[0]+tars_index_list[1]-out_index_list[1]
        return sum
