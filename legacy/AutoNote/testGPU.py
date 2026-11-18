# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 15:06:26 2025

@author: 13221
"""
import torch
print(torch.__version__)  # 查看当前 PyTorch 版本
if torch.cuda.is_available():
    print(f"CUDA is available. Using GPU: {torch.cuda.get_device_name(0)}")
    print(torch.cuda.current_device())  # 检查当前CUDA设备
    print(torch.cuda.get_device_name(0))  # 获取CUDA设备名称
else:
    print("CUDA is not available. Using CPU.")
