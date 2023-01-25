
import torch
import torch.nn as nn


class fir_Model(nn.Module):
    def __init__(self):
        super(fir_Model, self).__init__()
        self.Linear1 = nn.Linear(4, 1)

    def forward(self, x):
        x = self.Linear1(x)
        x = torch.softmax(x, dim=0)
        return x
