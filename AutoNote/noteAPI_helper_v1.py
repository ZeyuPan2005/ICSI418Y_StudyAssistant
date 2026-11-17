# -*- coding: utf-8 -*-
"""
This file provides help methods for the note API
Created on Thu Feb  6 22:05:58 2025
@author: Zeyu Pan
version 1
"""
from langchain_core.messages import SystemMessage

import locale
locale.getpreferredencoding = lambda: "UTF-8"

#记录日志
import myLogging

#引入响应和请求
from models import NoteResponse

# 获取默认的日志记录器
logging = myLogging.default_logger

from entities import RawRecognition

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from datetime import timedelta

import tempfile
import os

"""
将数据编码方式转换为utf-8
"""
def write_and_read_temp_file(formatted_text: list) -> list:
    try:
        # 将列表格式化为字符串（保持元组的格式）
        formatted_text_str = repr(formatted_text)

        # 创建一个临时文件，使用 UTF-8 编码写入
        with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as temp_file:
            temp_file.write(formatted_text_str)  # 写入文件
            temp_file_path = temp_file.name  # 获取临时文件路径

        # 读取文件内容
        with open(temp_file_path, 'r', encoding='utf-8') as temp_file:
            content = temp_file.read()

        # 删除临时文件
        os.remove(temp_file_path)

        # 将文件内容（字符串）转换回原始的列表结构
        formatted_text_from_file = eval(content)

        return formatted_text_from_file

    except Exception as e:
        logging.error(f"操作临时文件时发生错误: {e}")
        raise e


# 将秒数转换为 'HH:MM:SS' 格式
def seconds_to_time_format(seconds: int) -> str:
    return str(timedelta(seconds=seconds))

"""
将 list[RawRecognition] 转换为 list[str]。
"""
def format_record_text(record_text: list[RawRecognition]) -> list[str]:
    # 从 RawRecognition 对象中提取出 start 时间戳和 text 文本，并返回字符串格式
    return [f"({r.start}, '{r.text}')" for r in record_text]

"""
格式化文本
"""
def formatText(record_text: list[RawRecognition]) -> list[tuple]:
    # 将 record_text 格式化为字符串列表
    record_text_l = format_record_text(record_text)

    result = []
    for _ in record_text_l:
        # 去除文本中的换行符
        _ = _.replace('\n', '')

        # 使用 split 将字符串拆解为时间戳和文本两部分
        parts = _.strip('()').split(", ")
        timestamp = int(parts[0])  # 转换时间戳为整数
        text = parts[1].strip("'")  # 去除文本的单引号

        # 将时间戳转换为 'HH:MM:SS' 格式
        formatted_time = seconds_to_time_format(timestamp)

        # 将时间戳和文本组合为元组并添加到结果列表
        result.append((formatted_time, text))

    return result

"""
生成笔记
"""
def getNote(model_name:str,url:str,record_text):

    try:
        logging.info("开始生成笔记...")

        # 初始化ChatOpenAI模型，指定模型名称、API基础地址和最大token数。
        model_str = ChatOpenAI(
            model=model_name,
            openai_api_base=url,
            api_key=os.environ["ZHIPU_API_KEY"],
            max_tokens=2000, # 最大token数，限制输出的长度
        )
        logging.info(f"ChatOpenAI 模型 {model_name} 初始化成功")

        # 先格式化 record_text 变成元组列表
        formatted_text = formatText(record_text)

        # 构建一个消息模板，定义聊天的格式
        prompt_template_str = ChatPromptTemplate.from_messages(
            [   #SystemMessage(content="hello"),
                ('system','用户以元组列表形式输入一堂课的录音文本，元组的第1项为这句话的时间，第2项为这句话的文本，你被要求先优化识别错误的内容，然后根据处理后的文本，以文本形式输出一个课堂笔记，内容是：1.课程主题。2.课程摘要。3.详细的知识点笔记(每个知识点包含名称、重要程度（整数1-5，5代表最重要）、然后由子要点阐述解释或例子（子要点如定义、应用、证明等），每个子要点的标题前要有这个概念在录音文本中第一次被提到的时间（即这个子要点的开始时间），每个要点后附这个子要点对应的全部文本，即不要有任何改动的原文本））。4.几个关键词及对应的参考网站。'
                # ('system','用户以输入一堂课的录音文本，你被要求先优化识别错误的内容，然后根据处理后的文本，以文本形式输出一个课堂笔记，内容是：1.课程主题。2.课程摘要。3.详细的知识点笔记(每个知识点包含名称、重要程度（整数1-5，5代表最重要）、然后由子要点阐述详细解释或例子（子要点如定义、应用、证明等），然后瞎编一下这个子要点开始的时间（每个子要点一定要有时间！）以及这个子要点对应的全部文本，即不要有任何改动的原文本），4.几个关键词及对应的参考网站'
                          '示例如下：主题：二阶行列式和三阶行列式的定义及其计算；摘要：本节课首先通过一个二元一次方程组的例子，引出了二阶行列式的定义和计算方法。接着，介绍了三阶行列式的定义和计算方法，包括对角线法则。最后，讨论了特殊的行列式。'
                          '详细的知识点笔记：1. 二阶行列式的定义与计算 (重要程度：5)：（00:01）二阶行列式的定义：一个方程组的系数矩阵的主对角线元素之积，即对角线元素的乘积；（03：52）二阶行列式的计算方法：利用二阶行列式的定义，将方程组的系数矩阵化为上三角矩阵，再利用对角线元素的乘积求和。2. 三阶行列式的定义与计算 (重要程度：5)：（05：44）三阶行列式的定义：一个方程组的系数矩阵的主对角线元素之积，即对角线元素的乘积；（08：36）三阶行列式的计算方法：利用代数余子式的性质，利用三阶行列式的定义，将方程组的系数矩阵化为上三角矩阵，再利用对角线元素的乘积求和。3.特殊行列式（重要程度：3）：（15:03)上三角行列式：是主对角线以下的元素均为零的行列式，其值等于主对角线元素的乘积;（16:27)下三角行列式：主对角线以上的元素均为零的行列式，其值等于主对角线元素的乘积。关键词及参考网站：行列式 - 维基百科：https://zh.wikipedia.org/wiki/%E8%A1%8C%E5%88%97%E5%BC%8F；线性代数 - 可汗学院：https://zh.khanacademy.org/math/linear-algebra'
                          ),
                # 用户消息（此处用户输入的内容就是一堂课的录音文本，这将被模型用来生成课堂笔记）
                ('human','{formatted_text}')
            ]
        )
        logging.info("消息模板构建成功")


        # 将消息模板与模型连接，创建一个处理流程链（chain）
        chain_str = prompt_template_str|model_str

        #logging.info(formatted_text[:5])

        formatted_text=write_and_read_temp_file(formatted_text)

        logging.info(0)

        note_text = chain_str.invoke(input={'formatted_text':formatted_text}).content

        logging.info(1)

        if isinstance(note_text, bytes):
            note_text = note_text.decode('utf-8', errors="ignore")  # 解码成 UTF-8

        logging.info(2)

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
def generateResponse(model_name: str, url: str, note_text: str) -> dict:
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

        # 初始化 ChatOpenAI 模型
        model_json = ChatOpenAI(
            model=model_name,
            openai_api_base=url,
            api_key=os.environ["ZHIPU_API_KEY"],
            max_tokens=4095,
        )
        logging.info(f"ChatOpenAI 模型 {model_name} 初始化成功")

        # 定义系统提示，描述 JSON 结构
        model_json_message = (
            "请将用户输入的课堂笔记转换为 JSON 格式，不要换行，仅输出 JSON 代码，格式如下：\n"
            "{\n"
            '  "points": [\n'
            '    {\n'
            '      "name": "知识点名称",\n'
            '      "importance": 5,\n'
            '      "subtitles": [\n'
            '        {\n'
            '          "subtitle": "定义",\n'
            '          "md": "**二阶行列式**由两个正项相乘减去两个负项相乘得到。",\n'
            '          "raw_recognition": [{"start": 0, "end": 118, "text": "原始文本"}]\n'
            '        }\n'
            '      ],\n'
            '      "links": [\n'
            '        {"name": "MIT OpenCourseWare", "href": "https://ocw.mit.edu/courses/mathematics/18-06-linear-algebra-spring-2010"},\n'
            '        {"name": "Wolfram MathWorld", "href": "https://mathworld.wolfram.com/Determinant.html"}\n'
            '      ],\n'
            '      "summary": "课程摘要"\n'
            '    }\n'
            '  ]\n'
            '}'
        )

        # 构建 Prompt 模板
        prompt_template_json = ChatPromptTemplate.from_messages(
            [
                ('system', model_json_message),
                ('human', note_text)  # 课堂笔记内容
            ]
        )
        logging.info("JSON 结构化提示词构建成功")

        # 连接 Prompt 和 ChatOpenAI
        chain_json = prompt_template_json | model_json

        # 执行推理，生成 JSON 结果
        json_text = chain_json.invoke({}).content
        logging.info("模型推理完成，成功生成 JSON")

        # 清理 JSON 代码块
        json_text = json_text.strip().replace('```json', '').replace('```', '')

        # 解析为 Python 字典
        json_dict = eval(json_text)  # 这里用 `eval`，但建议用 `json.loads` 如果格式确保正确

        # 验证是否符合 NoteResponse 结构
        note_response = NoteResponse(**json_dict)

        logging.info("最终 NoteResponse 结构校验通过")
        return note_response.dict()

    except Exception as e:
        logging.error(f"生成 JSON 失败: {e}")
        raise e

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
