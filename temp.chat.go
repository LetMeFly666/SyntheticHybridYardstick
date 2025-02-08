/*
 * @Author: LetMeFly
 * @Date: 2025-02-06 16:22:30
 * @LastEditors: LetMeFly.xyz
 * @LastEditTime: 2025-02-08 14:50:15
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

--


请实现progress接口。progress接口的作用是：

监听case文件夹的文件变化，获取每个案例的对话进度（从文件夹下config.json获取），并返回给前端

只需要返回flask对应相关代码即可


---

注意前端const eventSource = new EventSource('/progress');
后端不应一次返回吧

---

很棒！能否做到当watchdog发现有文件更新时再返回

---

请详细介绍js的EventSource，

---

是否会有长时间数据不更新的自动断开机制

---

python watchdog实现一个功能：

文件夹`case`下任何文件发生变化时，调用hello函数

---

flask结束时，停止watchdog

---


browser_thread = threading.Thread(target=open_browser)
browser_thread.start()
run_flask()
browser_thread.join()

这样会导致watchdog在一开始时就被销毁，如何解决