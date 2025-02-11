'''
Author: LetMeFly
Date: 2025-02-09 10:18:43
LastEditors: LetMeFly.xyz
LastEditTime: 2025-02-11 13:47:23
'''
from flask import Flask, Response, jsonify, abort
import threading
from uuid import uuid4
import time
from collections import deque
from typing import Dict, TypedDict, Generator
from src import file
from src import chat
import os
import requests
import json


class SessionDict(TypedDict):
    status: str
    complete: threading.Event
    toSend: str
    sent: str


class Session:
    def __init__(self) -> None:
        self.session: SessionDict = {
            'status': 'processing',
            'complete': threading.Event(),
            'toSend':'',
            'sent': '',
        }

class ChatManager:
    def __init__(self) -> None:
        self.sessions: Dict[str, Session] = {}
        self.lock = threading.Lock()

    
    def __addMessage(self, chatId: str, content: str) -> None:
        with self.lock:
            self.sessions[chatId].session['toSend'] += content


    def __completeChat(self, caseHash: str) -> None:
        with self.lock:
            session = self.sessions[caseHash].session
            session['status'] = 'completed'
            data = session['sent'] + session['toSend']
            with open(f'case/{caseHash}/chat/02.txt', 'w', encoding='utf-8') as f:
                f.write(data)
            config = file.read_config(f'case/{caseHash}/config.json')
            config['progress']['now'] = 'DS初步分析'
            config['progress']['history'].append('DS初步分析')
            config['modified'] = time.time()
            with open(f'case/{caseHash}/config.json', 'w', encoding='utf-8') as f:
                f.write(json.dumps(config, ensure_ascii=False))
            session['complete'].set()
        time.sleep(1)  # 防止前端数据未读取完毕
        with self.lock:
            self.sessions.pop(caseHash)
    
    
    def __chat(self, caseHash: str, chatData: list) -> None:
        url = "https://api.lkeap.cloud.tencent.com/v1/chat/completions"  # 腾讯云
        headers = {
            "Authorization": f"Bearer {open('password', 'r').read()}",
            "Content-Type": "application/json"
        }
        response = requests.post(
            url,
            json={
                "model": "deepseek-r1",  # 腾讯云
                "messages": chatData,
                "stream": True
            },
            headers=headers,
            stream=True
        )
        
        thinking = False  # 假设如果有think一定是在对话的开始
        for chunk in response.iter_lines():
            if not chunk:
                continue
            data = chunk.decode('utf-8').strip('data: ')
            if data == '[DONE]':
                break
            data = json.loads(data)
            if 'error' in data and 'message' in data['error'] and data['error']['message'] == 'concurrency exceeded':
                print('对话失败，并发过大')  # 这就不往前端传了
                with self.lock:
                    self.sessions.pop(caseHash)
                return
            thinkData = data['choices'][0]['delta'].get('reasoning_content', '')
            contentData = data['choices'][0]['delta'].get('content', '')
            if thinkData:
                if not thinking:  # 第一个thinking
                    thinking = True
                    self.__addMessage(caseHash, '<div class="thinkTag">\n')
                self.__addMessage(caseHash, thinkData)
            if contentData:
                if thinking:  # 第一个content
                    thinking = False
                    self.__addMessage(caseHash, '\n\n</div>\n\n')
                self.__addMessage(caseHash, contentData)
        self.__completeChat(caseHash)
    

    def __getChatData(self, caseHash: str) -> Generator:
        msgDict = {
            'code': 0,
            'content': '',
        }
        notInMem = False
        session: SessionDict
        with self.lock:
            if caseHash not in self.sessions:
                notInMem = True
            else:
                session = self.sessions[caseHash].session
        if notInMem:
            print('not in mem')
            if not os.path.exists(f'case/{caseHash}/chat/02.txt'):
                msgDict['code'] = 2
                msgDict['content'] = '对话未开始'
            else:
                with open(f'case/{caseHash}/chat/02.txt', 'r', encoding='utf-8') as f:
                    msgDict['content'] = f.read()
                    msgDict['code'] = 1
            yield f'data: {json.dumps(msgDict, ensure_ascii=False)}\n\n'
            return
        
        with self.lock:
            session['sent'] += session['toSend']
            session['toSend'] = ''
            msgDict['content'] = session['sent']
        yield f'data: {json.dumps(msgDict, ensure_ascii=False)}\n\n'

        while not session['complete'].is_set():
            while session['toSend']:
                with self.lock:
                    msgDict['content'] = session['toSend']
                    session['sent'] += session['toSend']
                    session['toSend'] = ''
                yield f'data: {json.dumps(msgDict, ensure_ascii=False)}\n\n'
            time.sleep(0.01)  # 这里就不设置竞争锁了，先实现了想优化了再说
        msgDict['code'] = 1
        msgDict['content'] = session['sent']
        yield f'data: {json.dumps(msgDict, ensure_ascii=False)}\n\n'
        return

    
    def createSession(self, caseHash: str) -> Response:
        with self.lock:
            if caseHash in self.sessions:
                return jsonify({
                    'code': 2,
                    'msg': '案例正在对话中'
                })
            self.sessions[caseHash] = Session()  # fix: 判是否存在和设置案例存在要在一个锁里
        if not os.path.exists(f'case/{caseHash}'):
            return jsonify({
                'code': 1,
                'msg': '案例不存在'
            })
        os.makedirs(f'case/{caseHash}/chat', exist_ok=True)
        config = file.read_config(f'case/{caseHash}/config.json')
        fileName = config['fileName']
        data = file.read_doc_docx_txt(f'case/{caseHash}/{fileName}')
        data = '请结合相关法律对本案进行判决\n\n' + data

        with open(f'case/{caseHash}/chat/01.txt', 'w', encoding='utf-8') as f:
            f.write(data)
        
        message = [
            {
                "role": "user",
                "content": data,
            }
        ]
        threading.Thread(target=self.__chat, args=(caseHash, message, )).start()

        return jsonify({
            'code': 0,
            'msg': '对话创建成功'
        })


    def getStatus(self, caseHash: str) -> Response:
        if caseHash not in self.sessions:
            return jsonify({
                'code': 1,
                'msg': 'case not found'
            })
        with self.lock:
            status = self.sessions[caseHash].session['status']  # 不可变字符串常量不需要拷贝
        return jsonify({
            'code': 0,
            'status': status
        })
    

    def getChatData(self, caseHash: str) -> Response:
        return Response(self.__getChatData(caseHash), mimetype='text/event-stream')
        

chatManager = ChatManager()

