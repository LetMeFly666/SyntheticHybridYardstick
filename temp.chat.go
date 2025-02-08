/*
 * @Author: LetMeFly
 * @Date: 2025-02-06 16:22:30
 * @LastEditors: LetMeFly.xyz
 * @LastEditTime: 2025-02-08 13:22:21
 */
HTML实时将id为output的div中的内容渲染为markdown

---

flask返回js

---

@app.route('/static/js/<path:filename>')
def js(filename):
    print(filename)
    return send_from_directory('/static/js', filename)

我想使用这个函数手动返回，以便更多自定义控制

---

flask的send_from_directory不是从项目根路径开始的吗？
而是从app的路径开始的吗

---

使用marked.min.js实时渲染html为markdown

---

当<div id="output"></div>中内容发生变化时调用renderMarkdown函数

---

使用marked.min.js实时渲染

---

我想写一个flask应用，可以让用户上传一些docx或者doc文件，然后flask在后台为这些文件每个建立一个文件夹，并调用DeepSeek的API进行多轮对话，并保存对话进度。
主页可以上传文件、查看每个文件的对话进度（不需要显示具体对话内容，只需要显示“第一轮对话进行中”“第二轮对话已完成”等彩色tag）；点击一个文件可以进入这个文件的对话详情。

具体设计如下：
+ 每个文件及其对话信息、进度等以合理的格式保存到`case/{对应md5}`文件夹
+ 要求流式对话，实时获取对话内容

现在，你只需要将架构、设计、细节、可能会用到的知识等告诉我，不需要具体的代码实现。