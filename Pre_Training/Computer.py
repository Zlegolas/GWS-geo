# -*- coding:utf-8 -*-

import torch


def compute(x, T):

    model = torch.load()
    with torch.no_grad():
        pred = model(x).numpy()
        if pred > T:
            return 1
        else:
            return 0
