<!--
 * @Author: LetMeFly
 * @Date: 2025-02-06 08:59:49
 * @LastEditors: LetMeFly.xyz
 * @LastEditTime: 2025-02-11 13:41:25
-->
# SeekJudgeHybrid

让DeepSeek(以下可能简称DS)分别不依据和依据决策树判决一个案例并对比判决结果生成表格

## 流程

### 总述

1. 给DeepSeek一个彩礼纠纷相关的案例让DeepSeek判决应该返还多少彩礼
1. 给DeepSeek一个写好的法律判决决策树（By [shykeke](https://web.letmefly.xyz/He0/shykeke/)）让它重判
1. (Optional)告诉DS哪里判断错误了，需要xx修改
1. 让DeepSeek生成一个使用决策树前后判断结果的对比表格

### 细节

1. 上传案例（doc或docx），自动去重（保存到`case/{文件md5}`下）
1. Python[读案例](#读案例)（docx to text）
2. [调用API](#调api)接口和DS初次对话
3. 调用API接口和DS再次对话
4. 询问是否有需要[修改]()的地方，如果有就不断调用API和DS对话让它修改
5. 调用API和DS对话让它总结使用决策树前后判决结果关系

## 需实现功能

### 读案例

- [ ] python读docx为text。

### 调API

- [ ] 调用API和DS对话（可能需要带上历史记录）

### 界面

#### 修改询问

## 特色

+ `/chat`页面支持流式对话，实时显示大模型响应
+ 案件列表由EventStream更新，仅当`case`文件夹下某`config.json`更新时`增量`发送；某进度新完成时前端实时响应
+ 案例自动去重，重复上传只会覆盖上次文件名
+ 对话进度支持中断重连继续进行

## 不足

+ 不支持删除文件（除非手动删除`case/{md5}`整个文件夹并重启程序）
+ 多个网页端同时访问一个实时对话接口可能会导致每个接口的得到的数据都不完全
+ 设置首页案例进程“progress”接口的队列最大长度，若没有前端消费者则后端队列长度会在config.json变化时不断边长。
