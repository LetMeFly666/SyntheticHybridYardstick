'''
Author: LetMeFly
Date: 2025-02-09 10:33:13
LastEditors: LetMeFly.xyz
LastEditTime: 2025-02-12 17:17:30
'''
import json
import platform
import os
import tempfile
import shutil


"""
docx -> str
临时文件：
    pypandoc支持case/49f19ff403e02cbe63af83d64011dfce/Let造案例.docx
    不支持case/bae10f62700cbdfd3b7d7322dc13c947/[无结果版]苏某某、马某甲等婚约财产纠纷民事一审民...(FBM-CLI.C.558409211).docx
"""
def read_docx(filePath: str) -> str:
    with tempfile.NamedTemporaryFile(mode='w+b', delete=True, suffix='.docx') as f:
        tempFilePath = f.name
        f.close()
        print(f'临时文件路径：{tempFilePath}')
        shutil.copyfile(filePath, tempFilePath)
        import pypandoc
        text = pypandoc.convert_file(tempFilePath, 'plain')
    if os.path.exists(tempFilePath):
        try:
            os.remove(tempFilePath)
        except:
            print('临时文件删除失败')
    return text


"""
doc -> docx
未测试，怕报错的话，上传docx文件吧
"""
def doc2docx(filePath: str):
    if platform.system().lower() == 'windows':
        from win32com import client
        word = client.Dispatch('Word.Application')
        word.Visible = False  # 不显示 Word 界面
        doc = word.Documents.Open(filePath)
        doc.SaveAs(filePath + 'x', FileFormat=16)  # 16 代表 .docx 格式
        doc.Close()
        word.Quit()
    else:
        # 前提是安装了unoconv甚至是libreoffice
        os.system(f'unoconv -f docx {filePath}')


"""doc(x) -> str"""
def read_doc_docx(filePath: str) -> str:
    if filePath.endswith('.doc'):
        doc2docx(filePath)
        filePath = filePath + 'x'
    return read_docx(filePath)


"""doc(x)|txt -> str"""
def read_doc_docx_txt(filePath: str) -> str:
    if filePath.endswith('.doc') or filePath.endswith('.docx'):
        return read_doc_docx(filePath)
    with open(filePath, 'r', encoding='utf-8') as f:
        data = f.read()
    return data
        

"""json -> dict"""
def read_config(filePath: str) -> dict:
    with open(filePath, 'r', encoding='utf-8') as f:
        data = f.read()
    ans = json.loads(data)
    return ans

