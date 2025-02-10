'''
Author: LetMeFly
Date: 2025-02-08 11:58:17
LastEditors: LetMeFly.xyz
LastEditTime: 2025-02-10 22:26:14
'''
import requests
from typing import Generator, Callable, List
import random
import string
import os
import json
import datetime
import pytz


# 腾讯云文档 https://cloud.tencent.com/document/product/1772/115969
# 有效至 2025年2月25日23:59:59

def chatByFullMessage(payload: dict) -> Generator[str, any, None]:
    
    # url = "https://api.siliconflow.cn/v1/chat/completions"  # 硅基流动
    url = "https://api.lkeap.cloud.tencent.com/v1/chat/completions"  # 腾讯云
    headers = {
        "Authorization": f"Bearer {open('password', 'r').read()}",
        "Content-Type": "application/json"
    }
    
    def generate() -> Generator[str, any, None]:
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            stream=True
        )

        all_characters = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(all_characters) for i in range(47))
        folderPath = f'case/otherHistory/{random_string}'
        os.makedirs(folderPath, exist_ok=True)
        with open(f'{folderPath}/question.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(payload, ensure_ascii=False))
        
        utc_plus_8 = datetime.timezone(datetime.timedelta(hours=8))
        current_time = datetime.datetime.now(utc_plus_8)
        time_string_with_tz = current_time.isoformat(timespec='seconds')
        with open(f'{folderPath}/time.txt', 'w', encoding='utf-8') as f:
            f.write(time_string_with_tz)
        
        responseData = ''
        thinking = False
        for chunk in response.iter_lines():
            if not chunk:  # 过滤空行
                continue
            try:
                data = json.loads(chunk.decode('utf-8').strip('data: '))
                thinkData = data['choices'][0]['delta'].get('reasoning_content', '')
                contentData = data['choices'][0]['delta'].get('content', '')
                if thinkData:
                    if not thinking:
                        thinking = True
                        responseData += '<div class="thinkTag">\n'
                    responseData += thinkData
                if contentData:
                    if thinking:
                        thinking = False
                        responseData += '\n\n</div>\n\n'
                    responseData += contentData
            except:
                pass
            toReturn = f"{chunk.decode('utf-8')}\n\n"
            if not toReturn.startswith('data: '):
                toReturn = 'data: ' + toReturn
            yield toReturn
    
        with open(f'{folderPath}/response.txt', 'w', encoding='utf-8') as f:
            f.write(responseData)
    
    return generate()


def chatByMessage(messages: List[dict]) -> Generator[str, any, None]:
    payload = {
        # "model": "Pro/deepseek-ai/DeepSeek-R1-Distill-Llama-8B",  # 硅基流动
        # "model": "Qwen/Qwen2.5-Coder-7B-Instruct",  # 硅基流动
        "model": "deepseek-r1",  # 腾讯云
        "messages": messages,
        "stream": True
    }
    return chatByFullMessage(payload)