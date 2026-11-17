# -*- coding: utf-8 -*-
"""
This file provides help methods for the note API
Created on Sat Feb  8 21:46:15 2025
@author: Zeyu Pan
version 2
"""
#记录日志
import myLogging

#引入响应和请求
from models import NoteResponse

# 获取默认的日志记录器
logging = myLogging.default_logger

from entities import RawRecognition,Subtitle,Link,Point

# 大模型部分依赖库
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

import tempfile
import os

def formatText(record_text: list):
    try:
        # 创建一个临时文件
        with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as temp_file:
            # 格式化并写入文件
            for record in record_text:
                start = record.start
                text = record.text.replace('\n', '')  # 去除文本中的换行符

                # 数学计算将秒转换为 'HH:MM:SS' 格式
                hours = start // 3600
                minutes = (start % 3600) // 60
                seconds = start % 60
                formatted_time = f"{hours:02}:{minutes:02}:{seconds:02}"  # 格式化为两位数
                temp_file.write(f"{formatted_time}\t{text}\n")

            temp_file_path = temp_file.name  # 获取临时文件路径

        # 读取临时文件内容
        with open(temp_file_path, 'r', encoding='utf-8') as f:
            record_text_l = f.readlines()

        # 删除临时文件
        os.remove(temp_file_path)

        # 处理每一行，并将其转换为所需的元组格式
        result = []
        for line in record_text_l:
            line = line.replace('\n', '')  # 去掉换行符
            parts = line.split('\t')  # 按照 Tab 分隔时间和文本
            if len(parts) == 2:
                result.append((parts[0], parts[1]))  # 添加到结果列表中

        return result

    except Exception as e:
        logging.error(f"处理文本时发生错误: {e}")
        raise e

"""
生成笔记
"""
def getNote(model_name:str,url:str,record_text):

    try:
        logging.info("开始生成笔记...")

        # 初始化 OpenAI 客户端（在这里使用的是 Zhipu AI）
        client = OpenAI(
             # Zhipu AI API key
             api_key=os.environ["ZHIPU_API_KEY"],
             base_url="https://open.bigmodel.cn/api/paas/v4",  # Ensure URL is correct
        )

        # 先格式化 record_text 变成元组列表
        formatted_text = formatText(record_text)

        # 构建一个消息模板，定义聊天的格式
        prompt=(
               f"请根据以下内容生成一个简洁的主题和摘要（请用Markdown格式）:\n\n{formatted_text}\n\n"
               "用户以元组列表形式输入一堂课的录音文本，元组的第1项为这句话的时间，第2项为这句话的文本，你被要求先优化识别错误的内容，然后根据处理后的文本，以文本形式输出一个课堂笔记，内容是：1.课程主题。2.课程摘要。3.详细的知识点笔记(每个知识点包含名称、重要程度（整数1-5，5代表最重要）、然后由子要点阐述解释或例子（子要点如定义、应用、证明等），每个子要点的标题前要有这个概念在录音文本中第一次被提到的时间（即这个子要点的开始时间），每个要点后附这个子要点对应的全部文本，即不要有任何改动的原文本））。4.几个关键词及对应的参考网站。"
               "示例如下："
               "详细的知识点笔记：1. 二阶行列式的定义与计算 (重要程度：5)：（00:01）二阶行列式的定义：一个方程组的系数矩阵的主对角线元素之积，即对角线元素的乘积；（03：52）二阶行列式的计算方法：利用二阶行列式的定义，将方程组的系数矩阵化为上三角矩阵，再利用对角线元素的乘积求和。2. 三阶行列式的定义与计算 (重要程度：5)：（05：44）三阶行列式的定义：一个方程组的系数矩阵的主对角线元素之积，即对角线元素的乘积；（08：36）三阶行列式的计算方法：利用代数余子式的性质，利用三阶行列式的定义，将方程组的系数矩阵化为上三角矩阵，再利用对角线元素的乘积求和。3.特殊行列式（重要程度：3）：（15:03)上三角行列式：是主对角线以下的元素均为零的行列式，其值等于主对角线元素的乘积;（16:27)下三角行列式：主对角线以上的元素均为零的行列式，其值等于主对角线元素的乘积。关键词及参考网站：行列式 - 维基百科：https://zh.wikipedia.org/wiki/%E8%A1%8C%E5%88%97%E5%BC%8F；线性代数 - 可汗学院：https://zh.khanacademy.org/math/linear-algebra"
        )


        # 向 AI 模型发送请求并获取回复，指定使用的模型（glm-4）
        completion = client.chat.completions.create(
            model="glm-4-air-0111",  # 在这里指定模型
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt},
            ],
        )

        note_text=completion.choices[0].message.content

        logging.info(f"笔记生成成功, 模型输出token数：{len(note_text)}，内容如下：\n{note_text}")
        return note_text
    except Exception as e:
        logging.error(f"生成笔记失败: {e}")
        raise e

"""
检查模型
"""
def checkModel(note_text):
    model_name='glm-4-air-0111'

    #主要是根据人文类定的，数学类的话由于有很多公式token会虚多，很容易就切换到long了，效果下降，之后再想想怎么办
    if len(note_text) > 1000:
        model_name='glm-4-long'

    return model_name

# 生成响应
def generateResponse(model_name: str, url: str, note_text: str) -> NoteResponse:
    """
    将课堂笔记转换为符合 NoteResponse 结构的 JSON 数据。

    参数：
    - model_name (str): ChatOpenAI 使用的模型名称。
    - url (str): OpenAI API 的基础 URL。
    - note_text (str): 课堂笔记的文本内容。

    返回：
    - dict: 符合 NoteResponse 结构的字典，包含课程主题、知识点、摘要、关键词等信息。
    """

    try:
        logging.info("开始生成 JSON 响应...")

        # 初始化 OpenAI 客户端（在这里使用的是 Zhipu AI）
        client = OpenAI(
             # Zhipu AI API key
             api_key=os.environ["ZHIPU_API_KEY"],
             base_url="https://open.bigmodel.cn/api/paas/v4",  # Ensure URL is correct
        )

        # 构建一个消息模板，定义聊天的格式
        prompt=(
               f"接下来把用户输入的课堂笔记进行拆分并输出一个json代码，不分行，除了代码什么都不要:\n\n{note_text}\n\n"
               "包含：1.课程主题。2.详细的知识点笔记(知识点是由字典组成的列表，每个知识点包含名称、重要程度（整数1-5，5代表最重要）、子要点（每一个知识点要有对应的解释或例子，由子要点组织，即子要点是知识点内容的具体阐述、该知识点开始时间以及这个知识点对应的全部文本，子要点的名字要是一个简洁的词语或短语）；子要点也是由字典组成的列表，键和值用markdown格式，键用一级标题，值可以适当加粗或斜体等）、以字典列表组织的每个子要点对应的开始时间。3.关键词及对应的参考网站。4.课程摘要。示例如下："
               "{{'theme'：'二阶和三阶行列式的定义及其计算方法', 'points'：[{{'name：'#二阶行列式',‘importance':4, 'subtitles'：[{{'subtitle':'#定义','md':'**二阶行列式**由两个正项相乘减去两个数负项相乘得到。','raw_recognition':[{{'start':00:00,'end':01:58}}]}},"
               "{{'subtitle':'#应用','md':'解二元一次方程。',raw_recognition':[{{'start':01:58,'end':03:00]}}]}}]}}],"
               "[{{'name：'#特殊行列式',‘importance':2, 'subtitles'：[{{'subtitle':'#上三角行列式','md':{{'所有**主对角以下**的元素**为零**的行列式。'}},raw_recognition':[{{'start':03:00,'end':04:00}}]}},'"
               "{{'subtitle':'#下三角行列式','md':'所有主对角以上的元素**为零**的行列式'，raw_recognition':[{{'start':04:00,'end':05:00]}}]}}]}}],"
             "‘links’:[{{‘name’：‘MIT OpenCourseWare’，‘href’：‘https://ocw.mit.edu/courses/mathematics/18-06-linear-algebra-spring-2010’}}, {{‘name’：‘Wolfram MathWorld’，‘href’：‘hhttps://mathworld.wolfram.com/Determinant.html’}}],"
               "'summary'：'二阶行列式由两个正项相乘减去两个数负项相乘得到。三阶行列式由九个元素组成，计算时需要考虑三个正项和三个负项。正项是沿着主对角线、副对角线以及从左上角到右下角的对角线上的元素乘积。负项是沿着主对角线、副对角线以及从右上角到左下角的对角线上的元素乘积。三阶行列式的计算使用对角线法则，将三阶行列式展开为三个正项和三个负项的和。特殊行列式包括上三角行列式、下三角行列式和对角行列式。'}})"
        )


        # 向 AI 模型发送请求并获取回复，指定使用的模型（glm-4）
        completion = client.chat.completions.create(
            model="glm-4-air-0111",  # 在这里指定模型
            max_tokens=4095,
            messages=[
                {"role": "user", "content": prompt},
            ],
        )

        logging.info(completion.choices[0].message.content)
        return convert_json_to_note_response(completion.choices[0].message.content)
        #return completion.choices[0].message.content["points"]

    except Exception as e:
        logging.error(f"生成 JSON 失败: {e}")
        raise e

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
                RawRecognition(start=convert_time_to_seconds(rec["start"]), text=rec["text"])
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

# 转换时间格式为秒数
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
获取响应
"""
def getResponse(note:list[RawRecognition]):

    try:
        # 设置模型及网址
        model_name='glm-4-air-0111'
        base_url="https://open.bigmodel.cn/api/paas/v4/"

        #生成笔记
        note_text=getNote(model_name,base_url,note)

        #检查模型
        model_name=checkModel(note_text)

        #生成响应
        return generateResponse(model_name,base_url,note_text)
    except Exception as e:
        raise e
