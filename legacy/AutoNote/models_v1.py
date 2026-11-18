# -*- coding: utf-8 -*-
"""
This file defines responses and requests
Created on Sun Jan 26 16:15:00 2025
@author: Zeyu Pan
version 1
"""
#BaseModel：用于定义数据模型，强类型校验输入输出数据。
from pydantic import BaseModel
from entities import RawRecognition, Point, Link, Subtitle
# 定义请求和响应模型

class RecordResponse(BaseModel):
    id: int #id：录音唯一标识。
    duration: int #duration：录音时长（秒）。
    topic: str #topic：录音主题。
    abstract: str #abstract：录音摘要。
    raw_recognition: list[RawRecognition] #raw_recognition：识别的原始内容（一个 RawRecognition 列表）。

class NoteRequest(BaseModel):
    topic: str #topic：笔记主题。
    abstract: str #abstract：笔记摘要。
    raw_recognition: list[RawRecognition] #raw_recognition：识别的原始内容（一个 RawRecognition 列表）。


class NoteResponse(BaseModel):
    points: list[Point] #points：笔记要点列表（一个 Point 列表）。
