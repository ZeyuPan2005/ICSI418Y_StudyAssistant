# -*- coding: utf-8 -*-
"""
This file provides help methods for the network API
Created on Thu Feb  6 22:06:19 2025
@author: Zeyu Pan
version 1
"""
#记录日志
import myLogging

#引入响应和请求
from models import NetworkResponse

from entities import Lecture,NodeCategory,Node,NoteRoute,NodeLink

# 获取默认的日志记录器
logging = myLogging.default_logger

"""
获取响应
"""
def getResponse(lectureList:list[Lecture]):
    """

    Parameters
    ----------
    lectureList : list[Lecture]
        DESCRIPTION. 一个Lecture列表，包含每一堂课

    Returns
    -------
    networkResponse : NetworkResponse
        DESCRIPTION. Network接口的响应 包含 节点 节点链接 节点目录

    """
    try:
        #先获取list[Node]和list[NodeCategory]
        networkResponse1=get_ListNode_ListNodeCategory(lectureList)

        #获取list[NodeLink]
        nodeLinks=get_ListNodeLink()

        #构建networkResponse
        networkResponse=NetworkResponse(nodes=networkResponse1.nodes,links=nodeLinks,categories=networkResponse1.categories)

        return networkResponse
    except Exception as e:
        raise e

"""
根据list[Lecture]生成list[Node],list[NodeCategory]
"""
def get_ListNode_ListNodeCategory(lectureList:list[Lecture]):
    """


    Parameters
    ----------
    lectureList : list[Lecture]
        DESCRIPTION. 一个Lecture列表，包含每一堂课

    Returns
    -------
    TYPE
        DESCRIPTION. Network接口的响应 包含 节点 节点链接(其实为空) 节点目录

    """
    try:
        nodeList=[]
        nodeCategoryList=[]
        categoryNumber=0
        #遍历list[Lecture]
        for lecture in lectureList["lectures"]:
            #构建NodeCategory并添加到列表
            nodeCategoryList.append(NodeCategory(idx=categoryNumber,name=lecture.topic))
            #构建lecture的Node并添加到列表
            nodeList.append(Node(name=lecture.topic,category=categoryNumber,size=5,route=NoteRoute(id=lecture.id)))
            #遍历lecture中的list[Point]
            for point in lecture["points"]:
                #构建Node并添加到列表
                nodeList.append(Node(name=lecture.topic,category=categoryNumber,size=point.importance,route=NoteRoute(id=lecture.id,point=point.name)))
            categoryNumber+=1

        logging.info("list[Node]和list[NodeCategory]生成成功")
        return NetworkResponse(nodes=nodeList,links=[],categories=nodeCategoryList)
    except Exception as e:
        logging.info(f"list[Node]和list[NodeCategory]生成失败:{e}")
        raise e

"""
生成list[NodeLink]
"""
def get_ListNodeLink():
    try:
        linkList=[]
        logging.info("list[Link]生成成功")

        return linkList
    except Exception as e:
        logging.info(f"list[Link]生成失败:{e}")
        raise e
