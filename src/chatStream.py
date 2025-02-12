'''
Author: LetMeFly
Date: 2025-02-09 10:18:43
LastEditors: LetMeFly.xyz
LastEditTime: 2025-02-12 14:22:45
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
    step: int


class Session:
    def __init__(self, step: int) -> None:
        self.session: SessionDict = {
            'status': 'processing',
            'complete': threading.Event(),
            'toSend':'',
            'sent': '',
            'step': step,
        }

class ChatManager:
    def __init__(self) -> None:
        self.sessions: Dict[str, Session] = {}
        self.lock = threading.Lock()

    
    def __addMessage(self, chatId: str, content: str) -> None:
        with self.lock:
            self.sessions[chatId].session['toSend'] += content


    def __completeChat(self, caseHash: str, step: int) -> None:
        if step == 2:
            writeFile = '02.txt'
            stepName = 'DS初步分析'
        elif step == 3:
            writeFile = '04.txt'
            stepName = '给DS决策树并让它再次分析'
        elif step == 4:
            writeFile = '06.txt'
            stepName = '纠正DS错误'
        
        with self.lock:
            session = self.sessions[caseHash].session
            session['status'] = 'completed'
            data = session['sent'] + session['toSend']
            with open(f'case/{caseHash}/chat/{writeFile}', 'w', encoding='utf-8') as f:
                f.write(data)
            config = file.read_config(f'case/{caseHash}/config.json')
            config['progress']['now'] = stepName
            config['progress']['history'].append(stepName)
            config['modified'] = time.time()
            with open(f'case/{caseHash}/config.json', 'w', encoding='utf-8') as f:
                f.write(json.dumps(config, ensure_ascii=False))
            session['complete'].set()
        time.sleep(1)  # 防止前端数据未读取完毕
        with self.lock:
            self.sessions.pop(caseHash)
    
    
    def __chat(self, caseHash: str, chatData: list, step: int) -> None:
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
        self.__completeChat(caseHash, step)
    

    def __getChatData(self, caseHash: str, step: int) -> Generator:
        msgDict = {
            'code': 0,
            'content': '',
        }
        notInMem = False
        session: SessionDict
        with self.lock:
            if caseHash not in self.sessions or self.sessions[caseHash].session['step'] != step:
                notInMem = True
            else:
                session = self.sessions[caseHash].session
        if notInMem:
            fileName = ''
            if step == 2:
                fileName = '02.txt'
            elif step == 3:
                fileName = '04.txt'
            elif step == 4:
                fileName = '06.txt'
            print('not in mem')
            if not os.path.exists(f'case/{caseHash}/chat/{fileName}'):
                msgDict['code'] = 2
                msgDict['content'] = '对话未开始'
            else:
                with open(f'case/{caseHash}/chat/{fileName}', 'r', encoding='utf-8') as f:
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

    
    def createSession(self, caseHash: str, step: int) -> Response:
        with self.lock:
            if caseHash in self.sessions:
                return jsonify({
                    'code': 2,
                    'msg': '案例正在对话中'
                })
            self.sessions[caseHash] = Session(step)  # fix: 判是否存在和设置案例存在要在一个锁里
        if not os.path.exists(f'case/{caseHash}'):
            return jsonify({
                'code': 1,
                'msg': '案例不存在'
            })
        os.makedirs(f'case/{caseHash}/chat', exist_ok=True)
        config = file.read_config(f'case/{caseHash}/config.json')
        fileName = config['fileName']
        data = file.read_doc_docx_txt(f'case/{caseHash}/{fileName}')

        if step == 2:
            data = '请结合相关法律对本案进行判决\n\n' + data
            with open(f'case/{caseHash}/chat/01.txt', 'w', encoding='utf-8') as f:
                f.write(data)
            message = [
                {
                    'role': 'user',
                    'content': data,
                }
            ]
        elif step == 3:
            data = '请根据这个决策树进行判决：\n'+\
                'A[是否登记结婚]-->|是|B[是否满足离婚条件?];\n' +\
                'A-->|否|F[是否共同生活?];\n' +\
                'B -->|否|C[不返还彩礼];\n' +\
                'B -->|是|E[是否共同生活?];\n' +\
                'B -->|是 |[婚前给付是否困难?];\n' +\
                'F-->|是|G[结合彩礼实际使用、嫁妆情况、双方过错、当地习俗决定是否返还彩礼];\n' +\
                'F-->|否|H[全部返还彩礼];\n' +\
                'E -->|是|I[共同生活时间是否较短];\n' +\
                'I-->|是|K[彩礼数额是否过高];\n' +\
                'K -->|是|G;\n' +\
                'I-->|否|C;\n' +\
                'K -->|否|C;\n' +\
                'J-->|是|H;\n' +\
                'J-->|否|C;\n'
            with open(f'case/{caseHash}/chat/03.txt', 'w', encoding='utf-8') as f:
                f.write(data)
            message = [
                {
                    'role': 'user',
                    'content': open(f'case/{caseHash}/chat/01.txt', 'r', encoding='utf-8').read(),
                },
                {
                    'role': 'assistant',
                    'content': open(f'case/{caseHash}/chat/02.txt', 'r', encoding='utf-8').read(),
                },
                {
                    'role': 'user',
                    'content': data,
                }
            ]
        elif step == 4:
            data = '原案件中的婚姻登记状况错误，请将婚姻登记更改成相反的状况（即已登记改为未登记，未登记改为已登记），并根据修改后的案件情况进行重新判决'
            with open(f'case/{caseHash}/chat/05.txt', 'w', encoding='utf-8') as f:
                f.write(data)
            message = [
                {
                    'role': 'user',
                    'content': open(f'case/{caseHash}/chat/01.txt', 'r', encoding='utf-8').read(),
                },
                {
                    'role': 'assistant',
                    'content': open(f'case/{caseHash}/chat/02.txt', 'r', encoding='utf-8').read(),
                },
                {
                    'role': 'user',
                    'content': open(f'case/{caseHash}/chat/03.txt', 'r', encoding='utf-8').read(),
                },
                {
                    'role': 'assistant',
                    'content': open(f'case/{caseHash}/chat/04.txt', 'r', encoding='utf-8').read(),
                },
                {
                    'role': 'user',
                    'content': data
                },
            ]
        
        threading.Thread(target=self.__chat, args=(caseHash, message, step, )).start()

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
    

    def getChatData(self, caseHash: str, step: int) -> Response:
        return Response(self.__getChatData(caseHash, step), mimetype='text/event-stream')
    

    "不需要第4步的修改"
    def noNeed4(self, caseHash: str) -> Response:
        config = file.read_config(f'case/{caseHash}/config.json')
        config['progress']['now'] = '纠正DS错误'
        config['progress']['history'].append('纠正DS错误')
        config['progress']['step4'] = 'skip'
        config['modified'] = time.time()
        with open(f'case/{caseHash}/config.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(config, ensure_ascii=False))
        return jsonify({
            'code': 0,
            'msg': '第4步已跳过',
        })
    

    def ifhad4(self, caseHash: str) -> Response:
        if os.path.exists(f'case/{caseHash}/chat/06.txt'):
            return jsonify({
                'code': 0,
                'msg': '进行过step4'
            })
        with self.lock:
            if caseHash in self.sessions and self.sessions[caseHash].session['step'] == 4:
                return jsonify({
                    'code': 0,
                    'msg': '正在进行step4'
                })
        config = file.read_config(f'case/{caseHash}/config.json')
        if config['progress'].get('step4', '') == 'skip':
            return jsonify({
                'code': 1,
                'msg': '跳过step4'
            })
        return jsonify({
            'code': 2,
            'msg': '未进行过step4'
        })

chatManager = ChatManager()

