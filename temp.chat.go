/*
 * @Author: LetMeFly
 * @Date: 2025-02-06 16:22:30
 * @LastEditors: LetMeFly.xyz
 * @LastEditTime: 2025-02-08 16:14:38
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

python获取当前时间戳

---

html设置最大显示字符数量，多余的用...代替

---

html字典取所有键值

---

<ul id="fileList">
        <!-- 动态生成文件列表 -->
        <!-- <li class="file-item" id="file-{md5}">
            <a href="" class="fileName">[无结果版]苏某某、马某甲等婚约财产纠纷民事一审民...(FBM-CLI.C.558409211).doc</a>
        </li> -->
    <li id="file-c84890ac9e7509d72b12205fef70af68" class="file-item">
		<a href="/detail/c84890ac9e7509d72b12205fef70af68" class="fileName">[无结果版]苏某某、马某甲等婚约财产纠纷民事一审民...(FBM-CLI.C.558409211).doc</a>
		<span>状态: 上传案例文件</span>
	</li><li id="file-d990839b5f6eb9ee8b8ad33b517c0538" class="file-item">
		<a href="/detail/d990839b5f6eb9ee8b8ad33b517c0538" class="fileName">Let造案例.doc</a>
		<span>状态: 上传案例文件</span>
	</li></ul>

html设置最大显示字符数量，多余的用...代替
设置内容为#fileList .file-item a.fileName  对吗