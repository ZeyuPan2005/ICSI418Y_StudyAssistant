# -*- coding: utf-8 -*-
"""
This project has set up a server for communication
between the front-end and back-end
Created on Tue Jan 21 00:14:02 2025
@author: Zeyu Pan
version 1
"""
from pydantic import BaseModel, Field

"""
#功能:表示一段识别内容的结构。
#用途：
#可用于表示录音中某一段的文字内容及其时间范围。
#适合记录转录结果中的片段。
"""
class RawRecognition(BaseModel):
    start: int #start：起始时间点（秒）。
    end: int|None=None #end：结束时间点（秒）。
    text: str #text：识别的文本内容。

"""
#功能:表示与笔记相关的链接信息。
#用途：
#提供与笔记内容相关的参考资料。
#链接信息通常用于丰富笔记内容的上下文。
"""
class Link(BaseModel):
    name: str #name：链接的名称或描述。
    href: str #href：链接地址（URL）。

"""
#功能:表示笔记中的一个子标题及其相关内容。
#用途：
#细分笔记的内容，每个子标题下包含与之相关的解释和识别内容。
"""
class Subtitle(BaseModel):
    subtitle: str #subtitle：子标题的文本。
    md: str #md：与子标题相关的 Markdown 格式文本（比如说明或示例）。
    raw_recognition: list[RawRecognition] #raw_recognition：一个 RawRecognition 列表，用于表示与该子标题关联的原始识别片段。

"""
#功能
#表示笔记中的一个核心要点。
#用途：
#代表一个笔记的核心知识点，包含详细的说明、相关链接和重要性。
#代码整体逻辑
#面向 API 的数据结构：
#每个类通过继承 BaseModel 提供了数据类型校验和序列化能力，确保输入和输出数据结构的正确性。
#层次化组织笔记内容：
#顶层是 Point 类，表示笔记的核心要点。
#每个 Point 由多个 Subtitle（子标题）和 Link（参考链接）组成。
#每个 Subtitle 又关联多个 RawRecognition，表示与子标题相关的原始识别内容。
#字段验证：
#例如 importance 字段使用了 Field(ge=1, le=5)，确保其值在 1 到 5 的范围内。
#Markdown 支持：
#Subtitle 中的 md 字段允许使用 Markdown 格式内容，方便生成更加丰富的展示页面。
"""
class Point(BaseModel):
    name: str #name：要点的名称。
    importance: int = Field(ge=1, le=5) #importance：要点的重要程度，范围为 1-5（通过 Field 校验）。
    subtitles: list[Subtitle] #subtitles：与该要点相关的子标题列表（类型为 Subtitle）。
    links: list[Link] #links：与该要点相关的链接列表（类型为 Link）。
    summary: str #summary：该要点的简要总结。

"""
#附：整体数据模型的关系图
#Point
#├── name: str
#├── importance: int
#├── subtitles: list[Subtitle]
#│   ├── subtitle: str
#│   ├── md: str
#│   └── raw_recognition: list[RawRecognition]
#│       ├── start: int
#│       ├── end: int
#│       └── text: str
#├── links: list[Link]
#│   ├── name: str
#│   └── href: str
#└── summary: str
"""
