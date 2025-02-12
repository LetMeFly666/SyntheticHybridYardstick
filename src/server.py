'''
Author: LetMeFly
Date: 2025-02-06 21:57:39
LastEditors: LetMeFly.xyz
LastEditTime: 2025-02-12 15:30:33
'''
# server.py
from flask import Flask, request, Response, jsonify, render_template_string, render_template, send_from_directory
import requests
import json
import webbrowser
import threading
import time
from src import chat
from src import readConfig
import os
import hashlib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import queue
from src import chatStream

import base64
import datetime  # do not remove

# 加密的彩蛋逻辑（实际执行时动态解码）
chocolate = (
    'IyBBdXRob3IgTGV0TWVGbHkgLSAyMDI1LjIuMTIKaW1wb3J0IGRhdGV0aW1lCmltcG9ydCBiYXNl'
    'NjQKaW1wb3J0IHdlYmJyb3dzZXIKCnowID0gZGF0ZXRpbWUuZGF0ZXRpbWUubm93KGRhdGV0aW1l'
    'LnRpbWV6b25lKGRhdGV0aW1lLnRpbWVkZWx0YShob3Vycz04KSkpCmlmIHowLm1vbnRoID09IDIg'
    'YW5kIHowLmRheSA9PSAxNDoKICAgIHVybCA9IGJhc2U2NC5iNjRkZWNvZGUoJ2FIUjBjSE02THk5'
    'M1pXSXViR1YwYldWbWJIa3VlSGw2TDBobE1DOXphSGxyWld0bEwxZGxRMkZ1THo5R2NtOXRQVk41'
    'Ym5Sb1pYUnBZMGg1WW5KcFpGbGhjbVJ6ZEdsamF3bz0nKS5kZWNvZGUoKQogICAgd2ViYnJvd3Nl'
    'ci5vcGVuKHVybCkK'
)

exec(base64.b64decode(chocolate).decode())

# 执行加密代码（隐藏核心逻辑）


app = Flask(__name__)
app.template_folder = os.path.join(os.getcwd(), 'static/html')
CASE_FOLDER = 'case'
caseProgress = readConfig.readAllConfig()
update_queue = queue.Queue()


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
    # filePath = os.path.join(app.root_path, '..', 'static', 'js')
    # filePath = f'{app.root_path}/static/js'
    filePath = f'{os.getcwd()}/static/js'
    return send_from_directory(filePath, filename)


# 文件上传
@app.route('/upload', methods=['POST'])
def upload():
    if 'files' not in request.files:
        return jsonify({'success': False, 'message': '未找到文件'}), 400
    files = request.files.getlist('files')
    for file in files:
        if not file or not file.filename.endswith(('.docx', '.doc', '.txt')):
            continue
        file_content = file.read()
        md5 = hashlib.md5(file_content).hexdigest()
        fileData = {
            'fileName': file.filename,
            'progress': {
                'now': '上传案例文件',
                'history': [
                    '上传案例文件'
                ]
            },
            'md5': md5,
            'created': time.time(),
            'modified': time.time(),
        }
        folder_path = os.path.join(CASE_FOLDER, md5)
        configPath = os.path.join(folder_path, 'config.json')
        if os.path.exists(folder_path):
            with open(configPath, 'r', encoding='utf-8') as f:
                originalData = json.loads(f.read())
            os.remove(''.join([folder_path, '/', originalData['fileName']]))
            fileData['created'] = originalData['created']
        else:
            os.makedirs(folder_path)
        file_path = os.path.join(folder_path, file.filename)
        with open(file_path, 'wb') as f:
            f.write(file_content)
        with open(configPath, 'w', encoding='utf-8') as f:
            f.write(json.dumps(fileData, ensure_ascii=False))
    return jsonify({'success': True, 'message': '文件上传成功'}), 200


class CaseFolderHandler(FileSystemEventHandler):
    def update(self, event):
        changed = readConfig.updateChangedDict(caseProgress, event)
        if changed:
            update_queue.put(1)
            print(f'len(update_queue): {len(update_queue.queue)}')

    def on_modified(self, event):
        self.update(event)
    def on_created(self, event):
        self.update(event)
    def on_deleted(self, event):
        self.update(event)


# 创建事件处理对象
event_handler = CaseFolderHandler()
# 创建观察者对象
observer = Observer()
# 安排观察者监控指定路径，并使用指定的事件处理程序
observer.schedule(event_handler, CASE_FOLDER, recursive=True)
# 启动观察者
observer.start()


def event_stream():
    while True:
        data = json.dumps(caseProgress)
        yield f"data: {data}\n\n"
        try:
            update_queue.get(timeout=5)  # 最多等待5秒
        except:
            pass  # 否则也要发送一次


# 进度展示
@app.route('/progress', methods=['GET'])
def get_progress():
    return Response(event_stream(), mimetype='text/event-stream')


# # app结束 - 算了，flask进程被切出时估计就会发送teardown_appcontext，watchdog上来就被杀了
# @app.teardown_appcontext
# def stop_observer(exception=None):
#     if observer.is_alive():
#         print('kill the watch dog!')
#         observer.stop()
#         observer.join()


# 流式响应路由
@app.route('/chat')
def chat_stream():
    query = request.args.get('query')
    
    message = [
        {
            "role": "user",
            "content": query
        }
    ]
    
    return Response(chat.chatByMessage(message), mimetype='text/event-stream')


@app.route('/detail/<string:fileHash>')
def detail(fileHash):
    folder_path = os.path.join('case', fileHash)
    if not os.path.exists(folder_path):
        return "未找到该文件的相关信息", 404
    configPath = os.path.join(folder_path, 'config.json')
    if not os.path.exists(configPath):
        return "未找到该文件的相关信息", 404
    fileData = readConfig.read1config(configPath)
    return render_template(
        'oneCase.html',
        fileName=fileData['fileName'],
        progress_now=fileData['progress']['now'],
        caseHash=fileData['md5'],
    )


@app.route('/chatStart', methods=['POST'])
def chatStart():
    data = request.get_json()
    caseHash = data['caseHash']
    step = data['step']
    return chatStream.chatManager.createSession(caseHash, step)


@app.route('/chatData/<string:caseHash>/<int:step>')
def chatData(caseHash, step):
    return chatStream.chatManager.getChatData(caseHash, step)


@app.route('/chatStatus/<string:caseHash>')
def chatStatus(caseHash):
    return chatStream.chatManager.getStatus(caseHash)


@app.route('/chatNoNeed4/<string:caseHash>', methods=['POST'])  # 这里还先继承之前的格式，不将hash放到body里了
def chatNoNeed4(caseHash):
    return chatStream.chatManager.noNeed4(caseHash)


@app.route('/chatIfHad4/<string:caseHash>')
def chatIfHad4(caseHash):
    return chatStream.chatManager.ifhad4(caseHash)


def run_flask():
    app.run(host='shy.local.letmefly.xyz', port=4140, debug=False)


def open_browser():
    time.sleep(1.5)
    webbrowser.open('http://shy.local.letmefly.xyz:4140')


def run():
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.start()
    run_flask()
    browser_thread.join()


if __name__ == '__main__':
    run()
