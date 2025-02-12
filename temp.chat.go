/*
 * @Author: LetMeFly
 * @Date: 2025-02-06 16:22:30
 * @LastEditors: LetMeFly.xyz
 * @LastEditTime: 2025-02-12 16:52:43
 */
github支持mermaid的渲染吗

---

github pages如何自定义header或style

---

github pages在渲染markdown时引入js文件

---

压缩这段代码为一行

<script name="renderMermaid">
        function renderMermaid() {
            // 创建 script 元素
            const script = document.createElement('script');
            // 设置脚本的 src 属性
            script.src = 'https://letmefly.xyz/Links/mermaid.min.js';
            // 监听脚本的 load 事件
            script.onload = function () {
                // 脚本加载完成后，初始化 Mermaid 并渲染图表
                mermaid.initialize({ startOnLoad: false });
                mermaid.run({
                    querySelector: '.mermaid'
                });
            };
            // 监听脚本的 error 事件，处理加载失败的情况
            script.onerror = function () {
                console.error('Mermaid 脚本加载失败');
            };
            // 将脚本添加到文档的 head 中
            document.head.appendChild(script);
        }

        setTimeout(() => {
            renderMermaid();
        }, 10);
    </script>