'''
Author: LetMeFly
Date: 2025-02-07 13:18:12
LastEditors: LetMeFly.xyz
LastEditTime: 2025-02-07 16:15:47
'''
import qianfan

import os
os.environ["QIANFAN_AK"] = "xvxxxxxx"
os.environ["QIANFAN_SK"] = "bce-v3/xxfsfsdfsf/ssfsfsfsfsfsfsfsfsfs"


import requests
import json


def main():
        
    url = "https://qianfan.baidubce.com/v2/chat/completions"
    
    payload = json.dumps({
        "model": "deepseek-r1",
        "messages": [
            {
                "role": "user",
                "content": "您好"
            }
        ],
        "disable_search": False,
        "enable_citation": False
    }, ensure_ascii=False)
    headers = {
        'Content-Type': 'application/json',
        'appid': '',
        'Authorization': 'Bearer '
    }
    
    response = requests.request("POST", url, headers=headers, data=payload.encode("utf-8"))
    
    print(response.text)
    

if __name__ == '__main__':
    main()
