/*
 * @Author: LetMeFly
 * @Date: 2025-02-06 16:22:30
 * @LastEditors: LetMeFly.xyz
 * @LastEditTime: 2025-02-08 16:55:21
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


<form id="uploadForm" enctype="multipart/form-data">
	<input type="file" name="files" id="files" multiple accept=".docx,.doc">
	<button type="submit">上传文件</button>
</form>

文件上传成功后，清除form中的文件内容

---

上传案例文件->DS初步分析->给DS决策树并让它再次分析->纠正DS错误（可选）->生成使用决策树前后的结果对比表

将其画成mermaid流程图

---

给出mermaid源码，以及如何将其渲染到HTML上

---


<script src="https://letmefly.xyz/Links/mermaid.min.js.js" async></script>

如何设置在这个js加载完成后开始渲染

---

这段代码有什么错

<pre><code class="mermaid">
graph LR
	classDef process fill:#E5F6FF,stroke:#73A6FF,stroke-width:2px;
	
	A(上传案例文件):::process --> B(DS初步分析):::process
	B --> C(给DS决策树并让它再次分析):::process
	C --> D{纠正DS错误（可选）}:::process
	D --> |是| E(纠正错误):::process
	E --> F(生成使用决策树前后的结果对比表):::process
	D --> |否| F
</code></pre>

---

mermaid中如何加入中文括号（版本10.2.3)

---

不，就是因为括号所以报错了

{str: 'Lexical error on line 6. Unrecognized text.\n...s  …纠正DS错误（可选）}:::process    \n----------------------^', message: 'Lexical error on line 6. Unrecognized text.\n...s  …纠正DS错误（可选）}:::process    \n----------------------^', hash: 'Error', error: Error: Lexical error on line 6. Unrecognized text.
...s    C --> D{纠正DS错误（可选）}:::process    
------…}

如果把（可选）的括号去掉就可以正常渲染了

---

mermaid如何由上到下