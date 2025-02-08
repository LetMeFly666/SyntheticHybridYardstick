'''
Author: LetMeFly
Date: 2025-02-08 22:10:18
LastEditors: LetMeFly.xyz
LastEditTime: 2025-02-08 22:13:11
'''
from flask import Flask, Response, jsonify, abort
import threading
from uuid import uuid4
import time
from collections import deque

app = Flask(__name__)

# 线程安全的对话存储
class ChatManager:
    def __init__(self):
        self.sessions = {}
        self.lock = threading.Lock()
        self.history = {}  # 存储已完成的对话
    
    def create_session(self):
        chat_id = str(uuid4())
        with self.lock:
            self.sessions[chat_id] = {
                'queue': deque(),
                'status': 'processing',
                'complete': threading.Event()
            }
        return chat_id
    
    def add_message(self, chat_id, content):
        with self.lock:
            if chat_id in self.sessions:
                self.sessions[chat_id]['queue'].append(content)
            elif chat_id in self.history:
                self.history[chat_id]['content'].append(content)
    
    def complete_session(self, chat_id):
        with self.lock:
            if chat_id in self.sessions:
                session = self.sessions.pop(chat_id)
                self.history[chat_id] = {
                    'content': list(session['queue']),
                    'status': 'completed'
                }
                session['complete'].set()
    
    def get_session(self, chat_id):
        with self.lock:
            if chat_id in self.sessions:
                return self.sessions[chat_id]
            return self.history.get(chat_id)

chat_manager = ChatManager()

# 模拟与DeepSeek的流式对话
def process_deepseek_chat(chat_id):
    # 这里替换为实际的DeepSeek API调用
    for i in range(50):
        time.sleep(1)  # 模拟流式延迟
        chat_manager.add_message(chat_id, f"{chat_id} DeepSeek response chunk {i+1}")
    
    # 完成对话
    chat_manager.complete_session(chat_id)
    print(f"Chat {chat_id} saved to history")

@app.route('/start_chat', methods=['POST'])
def start_chat():
    chat_id = chat_manager.create_session()
    # 启动模拟的异步处理线程
    threading.Thread(target=process_deepseek_chat, args=(chat_id,)).start()
    return jsonify({'chatId': chat_id})

@app.route('/chatData/<chat_id>')
def stream_chat_data(chat_id):
    def generate():
        session = chat_manager.get_session(chat_id)
        if not session:
            yield "event: error\ndata: Chat not found\n\n"
            return
        
        if 'complete' in session:  # 处理中的会话
            while not session['complete'].is_set():
                while session['queue']:
                    chunk = session['queue'].popleft()
                    yield f"data: {chunk}\n\n"
                time.sleep(0.1)
            
            # 确保发送最后的内容
            while session['queue']:
                chunk = session['queue'].popleft()
                yield f"data: {chunk}\n\n"
            
            yield "event: complete\ndata: done\n\n"
        else:  # 已完成的会话
            for chunk in session['content']:
                yield f"data: {chunk}\n\n"
            yield "event: complete\ndata: done\n\n"
    
    return Response(generate(), mimetype='text/event-stream')

@app.route('/chatStatus/<chat_id>')
def get_chat_status(chat_id):
    session = chat_manager.get_session(chat_id)
    if not session:
        abort(404)
    
    return jsonify({
        'status': session.get('status', 'completed'),
        'updated': len(session.get('content', [])) if 'status' not in session else None
    })

if __name__ == '__main__':
    app.run(threaded=True, port=5000)