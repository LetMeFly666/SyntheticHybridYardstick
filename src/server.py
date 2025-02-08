'''
Author: LetMeFly
Date: 2025-02-06 21:57:39
LastEditors: LetMeFly.xyz
LastEditTime: 2025-02-08 12:04:04
'''
# server.py
from flask import Flask, request, Response, render_template_string
import requests
import json
import webbrowser
import threading
import time
from src import chat

app = Flask(__name__)

# 首页路由，直接返回 HTML 页面
@app.route('/')
def index():
    return render_template_string(open('src/index.html', 'r', encoding='utf-8').read())

# 流式响应路由
@app.route('/chat')
def chat_stream():
    query = request.args.get('query')
    
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
    
    return Response(chat.chatByFullMessage(payload), mimetype='text/event-stream')


def run_flask():
    app.run(host='shy.local.letmefly.xyz', port=4140, debug=False)


def open_browser():
    time.sleep(1.5)
    webbrowser.open('http://shy.local.letmefly.xyz:4140')


def main():
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.start()
    run_flask()
    browser_thread.join()


if __name__ == '__main__':
    main()
