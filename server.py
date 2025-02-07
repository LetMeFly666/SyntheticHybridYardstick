'''
Author: LetMeFly
Date: 2025-02-06 21:57:39
LastEditors: LetMeFly.xyz
LastEditTime: 2025-02-07 22:31:25
'''
# server.py
from flask import Flask, request, Response, render_template_string
import requests
import json

app = Flask(__name__)

# 首页路由，直接返回 HTML 页面
@app.route('/')
def index():
    return render_template_string(open('src/index.html', 'r', encoding='utf-8').read())

# 流式响应路由
@app.route('/chat')
def chat_stream():
    query = request.args.get('query')
    
    # 转发到大模型API（示例URL，需替换为真实API）
    url = "https://api.siliconflow.cn/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {open('password', 'r').read()}",
        "Content-Type": "application/json"
    }
    payload = {
        # "model": "Pro/deepseek-ai/DeepSeek-R1-Distill-Llama-8B",
        "model": "Qwen/Qwen2.5-Coder-7B-Instruct",
        "messages": [
            {
                "role": "user",
                "content": query
            }
        ],
        "stream": True
    }
    
    # 关键：以流模式转发请求
    def generate():
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
    
    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(host='shy.local.letmefly.xyz', port=4140, debug=True)