'''
Author: LetMeFly
Date: 2025-02-08 11:58:17
LastEditors: LetMeFly.xyz
LastEditTime: 2025-02-09 14:27:19
'''
import requests
from typing import Generator, Callable

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
        
        for chunk in response.iter_lines():
            if chunk:  # 过滤空行
                # 这里可以添加对大模型返回数据的解析逻辑
                # print(chunk.decode('utf-8'))
                with open('chat.log', 'a', encoding='utf-8') as f:
                    f.write(f"{chunk.decode('utf-8')}\n")
                yield f"{chunk.decode('utf-8')}\n\n"
    
    return generate()
