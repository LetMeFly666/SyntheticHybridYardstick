'''
Author: LetMeFly
Date: 2025-02-09 12:40:29
LastEditors: LetMeFly.xyz
LastEditTime: 2025-02-09 12:40:29
'''
import pypandoc
filePath = 'case/49f19ff403e02cbe63af83d64011dfce/Let造案例.docx'
text = pypandoc.convert_file(filePath, 'plain')
print(text)