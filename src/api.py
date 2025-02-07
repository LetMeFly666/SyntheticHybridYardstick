'''
Author: LetMeFly
Date: 2025-02-06 13:18:12
LastEditors: LetMeFly.xyz
LastEditTime: 2025-02-07 17:14:53
'''
import requests
import json

url = "https://api.siliconflow.cn/v1/chat/completions"

payload = {
    # "model": "Pro/deepseek-ai/DeepSeek-R1-Distill-Llama-8B",
    "model": "Qwen/Qwen2.5-Coder-7B-Instruct",
    "messages": [
        {
            "role": "user",
            "content": "我通过API和硅基流动的大模型对话，现在是我需要等到模型全部结果返回后才能得到输出，我想实时显示输出，请问我应该怎么做"
        }
    ],
    "stream": True
}

headers = {
    "Authorization": f"Bearer {open('password', 'r').read()}",
    "Content-Type": "application/json"
}

with requests.post(url, json=payload, headers=headers, stream=True) as response:
    if response.status_code != 200:
        print(f'请求失败！状态码：{response.status_code}')
        exit(0)
    for chunk in response.iter_lines():
        if not chunk:
            continue
        decoded_chunk = chunk.decode('utf-8')
        json_chunk = json.loads(decoded_chunk.lstrip('data: '))
        print(json_chunk.get('choices')[0].get('delta').get('content'), end='', flush=True)

# data: {"id":"0194dfac237829626e211efa5e18801f","object":"chat.completion.chunk","created":1738919388,"model":"Qwen/Qwen2.5-Coder-7B-Instruct","choices":[{"index":0,"delta":{"content":"","reasoning_content":null,"role":"assistant"},"finish_reason":null,"content_filter_results":{"hate":{"filtered":false},"self_harm":{"filtered":false},"sexual":{"filtered":false},"violence":{"filtered":false}}}],"system_fingerprint":"","usage":{"prompt_tokens":61,"completion_tokens":0,"total_tokens":61}}
# {"id":"0194df8288d25e3cae8716b661b97ab0","object":"chat.completion","created":1738916661,"model":"deepseek-ai/DeepSeek-V3","choices":[{"index":0,"message":{"role":"assistant","content":"你好！我是一个人工智能助手，专门设计来回答问题和提供帮助。你可以问我任何问题，我会尽力提供准确和有用的信息。有什么我可以帮你的吗？"},"finish_reason":"stop"}],"usage":{"prompt_tokens":57,"completion_tokens":33,"total_tokens":90},"system_fingerprint":""}
# {"id":"0194df91160795b30b3eb502e11cc8b3","object":"chat.completion","created":1738917615,"model":"Pro/deepseek-ai/DeepSeek-R1-Distill-Llama-8B","choices":[{"index":0,"message":{"role":"assistant","content":"您好！我是由中国的深度求索（DeepSeek）公司开发的智能助手DeepSeek-R1。如您有任何任何问题，我会尽我所能为您提供帮助。","reasoning_content":"您好！我是由中国的深度求索（DeepSeek）公司开发的智能助手DeepSeek-R1。如您有任何任何问题，我会尽我所能为您提供帮助。"},"finish_reason":"stop"}],"usage":{"prompt_tokens":12,"completion_tokens":90,"total_tokens":102},"system_fingerprint":""} 
# 好家伙，上一个对话持续了好久好久才得到结果


