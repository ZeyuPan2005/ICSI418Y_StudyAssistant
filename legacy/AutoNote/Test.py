# -*- coding: utf-8 -*-
"""
This file provide helper methods for testing API
Created on Fri Feb 14 11:14:12 2025
@author: Zeyu Pan
version 1
"""
#记录日志
import myLogging

# 获取默认的日志记录器
logging = myLogging.default_logger

# 用于发起服务端的请求
import requests

# 导入 json 模块
import json

import time

import uvicorn
from servers import app
from models import RecordResponse,NoteRequest,NetworkRequest

# 服务端 URL（根据你的服务端地址和端口修改）
host="127.0.0.1"
port=8000


def start_server():
    #以单独线程启动 FastAPI 服务
    uvicorn.run(app, host=host, port=port)

#测试 /record 接口
def test_record_endpoint():
    # 要测试的音频文件路径（修改为实际文件路径）
    #audio_file_path = r"C:\Users\13221\Desktop\test.mp3"
    video_file_path=r"C:\Users\13221\Desktop\排列与逆序.mp4"

    try:
        # 等待服务启动
        logging.info("等待服务启动...")
        # 等待 2 秒，确保服务正常启动
        time.sleep(2)

        # 打开音频文件，以二进制方式读取
        #with open(audio_file_path, "rb") as audio_file:
        #    #模拟上传文件的 POST 请求
        #    files = {"file": (audio_file_path, audio_file, "audio/mp3")}
        #    logging.info("开始测试 /record 接口...")
        #    response = requests.post(BASE_URL, files=files)

        #打开视频文件，以二进制方式读取
        with open(video_file_path, "rb") as video_file:
        #    # 模拟上传文件的 POST 请求
            files = {"file": (video_file_path, video_file, "video/mp4")}
            logging.info("开始测试 /record 接口...")
            response = requests.post( f"http://{host}:{port}/record", files=files)


        # 检查响应状态码并打印结果
        if response.status_code == 200:
            logging.info("测试成功！")
            #logging.info("测试成功！响应内容如下：")
            #logging.info(response.json())

            # 获取 JSON 数据
            response_json = response.json()

            # 确保响应包含所需的字段
            assert 'topic' in response_json, "响应数据中缺少 'topic' 字段"
            assert 'abstract' in response_json, "响应数据中缺少 'abstract' 字段"
            assert 'raw_recognition' in response_json, "响应数据中缺少 'raw_recognition' 字段"

            logging.info("返回数据验证通过！")

            # 创建 RecordResponse 对象并返回
            return RecordResponse(**response_json)
        else:
            logging.error(f"测试失败！状态码：{response.status_code}，响应内容：{response.text}")

    except FileNotFoundError:
        #logging.error(f"音频文件未找到: {audio_file_path}")
        logging.error(f"视频文件未找到: {video_file_path}")
        raise FileNotFoundError
    except Exception as e:
        logging.error(f"测试 /record 接口时发生错误: {e}")
        raise e

"""
根据recordResponse 生成 noteRequest
"""
def getNoteRequest(recordResponse:RecordResponse)-> NoteRequest:
    """
    根据 RecordResponse 生成 NoteRequest 对象。

    参数：
    - record_response (RecordResponse): 录音的响应模型。

    返回：
    - NoteRequest: 生成的笔记请求模型。
    """
    return NoteRequest(
        topic=recordResponse.topic,  # 直接从 RecordResponse 中获取主题
        abstract=recordResponse.abstract,  # 直接从 RecordResponse 中获取摘要
        raw_recognition=recordResponse.raw_recognition,  # 直接从 RecordResponse 中获取原始识别内容
        )


"""
# 测试 /note 接口
"""
def test_note_endpoint(recordResponse:RecordResponse):
    try:
        # 等待服务启动
        #logging.info("等待服务启动...")
        # 等待 2 秒，确保服务正常启动
        #time.sleep(2)

        #获取请求
        noteRequest=getNoteRequest(recordResponse)

        #logging.info(f"发送请求：{noteRequest}")

        noteRequest_dict = noteRequest.model_dump()

        # 模拟上传文件的 POST 请求
        logging.info("开始测试 /note 接口...")

        json_data = json.dumps(noteRequest_dict, ensure_ascii=False).encode("utf-8")  # 获取字典数据

        headers = {"Content-Type": "application/json; charset=utf-8"}
        response = requests.post(f"http://{host}:{port}/note", data=json_data, headers=headers)

        if response.status_code == 200:
            logging.info("测试成功！")
            # 获取并解码返回的响应内容为 utf-8
            #response_json = response.json()
            #logging.info(f"返回数据：{response_json}")
        else:
            logging.error(f"测试失败！状态码：{response.status_code}，响应内容：{response.text}")

    except Exception as e:
        logging.error(f"测试 /note 接口时发生错误: {e}")
        raise e

"""
#测试 /network 接口
"""
def test_network_endpoint():
    try:
        # 模拟上传文件的 POST 请求
        logging.info("开始测试 /network 接口...")

        #测试数据
        testData=getTestData()

        json_data = json.dumps(testData, ensure_ascii=False).encode("utf-8")  # 获取字典数据

        headers = {"Content-Type": "application/json; charset=utf-8"}
        response = requests.post(f"http://{host}:{port}/network", data=json_data, headers=headers)

        if response.status_code == 200:
            logging.inof("测试成功！")
        else:
            logging.error(f"测试失败！状态码：{response.status_code}，响应内容：{response.text}")

    except Exception as e:
        logging.error(f"测试 /network 接口时发生错误: {e}")
        raise e

def getTestData():
    data={
    "lectures": [
        {
            "id": 43,
            "topic": "https://loremflickr.com/400/400?lock=2198548917284926",
            "points": [
                {
                    "name": "杜俊熙",
                    "importance": 2,
                    "subtitles": [
                        {
                            "subtitle": "年度无论谁嘘喔耶",
                            "md": "nostrud",
                            "raw_recognition": [
                                {
                                    "start": 25,
                                    "end": 91,
                                    "text": "约在命总维她强水只万。"
                                },
                                {
                                    "start": 32,
                                    "end": 54,
                                    "text": "等实红型。济运较消置院因与识联。统知响压属间住。"
                                },
                                {
                                    "start": 32,
                                    "end": 1,
                                    "text": "着数山此。约只表流道千人。指使同法量只开身并图。"
                                }
                            ]
                        },
                        {
                            "subtitle": "撒篝火当然擒哎哟无论哪里",
                            "md": "sint deserunt ut",
                            "raw_recognition": [
                                {
                                    "start": 100,
                                    "end": 80,
                                    "text": "参而日本设。气明状。再在己。\n日别那并。难最土织划史气。深自出。\n阶分达龙必包机会可可。研指七法消机术。阶个理马给。"
                                },
                                {
                                    "start": 43,
                                    "end": 88,
                                    "text": "林美即亲现织又我张。众还法广。大给与。"
                                },
                                {
                                    "start": 83,
                                    "end": 43,
                                    "text": "思得听研容结然分看转。被人计在话于历取义这。结能外省采。"
                                }
                            ]
                        },
                        {
                            "subtitle": "在除了雪白穿过血淋淋朝向因此意识的",
                            "md": "in minim mollit",
                            "raw_recognition": [
                                {
                                    "start": 77,
                                    "end": 68,
                                    "text": "完文往极面处其治上。增用门难加那具。包除土场样科支领总步。"
                                },
                                {
                                    "start": 28,
                                    "end": 66,
                                    "text": "包行运。"
                                },
                                {
                                    "start": 14,
                                    "end": 49,
                                    "text": "什细少说标便复加。"
                                }
                            ]
                        }
                    ],
                    "links": [
                        {
                            "name": "祁开慧",
                            "href": "anim officia"
                        },
                        {
                            "name": "繁梓诚",
                            "href": "sed labore"
                        },
                        {
                            "name": "由萍",
                            "href": "Excepteur nostrud"
                        }
                    ],
                    "summary": "laboris adipisicing"
                }
            ]
        },
        {
            "id": 74,
            "topic": "https://loremflickr.com/400/400?lock=6087087268967745",
            "points": [
                {
                    "name": "节婷婷",
                    "importance": 1,
                    "subtitles": [
                        {
                            "subtitle": "抚秋海棠跳男朋友平坦因此熟练哪里每当相反",
                            "md": "do esse",
                            "raw_recognition": [
                                {
                                    "start": 94,
                                    "end": 92,
                                    "text": "维将酸需算果除上。团见土她一个划作收。式持争接结。\n全分手术。叫且效。议备水要务月建别。\n市研文专见东。听门文深几。接对求按量飞五眼。"
                                },
                                {
                                    "start": 53,
                                    "end": 3,
                                    "text": "口回集音查委。离装效做论回术次。商特系生质领此精其。\n土千式过书形展。量看设第层。系精整务厂决。\n亲济片连了。科只铁。厂收九给值程交。"
                                },
                                {
                                    "start": 1,
                                    "end": 60,
                                    "text": "至间格场之型设层教。下易指。构太布律。主风组京该取。便内中相少。技火为行。"
                                }
                            ]
                        }
                    ],
                    "links": [
                        {
                            "name": "殷政君",
                            "href": "ut sit fugiat ut tempor"
                        }
                    ],
                    "summary": "deserunt nulla sint quis adipisicing"
                },
                {
                    "name": "行一诺",
                    "importance": 1,
                    "subtitles": [
                        {
                            "subtitle": "直到除了好啊羚羊净",
                            "md": "voluptate cupidatat aliquip dolore",
                            "raw_recognition": [
                                {
                                    "start": 32,
                                    "end": 29,
                                    "text": "美电点观目。律解压近以。交参是目。\n清员带眼率。样养验采育往切受型南。是指克及选。\n组商理合号解整。素上历手天查质。价得没起这。"
                                },
                                {
                                    "start": 67,
                                    "end": 16,
                                    "text": "交理响山知做量样。"
                                }
                            ]
                        },
                        {
                            "subtitle": "整齐就吐小熟人大约简直",
                            "md": "est incididunt",
                            "raw_recognition": [
                                {
                                    "start": 58,
                                    "end": 45,
                                    "text": "义数及具至维始。效更整运代。化加值导。\n最该角。量花转展效阶知己布。象真一义温节用何极实。\n处形解传。各风向离我他。低除究它明长局。"
                                },
                                {
                                    "start": 88,
                                    "end": 35,
                                    "text": "育多还日。\n步使物价养。"
                                }
                            ]
                        }
                    ],
                    "links": [
                        {
                            "name": "佴政君",
                            "href": "minim et aliquip"
                        },
                        {
                            "name": "范婷",
                            "href": "consectetur velit aliquip irure qui"
                        }
                    ],
                    "summary": "ipsum esse proident minim voluptate"
                },
                {
                    "name": "索成",
                    "importance": 3,
                    "subtitles": [
                        {
                            "subtitle": "像以免畅销书沿着",
                            "md": "non commodo",
                            "raw_recognition": [
                                {
                                    "start": 19,
                                    "end": 54,
                                    "text": "便着美区美引来又认。决感她机人率。或飞交报东型。"
                                }
                            ]
                        },
                        {
                            "subtitle": "果然绿油油软修订",
                            "md": "est nostrud tempor",
                            "raw_recognition": [
                                {
                                    "start": 24,
                                    "end": 100,
                                    "text": "支并出。\n复的装信月酸体新新。\n性太区改大区此意为六。\n值委务必划片意。\n快机带。"
                                },
                                {
                                    "start": 19,
                                    "end": 43,
                                    "text": "标全身说我时。几度响中速土原划列然。放书院空和科素极力。\n更验先定。知先心车包年月所联。是精部象理石样。\n头立查始老。问院出林路情。存角程本派回易它况准。"
                                },
                                {
                                    "start": 86,
                                    "end": 85,
                                    "text": "流问飞得很步力别查严。即布阶任土。矿圆斯。查统确几长。物照五之法带在他点后。名别受酸发系。"
                                }
                            ]
                        },
                        {
                            "subtitle": "仅仅移动捣只呸大方所以除了拧",
                            "md": "aute nisi dolore consectetur nulla",
                            "raw_recognition": [
                                {
                                    "start": 40,
                                    "end": 11,
                                    "text": "性求整状但。表同部你元及。保真体就采调它其往二。"
                                },
                                {
                                    "start": 83,
                                    "end": 58,
                                    "text": "发群一他义。山们电是后任。始张青流生更放都酸定。"
                                },
                                {
                                    "start": 90,
                                    "end": 58,
                                    "text": "地权查音复太带元两期。\n消构最百造就装。"
                                }
                            ]
                        }
                    ],
                    "links": [
                        {
                            "name": "奕倩",
                            "href": "culpa cillum voluptate"
                        },
                        {
                            "name": "卯雪",
                            "href": "pariatur"
                        },
                        {
                            "name": "哈天娇",
                            "href": "sint nisi ut"
                        }
                    ],
                    "summary": "sit non sunt Duis"
                }
            ]
        }
    ]
}
    return data
