/*
 * @Author: LetMeFly
 * @Date: 2025-02-06 16:22:30
 * @LastEditors: LetMeFly.xyz
 * @LastEditTime: 2025-02-09 16:38:18
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

python创建文件夹，存在时不报错

---

编写一段python赞美太阳的代码

---

HTML为.thinkTag加一个边框