'''
Author: LetMeFly
Date: 2025-02-09 10:18:43
LastEditors: LetMeFly.xyz
LastEditTime: 2025-02-09 19:57:55
'''
from flask import Flask, Response, jsonify, abort
import threading
from uuid import uuid4
import time
from collections import deque
from typing import Dict
from src import file
from src import chat
import os
import requests
import json


class Session:
    def __init__(self) -> None:
        self.session = {
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
            session['complete'].set()
    
    
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
            print('*' * 100)
            print('*' + data + '*')  # debug
            print('*' * 100)
            data = json.loads(data)
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
            
    
    def createSession(self, caseHash: str) -> Response:
        with self.lock:
            print(caseHash)
            print(self.sessions)
            print(caseHash in self.sessions)
            if caseHash in self.sessions:
                print('return 2' * 30)
                return jsonify({
                    'code': 2,
                    'msg': '案例已存在'
                })
            self.sessions[caseHash] = Session()  # fix: 判是否存在和设置案例存在要在一个锁里
        with open('runtime', 'a') as f:
            f.write(f'start {caseHash}\n')
        if not os.path.exists(f'case/{caseHash}'):
            return jsonify({
                'code': 1,
                'msg': '案例不存在'
            })
        os.makedirs(f'case/{caseHash}/chat', exist_ok=True)
        config = file.read_config(f'case/{caseHash}/config.json')
        fileName = config['fileName']
        data = file.read_doc_docx(f'case/{caseHash}/{fileName}')
        data = '请结合相关法律对本案进行判决\n\n' + data
        message = [
            {
                "role": "user",
                "content": data,
            }
        ]
        threading.Thread(target=self.__chat, args=(caseHash, message, )).start()

        return jsonify({
            'code': 0,
            'msg': '创建成功'
        })


    def getStatus(self, caseHash: str) -> Response:
        if caseHash not in self.sessions:
            return jsonify({
                'code': 1,
                'msg': 'case not found'
            })
        with self.lock:
            status = f'{self.sessions[caseHash].session["status"]}'  # 复制一份儿
        return jsonify({
            'code': 0,
            'status': status
        })
        

chatManager = ChatManager()

