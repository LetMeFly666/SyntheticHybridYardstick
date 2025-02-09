'''
Author: LetMeFly
Date: 2025-02-06 21:57:39
LastEditors: LetMeFly.xyz
LastEditTime: 2025-02-09 14:13:32
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
    
    payload = {
        # "model": "Pro/deepseek-ai/DeepSeek-R1-Distill-Llama-8B",  # 硅基流动
        # "model": "Qwen/Qwen2.5-Coder-7B-Instruct",  # 硅基流动
        "model": "deepseek-r1",  # 腾讯云
        "messages": [
            {
                "role": "user",
                "content": query
            }
        ],
        "stream": True
    }
    
    return Response(chat.chatByFullMessage(payload), mimetype='text/event-stream')


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
    )

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
