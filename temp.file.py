'''
Author: LetMeFly
Date: 2025-02-09 11:04:28
LastEditors: LetMeFly.xyz
LastEditTime: 2025-02-09 11:21:22
'''
# import pypandoc
# text = pypandoc.convert_file('case/d990839b5f6eb9ee8b8ad33b517c0538/Let造案例.doc', 'plain')
# print(text)

import textract


# 示例使用
file_path = "case/d990839b5f6eb9ee8b8ad33b517c0538/Let造案例.doc"
content = textract.process(file_path).decode("utf-8")
print(content)