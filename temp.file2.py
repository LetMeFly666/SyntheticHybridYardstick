'''
Author: LetMeFly
Date: 2025-02-09 12:27:38
LastEditors: LetMeFly.xyz
LastEditTime: 2025-02-09 12:38:45
'''
import pypandoc
from urllib.parse import quote

filePath = 'case/bae10f62700cbdfd3b7d7322dc13c947/[无结果版]苏某某、马某甲等婚约财产纠纷民事一审民...(FBM-CLI.C.558409211).docx'
filePath = 'F:\\OtherApps\\Program\\Git\\Store\\Store56_SeekJudgeHybrid\\SeekJudgeHybrid\\case\\bae10f62700cbdfd3b7d7322dc13c947\\[无结果版]苏某某、马某甲等婚约财产纠纷民事一审民...(FBM-CLI.C.558409211).docx'
text = pypandoc.convert_file(quote(filePath), 'plain')
print(text)