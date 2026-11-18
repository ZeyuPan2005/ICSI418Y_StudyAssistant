# -*- coding: utf-8 -*-
"""
This file is used to record logs
Created on Sun Jan 26 16:33:57 2025
@author: Zeyu Pan
version 2
"""
#记录日志
import logging

# 初始化日志配置的函数
def setup_logger(name, log_file, level=logging.INFO):
    # 创建logger对象
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.hasHandlers():
        # 创建文件处理器
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)

        # 创建控制台处理器
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(level)

        # 创建日志格式
        """
        #定义日志的输出格式：
        #%(asctime)s：日志记录的时间戳。
        #%(levelname)s：日志级别名称（如 INFO, ERROR）。
        #%(message)s：日志内容。
        """
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        #将日志写入到指定文件中。
        file_handler.setFormatter(formatter)

        #将日志输出到控制台。
        stream_handler.setFormatter(formatter)

        # 将处理器添加到logger
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger

"""
# 如果需要在其他模块中使用，可以直接导入 default_logger
"""

# 创建一个默认的日志记录器 调试阶段选用下行代码
default_logger = setup_logger('default_logger', 'api.log')


# 前端测试时选用下行代码
import os
# 获取用户的 HOME 环境变量（针对 Windows 系统，用户目录为 %USERPROFILE%）
if os.name == 'nt':  # 如果是 Windows 系统
    home_dir = os.getenv("USERPROFILE")  # 获取 Windows 用户目录
    log_dir = os.path.join(home_dir, "AppData", "Local", "com.auto-notes.app", "logs")
elif os.name == 'posix':  # 如果是 macOS 或 Linux 系统
    home_dir = os.getenv("HOME")  # 获取 macOS 用户目录
    log_dir = os.path.join(home_dir, "Library", "Logs", "com.auto-notes.app")
else:
    raise EnvironmentError("Unsupported OS")

# 确保日志目录存在
try:
    os.makedirs(log_dir, exist_ok=True)
except PermissionError:
    raise RuntimeError(f"无法创建日志目录: {log_dir}, 请检查权限")

#default_logger = setup_logger('default_logger', log_dir)
