/*
 * @Author: LetMeFly
 * @Date: 2025-02-06 16:22:30
 * @LastEditors: LetMeFly.xyz
 * @LastEditTime: 2025-02-08 13:53:35
 */
我想写一个flask应用，可以让用户上传一些docx或者doc文件，然后flask在后台为这些文件每个建立一个文件夹，并调用DeepSeek的API进行多轮对话，并保存对话进度。
主页可以上传文件、查看每个文件的对话进度（不需要显示具体对话内容，只需要显示“第一轮对话进行中”“第二轮对话已完成”等彩色tag）；点击一个文件可以进入这个文件的对话详情。

具体设计如下：
+ 每个文件及其对话信息、进度等以合理的格式保存到`case/{对应md5}`文件夹
+ 要求流式对话，实时获取对话内容

现在，你只需要将架构、设计、细节、可能会用到的知识等告诉我，不需要具体的代码实现。

---

现在，请给我生成前端html，包括：上传文件（要支持批量上传）、实时显示每个文件的对话进度，以及可以点击每个文件跳转到新页面

注意，请设计如何实时显示每个文件的对话进度。

暂时不需要样式。

---

请实现后端对应的所需功能

---

这是我的前端页面，请你牢记，并等待下一步指令


--


请实现upload接口。

只需要返回flask对应相关函数即可

---

<form id="uploadForm" enctype="multipart/form-data">
<input type="file" name="files" id="files" multiple accept=".docx,.doc">
<button type="submit">上传文件</button>
</form>

这段代码点击上传后会刷新页面吗




---

给我一段python赞美太阳的代码

---

这段代码在控制台会输出：

对话结束
EventSource 加载失败：GET“http://shy.local.letmefly.xyz:4140/chat?query=”。

为什么会输出EventSource 加载失败


{{file}}
---
