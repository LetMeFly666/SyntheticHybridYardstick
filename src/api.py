'''
Author: LetMeFly
Date: 2025-02-06 13:18:12
LastEditors: LetMeFly.xyz
LastEditTime: 2025-02-07 17:06:45
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

    isFirst = True
    context = ""
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            if isFirst:
                isFirst = False
                print('*' * 50)
                print(chunk.decode('utf-8'))
                print('*' * 50)
            # thisContext = json.loads(chunk.decode('utf-8'))
            # context += thisContext
            # print(thisContext, end="", flush=True)

    print(context)

    print(response.text)
    json_: dict = response.json()
    if json_.get('code', 0) == 200:
        print('失败')

# {"id":"0194df8288d25e3cae8716b661b97ab0","object":"chat.completion","created":1738916661,"model":"deepseek-ai/DeepSeek-V3","choices":[{"index":0,"message":{"role":"assistant","content":"你好！我是一个人工智能助手，专门设计来回答问题和提供帮助。你可以问我任何问题，我会尽力提供准确和有用的信息。有什么我可以帮你的吗？"},"finish_reason":"stop"}],"usage":{"prompt_tokens":57,"completion_tokens":33,"total_tokens":90},"system_fingerprint":""}
# {"id":"0194df91160795b30b3eb502e11cc8b3","object":"chat.completion","created":1738917615,"model":"Pro/deepseek-ai/DeepSeek-R1-Distill-Llama-8B","choices":[{"index":0,"message":{"role":"assistant","content":"您好！我是由中国的深度求索（DeepSeek）公司开发的智能助手DeepSeek-R1。如您有任何任何问题，我会尽我所能为您提供帮助。","reasoning_content":"您好！我是由中国的深度求索（DeepSeek）公司开发的智能助手DeepSeek-R1。如您有任何任何问题，我会尽我所能为您提供帮助。"},"finish_reason":"stop"}],"usage":{"prompt_tokens":12,"completion_tokens":90,"total_tokens":102},"system_fingerprint":""} 
# 好家伙，上一个对话持续了好久好久才得到结果


