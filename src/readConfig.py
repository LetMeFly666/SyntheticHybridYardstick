'''
Author: LetMeFly
Date: 2025-02-08 15:10:19
LastEditors: LetMeFly.xyz
LastEditTime: 2025-02-09 21:09:04
'''
import os
import json


def read1config(filePath: str) -> dict:
    with open(filePath, 'r', encoding='utf-8') as f:
        config: dict = json.loads(f.read())
        # print(config)
        # 假设 config.json 中有一个 "progress" 字段表示对话进度
    return {
        'fileName': config['fileName'],
        'progress': config['progress'],
        'md5': config['md5'],
        'created': config['created'],
        'modified': config['modified'],
    }


def readAllConfig() -> dict:
    ans = {}
    for fileHash in os.listdir('case'):
        if len(fileHash) != 32:
            continue
        if not os.path.isdir(f'case/{fileHash}'):
            continue
        ans[fileHash] = read1config(f'case/{fileHash}/config.json')
    return ans


# 增量更新，返回是否更新
def updateChangedDict(caseProgress: dict, event) -> bool:
    print(event.is_directory)
    if event.is_directory:
        return False
    filePath: str = event.src_path
    if not filePath.endswith('config.json'):
        return False
    fileHash = os.path.basename(os.path.dirname(filePath))
    try:
        caseProgress[fileHash] = read1config(filePath)
        print(f'config changed: {filePath}')
        return True
    except Exception as e:
        print(f"Error reading {filePath}: {e}")
        return False


if __name__ == '__main__':
    config = readAllConfig()
    print(config)
