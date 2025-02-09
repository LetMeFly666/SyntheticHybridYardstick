/*
 * @Author: LetMeFly
 * @Date: 2025-02-06 16:22:30
 * @LastEditors: LetMeFly.xyz
 * @LastEditTime: 2025-02-09 12:46:47
 */
我想写一个flask应用，可以让用户上传一些docx或者doc文件，然后flask在后台为这些文件每个建立一个文件夹，并调用DeepSeek的API进行多轮对话，并保存对话进度。
主页可以上传文件、查看每个文件的对话进度（不需要显示具体对话内容，只需要显示“第一轮对话进行中”“第二轮对话已完成”等彩色tag）；点击一个文件可以进入这个文件的对话详情。

具体设计如下：
+ 每个文件及其对话信息、进度等以合理的格式保存到`case/{对应md5}`文件夹
+ 要求流式对话，实时获取对话内容

现在，你只需要将架构、设计、细节、可能会用到的知识等告诉我，不需要具体的代码实现。

---

现在，请给我生成单个案例操作的HTML，包括：

显示所有进度、可以执行步骤、可以继续对话等。

流程图如下所示：

graph LR
            classDef process fill:#E5F6FF,stroke:#73A6FF,stroke-width:2px;
        
            A(上传案例文件):::process --> B(DS初步分析):::process
            B --> C(给DS决策树并让它再次分析):::process
            C --> D{纠正DS错误}:::process
            D --> |是| E(纠正错误):::process
            D --> |否| F(生成使用决策树前后的结果对比表):::process
            E --> F

---

flask后端可能同时进行着多个和DeepSeek的流式对话，请实现如下功能：

+ 为前端提供接口/chatData/{chatId}，实时返回对话内容
+ 当和DeepSeek的对话完成时，存储对话内容

前端可以随时访问任意接口，获取对话内容或对话状态。

---

详细解释这段代码

---

请解释python threading.Event()和threading.Lock()

---

python读取doc或docx中的所有文本内容

---

mac上如何读doc

---

pandoc能读docx吗？

如果可以，请告诉我一种在windows和mac上都支持的，简单的可以读doc和docx的方法


---

pandoc读doc为文本

---

doc批量转为docx

---

import pypandoc
text = pypandoc.convert_file('case/d990839b5f6eb9ee8b8ad33b517c0538/Let造案例.doc', 'plain')
print(text)

报错：

Traceback (most recent call last):
  File "F:\OtherApps\Program\Git\Store\Store56_SeekJudgeHybrid\SeekJudgeHybrid\temp.file.py", line 8, in <module>
    text = pypandoc.convert_file('case/d990839b5f6eb9ee8b8ad33b517c0538/Let造案例.doc', 'plain')
  File "F:\OtherApps\Program\Python\Python\lib\site-packages\pypandoc\__init__.py", line 206, in convert_file
    return _convert_input(discovered_source_files, format, 'path', to, extra_args=extra_args,
  File "F:\OtherApps\Program\Python\Python\lib\site-packages\pypandoc\__init__.py", line 371, in _convert_input
    format, to = _validate_formats(format, to, outputfile)
  File "F:\OtherApps\Program\Python\Python\lib\site-packages\pypandoc\__init__.py", line 318, in _validate_formats
    raise RuntimeError(
RuntimeError: Invalid input format! Got "doc" but expected one of these: biblatex, bibtex, commonmark, commonmark_x, creole, csljson, csv, docbook, docx, dokuwiki, endnotexml, epub, fb2, gfm, haddock, html, ipynb, jats, jira, json, latex, man, markdown, markdown_github, markdown_mmd, markdown_phpextra, markdown_strict, mediawiki, muse, native, odt, opml, org, ris, rst, rtf, t2t, textile, tikiwiki, twiki, vimwiki

---

textract转doc为文本

---

import textract


# 示例使用
file_path = "case/d990839b5f6eb9ee8b8ad33b517c0538/Let造案例.doc"
content = textract.process(file_path).decode("utf-8")
print(content)

报错

Traceback (most recent call last):
  File "F:\OtherApps\Program\Python\Python\lib\site-packages\textract\parsers\utils.py", line 87, in run
    pipe = subprocess.Popen(
  File "F:\OtherApps\Program\Python\Python\lib\subprocess.py", line 951, in __init__
    self._execute_child(args, executable, preexec_fn, close_fds,
  File "F:\OtherApps\Program\Python\Python\lib\subprocess.py", line 1420, in _execute_child
    hp, ht, pid, tid = _winapi.CreateProcess(executable, args,
FileNotFoundError: [WinError 2] 系统找不到指定的文件。

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "F:\OtherApps\Program\Git\Store\Store56_SeekJudgeHybrid\SeekJudgeHybrid\temp.file.py", line 16, in <module>
    content = textract.process(file_path).decode("utf-8")
  File "F:\OtherApps\Program\Python\Python\lib\site-packages\textract\parsers\__init__.py", line 79, in process
    return parser.process(filename, input_encoding, output_encoding, **kwargs)
  File "F:\OtherApps\Program\Python\Python\lib\site-packages\textract\parsers\utils.py", line 46, in process
    byte_string = self.extract(filename, **kwargs)
  File "F:\OtherApps\Program\Python\Python\lib\site-packages\textract\parsers\doc_parser.py", line 9, in extract
    stdout, stderr = self.run(['antiword', filename])
  File "F:\OtherApps\Program\Python\Python\lib\site-packages\textract\parsers\utils.py", line 95, in run
    raise exceptions.ShellError(
textract.exceptions.ShellError: The command `antiword case/d990839b5f6eb9ee8b8ad33b517c0538/Let造案例.doc` failed with exit code 127
------------- stdout -------------
------------- stderr -------------

---

使用python-docx将doc转为docx

---

python读doc

---

windows和mac分别安装antiword

---


windows和mac分别安装unoconv

---

我能不能只安装unoconv而不是整个LibreOffice

---

unoconv将doc转为docx
.
---

windows上pip isntall unoconv后，执行unoconv命令，系统提示“选择unoconv的打开方式”

--


python判断是windows还是mac还是linux

---

windows上将doc转为docx，python转

---

import pypandoc
filePath = 'case/bae10f62700cbdfd3b7d7322dc13c947/[无结果版]苏某某、马某甲等婚约财产纠纷民事一审民...(FBM-CLI.C.558409211).docx'
text = pypandoc.convert_file(filePath, 'plain')
print(text)

报错：

Traceback (most recent call last):
  File "F:\OtherApps\Program\Git\Store\Store56_SeekJudgeHybrid\SeekJudgeHybrid\temp.file2.py", line 9, in <module>
    text = pypandoc.convert_file(filePath, 'plain')
  File "F:\OtherApps\Program\Python\Python\lib\site-packages\pypandoc\__init__.py", line 206, in convert_file
    return _convert_input(discovered_source_files, format, 'path', to, extra_args=extra_args,
  File "F:\OtherApps\Program\Python\Python\lib\site-packages\pypandoc\__init__.py", line 387, in _convert_input
    input_file = sorted(input_file)
TypeError: 'WindowsPath' object is not iterable


---


pypandoc将docx转为文本

---

我找到原因了

[无结果版]苏某某、马某甲等婚约财产纠纷民事一审民...(FBM-CLI.C.558409211).docx

这里包含特殊字符了

换成正常的文件名就可以。


如何解决


---

python临时文件

---

python将一个文件复制为临时文件，执行一定操作后，再删除

---

临时文件需要具有rb权限

---

def read_docx(filePath: str) -> str:
    with tempfile.NamedTemporaryFile(mode='w+b', delete=True, suffix='.docx') as f:
        print(f'临时文件路径：{f.name}')
        shutil.copyfile(filePath, f.name)
        text = pypandoc.convert_file(f.name, 'plain')
    return text


报错

Traceback (most recent call last):
  File "F:\OtherApps\Program\Python\Python\lib\site-packages\flask\app.py", line 2213, in __call__
    return self.wsgi_app(environ, start_response)
  File "F:\OtherApps\Program\Python\Python\lib\site-packages\flask\app.py", line 2193, in wsgi_app
    response = self.handle_exception(e)
  File "F:\OtherApps\Program\Python\Python\lib\site-packages\flask\app.py", line 2190, in wsgi_app
    response = self.full_dispatch_request()
  File "F:\OtherApps\Program\Python\Python\lib\site-packages\flask\app.py", line 1486, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "F:\OtherApps\Program\Python\Python\lib\site-packages\flask\app.py", line 1484, in full_dispatch_request
    rv = self.dispatch_request()
  File "F:\OtherApps\Program\Python\Python\lib\site-packages\flask\app.py", line 1469, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
  File "F:\OtherApps\Program\Git\Store\Store56_SeekJudgeHybrid\SeekJudgeHybrid\src\chatStream.py", line 46, in chatStart
    chatManager.createSession(caseHash)
  File "F:\OtherApps\Program\Git\Store\Store56_SeekJudgeHybrid\SeekJudgeHybrid\src\chatStream.py", line 38, in createSession
    data = file.read_doc_docx(f'case/{caseHash}/{fileName}')
  File "F:\OtherApps\Program\Git\Store\Store56_SeekJudgeHybrid\SeekJudgeHybrid\src\file.py", line 52, in read_doc_docx
    return read_docx(filePath)
  File "F:\OtherApps\Program\Git\Store\Store56_SeekJudgeHybrid\SeekJudgeHybrid\src\file.py", line 24, in read_docx
    shutil.copyfile(filePath, f.name)
  File "F:\OtherApps\Program\Python\Python\lib\shutil.py", line 264, in copyfile
    with open(src, 'rb') as fsrc, open(dst, 'wb') as fdst:
PermissionError: [Errno 13] Permission denied: 'C:\\Users\\LetMe\\AppData\\Local\\Temp\\tmpznhotl8d.docx'