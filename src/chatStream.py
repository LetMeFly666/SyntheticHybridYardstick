'''
Author: LetMeFly
Date: 2025-02-09 10:18:43
LastEditors: LetMeFly.xyz
LastEditTime: 2025-02-09 12:26:20
'''
from flask import Flask, Response, jsonify, abort
import threading
from uuid import uuid4
import time
from collections import deque
from typing import Dict
from src import file
import os


app = Flask(__name__)

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
    
    def createSession(self, caseHash: str):
        if not os.path.exists(f'case/{caseHash}'):
            abort(404)
        config = file.read_config(f'case/{caseHash}/config.json')
        fileName = config['fileName']
        data = file.read_doc_docx(f'case/{caseHash}/{fileName}')
        print(data)

chatManager = ChatManager()


@app.route('/chatStart/<string:caseHash>')
def chatStart(caseHash):
    chatManager.createSession(caseHash)


def run():
    app.run(debug=True)
    