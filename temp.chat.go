/*
 * @Author: LetMeFly
 * @Date: 2025-02-06 16:22:30
 * @LastEditors: LetMeFly.xyz
 * @LastEditTime: 2025-02-12 16:22:29
 */
<button onclick="location.href='https://shy-ds.letmefly.xyz/'" class="endbutton">使用说明</button>
修改为在新页面打开



li标签设置点击时响应


js在新页面打开窗口


HTML设置li鼠标悬浮时显示点击手势


---


美化这个页面，你只需要返回css代码即可

<!--
 * @Author: LetMeFly
 * @Date: 2025-02-07 22:01:23
 * @LastEditors: LetMeFly.xyz
 * @LastEditTime: 2025-02-11 12:16:48
-->
<!DOCTYPE html>
<html>

<head>
    <meta charset="UTF-8">
    <title>LetSHY - 实时对话演示</title>
    <script src="https://letmefly.xyz/Links/Common.js" async></script>
    <script src="/static/js/marked.min.js"></script>
    <style>
        .thinkTag {
            color: #999;
            font-style: italic;
            margin-bottom: 10px;
            margin-top: 10px;
            border: #999 solid 1px;
        }
    </style>
</head>

<body>
    <h2>仅支持一轮对话</h2>
    <div>
        <input type="text" id="input" placeholder="输入你的问题">
        <button onclick="startChat()">发送</button>
        <button onclick="stopChat()">停止</button>
    </div>
    <div id="output" style="white-space: pre-wrap; margin-top: 20px; display: none"></div>
    <div id="markdown"></div>

    <script>
        function stopChat() {
            if (eventSource) eventSource.close();
        }
    </script>

    <script>
        const output = document.getElementById('output');
        const markdown = document.getElementById('markdown');

        function renderMarkdown() {
            const inputText = output.innerHTML;
            const renderedHtml = marked.parse(inputText);
            markdown.innerHTML = renderedHtml;
        }

        const targetNode = document.getElementById('output');

        // 配置观察选项
        const config = {
            childList: true, // 观察子节点的变化
            subtree: true,   // 观察所有后代节点
            characterData: true // 观察文本内容的变化
        };

        // 创建一个回调函数，当观察到变化时执行
        const onOutputModified = function (mutationsList, observer) {
            for (let mutation of mutationsList) {
                if (mutation.type === 'childList' || mutation.type === 'characterData') {
                    // 调用 renderMarkdown 函数
                    renderMarkdown();
                }
            }
        };

        // 创建一个 MutationObserver 实例并传入回调函数
        const observer = new MutationObserver(onOutputModified);

        // 开始观察目标节点
        observer.observe(targetNode, config);
    </script>

    <script>
        let eventSource;

        function startChat() {
            const input = document.getElementById('input').value;
            document.title = 'LetSHY - ' + input || '';
            const output = document.getElementById('output');
            output.innerHTML = '发起请求...';

            // 关闭之前的连接（如果有）
            if (eventSource) eventSource.close();

            // 建立 SSE 连接
            eventSource = new EventSource(`/chat?query=${encodeURIComponent(input)}`);

            eventSource.onopen = () => {
                output.innerHTML = '正在思考...';
            };
            let first = true;
            let ifThink = false;  // 假设如果有think一定是在对话的开始
            let globalDataInFunction = '';
            // 监听数据
            eventSource.onmessage = (event) => {
                globalDataInFunction = event.data;
                try {
                    const data = JSON.parse(event.data);
                    if (first) {
                        output.innerHTML = '';
                        first = false;
                    }
                    const thinkData = data.choices[0].delta.reasoning_content || '';
                    const contentData = data.choices[0].delta.content || '';
                    if (thinkData) {
                        if (ifThink === false) {
                            ifThink = true;
                            const thinkTag = document.createElement('div');
                            thinkTag.setAttribute('class', 'thinkTag');
                            output.appendChild(thinkTag);
                        }
                        const thinkTag = output.querySelector('.thinkTag');
                        thinkTag.innerHTML += thinkData;
                    }
                    if (contentData) {
                        output.innerHTML += contentData;
                    }
                } catch (e) {
                    if (event.data == '[DONE]') {
                        console.log('对话结束')
                        eventSource.close();
                        return;
                    }
                    try {
                        const data = JSON.parse(globalDataInFunction);
                        if (data['error']['message'] == 'concurrency exceeded') {
                            output.innerHTML = '并发过大，超过API提供方限制';
                        }
                        console.log('对话结束')
                        eventSource.close();
                    } catch (e) {
                        console.log(e)
                    }
                }
            };

            eventSource.onerror = (err) => {
                console.error('连接错误:', err);
                eventSource.close();
                output.innerHTML = '连接错误！';
            };
        }
    </script>
</body>

</html>

其中，上一个页面的美化结果如下，你可以进行参考：

body {
	font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
	line-height: 1.6;
	max-width: 1200px;
	margin: 0 auto;
	padding: 20px;
	background-color: #f5f8fa;
	color: #333;
}

h1 {
	color: #2c3e50;
	border-bottom: 3px solid #3498db;
	padding-bottom: 10px;
	margin-bottom: 30px;
}

h2 {
	color: #3498db;
	margin: 25px 0 15px;
}

#uploadForm {
	background: white;
	padding: 25px;
	border-radius: 8px;
	box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
	margin-bottom: 30px;
}

input[type="file"] {
	padding: 8px;
	border: 2px solid #3498db;
	border-radius: 4px;
	margin-right: 10px;
}

button {
	background-color: #3498db;
	color: white;
	padding: 10px 20px;
	border: none;
	border-radius: 5px;
	cursor: pointer;
	transition: background-color 0.3s;
}

button:hover {
	background-color: #2980b9;
}

#fileList {
	background: white;
	padding: 20px;
	border-radius: 8px;
	box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
	list-style-type: none;
}

.file-item {
	padding: 15px;
	margin: 10px 0;
	background-color: #f8f9fa;
	border-radius: 5px;
	display: flex;
	align-items: center;
	justify-content: space-between;
	transition: transform 0.2s;
}

.file-item:hover {
	transform: translateX(5px);
	box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.fileName {
	color: #2c3e50;
	text-decoration: none;
	font-weight: 500;
	transition: color 0.2s;
}

.fileName:hover {
	color: #3498db;
}

pre {
	background-color: #f8f9fa;
	border: 1px solid #e1e4e8;
	border-radius: 6px;
	padding: 20px;
	overflow-x: auto;
}

.endbutton {
	margin-top: 20px;
	font-size: 1.1em;
	padding: 12px 25px;
	float: right;
}

/* 进度文字样式 */
.file-item span {
	color: #7f8c8d;
	font-size: 0.9em;
	font-style: italic;
}

/* 响应式设计 */
@media (max-width: 768px) {
	body {
		padding: 15px;
	}

	.file-item {
		flex-direction: column;
		align-items: flex-start;
	}

	.fileName {
		width: 100%;
		margin-bottom: 8px;
	}
}

#fileList li {
	cursor: pointer;
}