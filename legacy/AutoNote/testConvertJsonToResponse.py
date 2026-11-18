# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 15:44:23 2025

@author: 13221
"""
from entities import RawRecognition,Subtitle,Link,Point
from models import NoteResponse
"""
转换时间格式为秒数
"""
def convert_time_to_seconds(time_str):
    if time_str:
        # 假设输入格式为 "mm:ss" 或 "hh:mm:ss"
        parts = time_str.split(":")
        if len(parts) == 2:  # mm:ss 格式
            minutes, seconds = map(int, parts)
            return minutes * 60 + seconds
        elif len(parts) == 3:  # hh:mm:ss 格式
            hours, minutes, seconds = map(int, parts)
            return hours * 3600 + minutes * 60 + seconds
    return 0  # 默认返回0秒

"""
将JSON格式转化为NoteResponse
"""
def convert_json_to_note_response(json_data):
    points = []

    # 遍历 JSON 中的每个要点
    for point_data in json_data["points"]:
        subtitles = []

        # 遍历每个要点的子标题
        for subtitle_data in point_data["subtitles"]:
            raw_recognition = [
                RawRecognition(start=convert_time_to_seconds(rec["start"]))
                for rec in subtitle_data["raw_recognition"]
            ]
            subtitle = Subtitle(
                subtitle=subtitle_data["subtitle"],
                md=subtitle_data["md"],
                raw_recognition=raw_recognition
            )
            subtitles.append(subtitle)

        links = [
            Link(name=link["name"], href=link["href"]) for link in json_data.get("links", [])
        ]

        point = Point(
            name=point_data["name"],
            importance=point_data["importance"],
            subtitles=subtitles,
            links=links,
            summary=point_data.get("summary", "")
        )

        points.append(point)

    # 创建 NoteResponse 实例
    note_response = NoteResponse(points=points)

    return note_response

data={
  "theme": "排列与逆序数的概念及其应用",
  "points": [
    {
      "name": "#排列的定义与计算",
      "importance": 3,
      "subtitles": [
        {
          "subtitle": "#N级排列",
          "md": "由1到N组成的一个有序数组。",
          "raw_recognition": [{"start": "00:01", "end": "00:45"}]
        },
        {
          "subtitle": "#标准排列",
          "md": "N级排列中，按照自然顺序排列的排列。",
          "raw_recognition": [{"start": "00:45", "end": "00:49"}]
        },
        {
          "subtitle": "#逆序数",
          "md": "一个排列中，逆序的总数。",
          "raw_recognition": [{"start": "00:49", "end": "00:55"}]
        },
        {
          "subtitle": "#奇排列",
          "md": "逆序数为奇数的排列。",
          "raw_recognition": [{"start": "00:55", "end": "00:58"}]
        },
        {
          "subtitle": "#偶排列",
          "md": "逆序数为偶数的排列。",
          "raw_recognition": [{"start": "00:58", "end": "00:89"}]
        },
        {
          "subtitle": "#对换",
          "md": "将排列中的两个数交换位置，其他数保持不变的操作。",
          "raw_recognition": [{"start": "00:89", "end": "00:95"}]
        },
        {
          "subtitle": "#对换性质",
          "md": "每做一次对换，排列的奇偶性就要改变一次。",
          "raw_recognition": [{"start": "00:95", "end": "01:58"}]
        }
      ]
    },
    {
      "name": "#逆序数的计算方法",
      "importance": 4,
      "subtitles": [
        {
          "subtitle": "#逆序数的计算",
          "md": "从排列的第一个数开始，依次计算每个数后面有多少个数比它小，将这些数量相加即为逆序数。",
          "raw_recognition": [{"start": "00:45", "end": "00:54"}]
        },
        {
          "subtitle": "#逆序数的性质",
          "md": "每做一次对换，排列的奇偶性就要改变一次。",
          "raw_recognition": [{"start": "00:54", "end": "00:89"}]
        }
      ]
    },
    {
      "name": "#排列数量的奇偶性",
      "importance": 2,
      "subtitles": [
        {
          "subtitle": "#排列数量的奇偶性",
          "md": "N级排列的总数是N的阶乘，当N大于等于2时，N的阶乘是一个偶数。",
          "raw_recognition": [{"start": "00:89", "end": "00:89"}]
        },
        {
          "subtitle": "#奇排列和偶排列的数量",
          "md": "在所有的N级排列中，奇排列和偶排列各占一半，各为N的阶乘的一半。",
          "raw_recognition": [{"start": "00:89", "end": "01:58"}]
        }
      ]
    }
  ],
  "links": [
    {
      "name": "排列",
      "href": "https://zh.wikipedia.org/wiki/%E6%8E%92%E5%88%97"
    },
    {
      "name": "逆序数",
      "href": "https://zh.wikipedia.org/wiki/%E9%80%86%E5%BA%8F%E6%95%B0"
    },
    {
      "name": "奇排列和偶排列",
      "href": "https://zh.wikipedia.org/wiki/%E5%A5%87%E6%8E%92%E5%88%97%E5%92%8C%E5%81%B6%E6%8E%92%E5%88%97"
    }
  ],
  "summary": "本节课主要讲解了排列的概念，包括N级排列、标准排列、逆序数的定义及其计算方法，并介绍了奇排列和偶排列的概念，以及排列的对换性质和排列数量的奇偶性。"
}
print(convert_json_to_note_response(data))
