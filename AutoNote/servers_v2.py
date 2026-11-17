# -*- coding: utf-8 -*-
"""
This project has set up a server for communication
between the front-end and back-end
Created on Tue Jan 21 15:53:05 2025
@author: Zeyu Pan
version 2
"""
#用于模拟延时
import time
#FastAPI 的强项在于异步执行。await asyncio.sleep 实现异步延时。
import asyncio

#记录日志
import myLogging

#FAST API 创建 Web API 框架。
from fastapi import FastAPI, UploadFile, HTTPException

from entities import RawRecognition, Point, Link, Subtitle,NoteRoute,NodeLink,Lecture,Node,NodeCategory

import os

import warnings

#引入响应和请求
import models

#引入recordAPI的辅助函数
import recordAPI_helper


#创建了一个 FastAPI 应用实例，用于注册 API 路由和处理请求
app = FastAPI()

# 获取默认的日志记录器
logging = myLogging.default_logger

#API 路由

"""
#/test 测试接口
#一个简单的 GET 请求接口，返回字符串。
#会记录日志 Test endpoint accessed.
"""
@app.get("/test", response_model=str)
async def test():
    logging.info("Test endpoint accessed.")
    return "Test endpoint accessed!"

"""
#/record 上传录音接口
#模拟处理上传文件的 POST 请求接口。
#返回 RecordResponse，其中包含录音的相关信息（ID、时长、主题等）。
#如果出错，返回 400 错误。
"""
@app.post("/record", response_model=models.RecordResponse)
async def post_record(file: UploadFile, fake: bool = False):
    """
    #处理上传的音频文件，使用 Whisper 进行语音转文字。
    #:param file: 上传的音频文件
    #:return: 包含转录结果的 JSON 响应
    """

    if fake:
       time.sleep(2)  # 模拟延时
       return models.RecordResponse.fake()

    logging.info(f"收到音频文件上传请求: 文件名={file.filename}, 类型={file.content_type}")

    try:
        # 保存上传的文件到临时目录
        saved_file_path = await recordAPI_helper.save_uploaded_file(file)
        logging.info(f"文件保存成功: {saved_file_path}")

        # 设置音频文件路径
        audio_file = saved_file_path

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
            #设置忽略警告
            warnings.simplefilter("ignore", UserWarning)
            #检查GPU
            recordAPI_helper.check_gpu()
            #检查设备类型 是GPU还是CPU
            device = recordAPI_helper.check_device()
            #device="cpu"
            logging.info(f"Using device: {device}")

            # 加载模型
            whisper_model = recordAPI_helper.load_whisper(device)

            # 转文字
            try:

                #控制台交互
                #transcription = transcribe_audio(audio_file, whisper_model)
                #logging.info(f"转录结果: {transcription}")

                #文件交互
                result=recordAPI_helper.transcribe_audio(audio_file, whisper_model, output_file,device)
                logging.info(f"转录结果已保存到文件: {output_file}")

                # 读取转录结果
                with open(output_file, "r", encoding="utf-8") as f:
                        transcription = f.read()
                        #logging.info(f"转录内容: {transcription}")

                topic_and_abstract=recordAPI_helper.get_topic_and_abstract(transcription)
                topic_str=topic_and_abstract['topic'].split('：')[1]
                abstract_str=topic_and_abstract['abstract'].split('：')[1]

                rawRecognitions=[]
                for rawRecognition in result:
                    rawRecognitions.append(RawRecognition(start=recordAPI_helper.time_conversion(rawRecognition.split("\t")[0]),text=rawRecognition.split("\t")[1]))

                # 构造响应数据
                response = models.RecordResponse(
                    id=int(time.time()),  # 使用时间戳作为唯一标识符
                    # 将最后一行记录的开始时间作为总时长 单位 秒
                    duration=recordAPI_helper.time_conversion(result[-1].split("\t")[0]),
                    topic=topic_str,
                    abstract=abstract_str,
                    raw_recognition=rawRecognitions
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

"""
#/note 笔记生成接口
#模拟根据 NoteRequest 数据生成笔记。
#返回一个 NoteResponse，其中包含笔记要点、链接和子标题。
"""
@app.post("/note", response_model=models.NoteResponse)
async def get_note(note: models.NoteRequest):
    try:
        logging.info(f"Received note request for topic: {note.topic}")
        await asyncio.sleep(2)  # 模拟异步延时
        response = models.NoteResponse(
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
