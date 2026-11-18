# -*- coding: utf-8 -*-
"""
This project has set up a server for communication
between the front-end and back-end
Created on Tue Jan 21 15:53:05 2025
@author: Zeyu Pan
version 1
"""
import time
#FastAPI 的强项在于异步执行。用 time.sleep 模拟延时，会阻塞主线程。
#替换为 await asyncio.sleep 实现异步延时。
import asyncio

#记录日志
import logging

#FAST API 创建 Web API 框架。
#UploadFile：处理文件上传。
#HTTPException：用于抛出 HTTP 错误。
#Request：表示 HTTP 请求对象。
#JSONResponse：构建自定义的 JSON 格式响应。
from fastapi import FastAPI, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse

#BaseModel：用于定义数据模型，强类型校验输入输出数据。
from pydantic import BaseModel

from models import RawRecognition, Point, Link, Subtitle

import whisper
import tempfile
import os

#创建了一个 FastAPI 应用实例，用于注册 API 路由和处理请求
app = FastAPI()

# 初始化日志配置
logging.basicConfig(
    #设定日志的最低级别 DEBUG-INFO-WARNING-ERROR-CRITICAL
    #低于此级别的将不再被记录
    level=logging.INFO,

    #定义日志的输出格式：
    #%(asctime)s：日志记录的时间戳。
    #%(levelname)s：日志级别名称（如 INFO, ERROR）。
    #%(message)s：日志内容。
    format="%(asctime)s - %(levelname)s - %(message)s",

    handlers=[
        #将日志写入到 server.log 文件中。
        logging.FileHandler("server.log"),
        #将日志输出到控制台。
        logging.StreamHandler()
    ]
)

TEST_MARKDOWN = """
以下为CommonMark Markdown的语法示例：
# 一级标题
（这里建议只包含一级标题，因为我们在笔记左侧已经有一级子主题了）

**加粗**，*斜体*，~~删除线~~，`python main.py`，$E=mc^2$，

有序列表
1. 第一项
2. 第二项
3. 第三项

无序列表
- 第一项
- 第二项
"""

# 定义请求和响应模型

#RecordResponse：
#表示 /record 接口的响应模型，包含以下字段：
#id：录音唯一标识。
#duration：录音时长（秒）。
#topic：录音主题。
#abstract：录音摘要。
#raw_recognition：识别的原始内容（一个 RawRecognition 列表）。
class RecordResponse(BaseModel):
    id: int
    duration: int
    topic: str
    abstract: str
    raw_recognition: list[RawRecognition]

#NoteRequest：
#表示 /note 接口的请求模型，包含以下字段：
#topic：笔记主题。
#abstract：笔记摘要。
#raw_recognition：识别的原始内容（一个 RawRecognition 列表）。
class NoteRequest(BaseModel):
    topic: str
    abstract: str
    raw_recognition: list[RawRecognition]

#NoteResponse：
#表示 /note 接口的响应模型，包含以下字段：
#points：笔记要点列表（一个 Point 列表）。
class NoteResponse(BaseModel):
    points: list[Point]

#捕获未处理的异常，记录日志，并返回通用的错误信息。
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    #全局异常处理器
    logging.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "服务器内部错误，请稍后重试"}
    )





#API 路由

#/test 测试接口
#一个简单的 GET 请求接口，返回字符串。
#会记录日志 Test endpoint accessed.
@app.get("/test", response_model=str)
async def test():
    logging.info("Test endpoint accessed.")
    return "Test endpoint accessed!"






# 语音转文字 应用whisper

# 加载 Whisper 模型
def load_whisper():
    try:
        logging.info("加载 Whisper 模型中...")
        # 可选择 'tiny', 'base', 'small', 'medium', 'large'
        model = whisper.load_model("base")
        logging.info("Whisper 模型加载成功！")
        return model
    except Exception as e:
        logging.critical(f"Whisper 模型加载失败: {e}")
        raise RuntimeError("模型加载失败，请检查配置。")

#上传文件并转文字 控制台交互不需要最后一个输出文件的参数 注意修改
def transcribe_audio(file_path: str, model,output_file: str):
    try:
        logging.info(f"正在处理音频文件: {file_path}")
        # 没有 GPU，设置 `fp16=False`
        result = model.transcribe(file_path, fp16=False)
        logging.info("语音转文字完成！")

        # 提取时间戳和文本段落
        segments = result['segments']  # 包含每段的时间戳和文本

        #纯文本没有时间戳的结果
        #transcription = result['text']

        #将结果写入日志
        #return result['text']

        # 将结果写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            for segment in segments:
                start_time = segment['start']  # 起始时间（秒）
                end_time = segment['end']      # 结束时间（秒）
                text = segment['text'].strip()  # 文本内容

                # 格式化输出 还需要转化时间格式
                line = f"[{start_time:.2f} - {end_time:.2f}] {text}\n"
                f.write(line)
        #logging.info(f"转录结果已成功保存到文件: {output_file}")

    except Exception as e:
        logging.error(f"语音转文字失败: {e}")
        raise RuntimeError("转文字失败，请重试")

#/record 上传录音接口
#模拟处理上传文件的 POST 请求接口。
#返回 RecordResponse，其中包含录音的相关信息（ID、时长、主题等）。
#如果出错，返回 400 错误。
@app.post("/record", response_model=RecordResponse)
async def post_record(file: UploadFile):
    #处理上传的音频文件，使用 Whisper 进行语音转文字。
    #:param file: 上传的音频文件
    #:return: 包含转录结果的 JSON 响应

    logging.info(f"收到音频文件上传请求: 文件名={file.filename}, 类型={file.content_type}")

    # 检查文件类型是否为支持的音频格式
    if file.content_type not in ["audio/mpeg", "audio/wav", "audio/mp3"]:
        logging.warning(f"不支持的文件类型: {file.content_type}")
        raise HTTPException(status_code=400, detail="Unsupported file type. Please upload a .mp3 or .wav file.")

    try:
        # 保存上传的音频文件到临时目录
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            temp_file.write(await file.read())
            temp_file_path = temp_file.name
        #logging.info(f"音频文件已保存到临时文件: {temp_file_path}")

        # 设置音频文件路径
        audio_file = temp_file_path

        # 获取用户桌面路径
        #output_file = r"C:\Users\13221\Desktop\transcription.mp3"
        home_dir = os.path.expanduser("~")
        desktop_dir = os.path.join(home_dir, "Desktop")
        output_file = os.path.join(desktop_dir, "transcription.txt")

        # 检查文件是否存在
        if not os.path.exists(audio_file):
            logging.error(f"音频文件未找到: {audio_file}")
            raise HTTPException(status_code=500, detail="Audio file not found.")
        else:
            # 加载模型
            whisper_model = load_whisper()

            # 转文字
            try:

                #控制台交互
                #transcription = transcribe_audio(audio_file, whisper_model)
                #logging.info(f"转录结果: {transcription}")

                #文件交互
                transcribe_audio(audio_file, whisper_model, output_file)
                logging.info(f"转录结果已保存到文件: {output_file}")

                # 读取转录结果
                with open(output_file, "r", encoding="utf-8") as f:
                        transcription = f.read()
                        #logging.info(f"转录内容: {transcription}")

                # 构造响应数据
                response = RecordResponse(
                    id=int(time.time()),  # 使用时间戳作为唯一标识符
                    duration=0,  # 暂时使用 0，具体时长需要从模型中获取
                    topic="自动识别的音频主题",  # 默认主题（可根据需求改为自动生成）
                    abstract="此音频的内容已自动转录。",  # 默认摘要（可进一步扩展）
                    raw_recognition=[RawRecognition(start=0, end=0, text=transcription)]
                    )
                logging.info(f"成功生成响应数据: ID={response.id}")
                return response

            except Exception as e:
                logging.error("处理过程中出现错误：%s", e)
                raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


            finally:
                # 删除临时文件
                os.remove(audio_file)
                #os.remove(output_file)
                logging.info(f"已删除临时文件: {audio_file}")

    except Exception as e:
        logging.error(f"处理音频文件时发生错误: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")





#/note 笔记生成接口
#模拟根据 NoteRequest 数据生成笔记。
#返回一个 NoteResponse，其中包含笔记要点、链接和子标题。
@app.post("/note", response_model=NoteResponse)
async def get_note(note: NoteRequest):
    try:
        logging.info(f"Received note request for topic: {note.topic}")
        await asyncio.sleep(2)  # 模拟异步延时
        response = NoteResponse(
            points=[
                Point(importance=2, name="布尔值", summary="布尔值是逻辑中的基本概念，它只有两个取值：真和假。", links=[
                    Link(name="维基百科", href="https://zh.wikipedia.org/wiki/%E5%B8%83%E5%B0%94%E5%80%BC"),
                    Link(name="布尔代数", href="https://zh.wikipedia.org/wiki/%E5%B8%83%E5%B0%94%E4%BB%A3%E6%95%B0"),
                ], subtitles=[
                    Subtitle(subtitle="真值表",
                             md=TEST_MARKDOWN,
                             raw_recognition=[
                                 RawRecognition(start=0, end=12, text="真值表的形式有几种形式？"),
                                 RawRecognition(start=13, end=25, text="真值表有几种形式？"),
                             ]
                    ),
                    Subtitle(subtitle="真值",
                             md="**真值**是指命题在某种特定条件下取真的结果。",
                             raw_recognition=[
                                 RawRecognition(start=22 * 60, end=22 * 60 + 12, text="什么是真值？"),
                                 RawRecognition(start=22 * 60 + 13, end=22 * 60 + 25, text="真值有什么用？"),
                             ]
                    ),
                ])
            ]
        )
        logging.info("Note processed successfully.")
        return response
    except Exception as e:
        logging.error(f"Error processing note request: {e}")
        raise HTTPException(status_code=400, detail="笔记生成失败")
