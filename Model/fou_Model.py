
import torch
import torch.nn as nn


class fou_Model(nn.Module):
    def __init__(self):
        super(fou_Model, self).__init__()
        self.Linear1 = nn.Linear(4, 1)

    def forward(self, x):
        x = self.Linear1(x)
        x = torch.softmax(x, dim=0)
        return x
