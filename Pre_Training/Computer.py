# -*- coding:utf-8 -*-
# @FileName  :Computer.py
# 主要是用于计算预测值返回0/1
import torch


def compute(x, T):
    """
    输入特征，输出预测千米数
    计算预预测值，并返回是0/1
    """
    model = torch.load()
    with torch.no_grad():
        pred = model(x).numpy()
        if pred > T:
            return 1
        else:
            return 0
