'''
Author: LetMeFly
Date: 2025-02-08 11:58:17
LastEditors: LetMeFly.xyz
LastEditTime: 2025-02-08 12:03:05
'''
import requests
from typing import Generator, Callable


def chatByFullMessage(payload: dict) -> Generator[str, any, None]:
    url = "https://api.siliconflow.cn/v1/chat/completions"
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
        
        for chunk in response.iter_lines():
            if chunk:  # 过滤空行
                # 这里可以添加对大模型返回数据的解析逻辑
                # print(chunk.decode('utf-8'))
                yield f"{chunk.decode('utf-8')}\n\n"
    
    return generate()
