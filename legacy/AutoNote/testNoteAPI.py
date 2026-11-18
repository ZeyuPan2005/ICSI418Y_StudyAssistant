# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 15:58:22 2025

@author: 13221
"""
# 大模型部分依赖库
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

import time
start_time = time.time()
time_now=time.strftime("%Y%m%d%H%M", time.localtime())

import os

# 设置输入输出文件
input_file = os.path.join(os.path.expanduser('~'), 'Desktop', 'transcription.txt')
output_file1 = os.path.join(os.path.expanduser('~'), 'Desktop', f'英文输出_airOrlong_{time_now}.md')
output_file2 = os.path.join(os.path.expanduser('~'), 'Desktop', f'英文输出_airOrlong_{time_now}.json')

# 读取文件
# with open(input_file, 'r', encoding='utf-8') as f:
#     record_text = f.read()
with open(input_file, 'r', encoding='utf-8') as f:#输入改成列表
    record_text_l = f.readlines()
print(record_text_l)
record_text = []
for _ in record_text_l:
    _ = _.replace('\n','')
    record_text.append((_.split('\t')[0],_.split('\t')[1]))
    #record_text.append((_.split(']')[0].replace('[',''),_.split(']')[1]))
#print(record_text)

time0 = time.time()
print("读取输入文件成功，当前步骤耗时：", f"{time0-start_time:.2f}s",f"总耗时：{time0-start_time:.2f}s")

# 初始化 OpenAI 客户端（在这里使用的是 Zhipu AI）
client = OpenAI(
     # Zhipu AI API key
     api_key=os.environ["ZHIPU_API_KEY"],
     base_url="https://open.bigmodel.cn/api/paas/v4",  # Ensure URL is correct
)
print("ChatOpenAI 模型初始化成功")


# 构建一个消息模板，定义聊天的格式
prompt=(
       f"请根据以下内容生成一个简洁的主题和摘要（请用Markdown格式）:\n\n{record_text}\n\n"
       "用户以元组列表形式输入一堂课的录音文本，元组的第1项为这句话的时间，第2项为这句话的文本，你被要求先优化识别错误的内容，然后根据处理后的文本，以文本形式输出一个课堂笔记，内容是：1.课程主题。2.课程摘要。3.详细的知识点笔记(每个知识点包含名称、重要程度（整数1-5，5代表最重要）、然后由子要点阐述解释或例子（子要点如定义、应用、证明等），每个子要点的标题前要有这个概念在录音文本中第一次被提到的时间（即这个子要点的开始时间），每个要点后附这个子要点对应的全部文本，即不要有任何改动的原文本））。4.几个关键词及对应的参考网站。"
       "示例如下："
       "详细的知识点笔记：1. 二阶行列式的定义与计算 (重要程度：5)：（00:01）二阶行列式的定义：一个方程组的系数矩阵的主对角线元素之积，即对角线元素的乘积；（03：52）二阶行列式的计算方法：利用二阶行列式的定义，将方程组的系数矩阵化为上三角矩阵，再利用对角线元素的乘积求和。2. 三阶行列式的定义与计算 (重要程度：5)：（05：44）三阶行列式的定义：一个方程组的系数矩阵的主对角线元素之积，即对角线元素的乘积；（08：36）三阶行列式的计算方法：利用代数余子式的性质，利用三阶行列式的定义，将方程组的系数矩阵化为上三角矩阵，再利用对角线元素的乘积求和。3.特殊行列式（重要程度：3）：（15:03)上三角行列式：是主对角线以下的元素均为零的行列式，其值等于主对角线元素的乘积;（16:27)下三角行列式：主对角线以上的元素均为零的行列式，其值等于主对角线元素的乘积。关键词及参考网站：行列式 - 维基百科：https://zh.wikipedia.org/wiki/%E8%A1%8C%E5%88%97%E5%BC%8F；线性代数 - 可汗学院：https://zh.khanacademy.org/math/linear-algebra"
)
print("消息模板构建成功")

# 向 AI 模型发送请求并获取回复，指定使用的模型（glm-4）
completion = client.chat.completions.create(
    model="glm-4-air-0111",  # 在这里指定模型
    max_tokens=2000,
    messages=[
        {"role": "user", "content": prompt},
    ],
)

print(completion.choices[0].message.content)
