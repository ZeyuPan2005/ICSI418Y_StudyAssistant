# -*- coding: utf-8 -*-
"""
This project has set up a server for communication
between the front-end and back-end
Created on Tue Jan 21 00:14:02 2025
@author: Zeyu Pan
version 1
"""
from Test import test_note_endpoint,test_record_endpoint,test_network_endpoint,start_server

from threading import Thread

# 主程序
if __name__ == "__main__":
    # 使用线程启动服务
    server_thread = Thread(target=start_server, daemon=True)
    server_thread.start()

    # 测试 /record 接口
    recordResponse=test_record_endpoint()

    # 测试 /note 接口
    test_note_endpoint(recordResponse)

    # 测试 /network 接口
    #test_network_endpoint()
