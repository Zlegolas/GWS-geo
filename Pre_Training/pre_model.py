import torch.nn as nn


class pre_model(nn.Module):
    def __init__(self):
        super(pre_model, self).__init__()
        self.liear1 = nn.Linear(4, 2, bias=True)
        self.liear2 = nn.Linear(2, 1, bias=True)

    def forward(self, x):
        out = self.liear1(x)
        out = self.liear2(out)
        return out