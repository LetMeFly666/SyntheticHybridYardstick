'''
Author: LetMeFly
Date: 2025-02-06 21:57:39
LastEditors: LetMeFly.xyz
LastEditTime: 2025-02-08 14:02:17
'''
# server.py
from flask import Flask, request, Response, jsonify, render_template_string, send_from_directory
import requests
import json
import webbrowser
import threading
import time
from src import chat
import os
import hashlib


app = Flask(__name__)
UPLOAD_FOLDER = 'case'


# 首页
@app.route('/')
def index():
    return render_template_string(open('static/html/index.html', 'r', encoding='utf-8').read())


# 单次对话
@app.route('/singleChat')
def singleChat():
    return render_template_string(open('static/html/singleChat.html', 'r', encoding='utf-8').read())


# js
@app.route('/static/js/<path:filename>')
def js(filename):
    print(filename)
    # filePath = os.path.join(app.root_path, '..', 'static', 'js')
    # filePath = f'{app.root_path}/static/js'
    filePath = f'{os.getcwd()}/static/js'
    print(filePath)
    return send_from_directory(filePath, filename)


# 文件上传
@app.route('/upload', methods=['POST'])
def upload():
    if 'files' not in request.files:
        return jsonify({'success': False, 'message': '未找到文件'}), 400
    files = request.files.getlist('files')
    for file in files:
        if file and file.filename.endswith(('.docx', '.doc')):
            file_content = file.read()
            md5 = hashlib.md5(file_content).hexdigest()
            fileData = {'fileName': file.filename}
            folder_path = os.path.join(UPLOAD_FOLDER, md5)
            configPath = os.path.join(folder_path, 'config.json')
            if os.path.exists(folder_path):
                with open(configPath, 'r', encoding='utf-8') as f:
                    originalData = json.loads(f.read())
                os.remove(''.join([folder_path, '/', originalData['fileName']]))
            else:
                os.makedirs(folder_path)
            file_path = os.path.join(folder_path, file.filename)
            with open(file_path, 'wb') as f:
                f.write(file_content)
            with open(configPath, 'w', encoding='utf-8') as f:
                f.write(json.dumps(fileData, ensure_ascii=False))
    return jsonify({'success': True, 'message': '文件上传成功'}), 200


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
