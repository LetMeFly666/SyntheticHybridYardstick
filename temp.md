data: {"id":"0194dfac237829626e211efa5e18801f","object":"chat.completion.chunk","created":1738919388,"model":"Qwen/Qwen2.5-Coder-7B-Instruct","choices":[{"index":0,"delta":{"content":"","reasoning_content":null,"role":"assistant"},"finish_reason":null,"content_filter_results":{"hate":{"filtered":false},"self_harm":{"filtered":false},"sexual":{"filtered":false},"violence":{"filtered":false}}}],"system_fingerprint":"","usage":{"prompt_tokens":61,"completion_tokens":0,"total_tokens":61}}
 在 Flask 中启动 SSL 加密可以通过使用 `ssl_context` 参数来实现。以下是一个简单的示例，展示了如何在 Flask 应用中使用自签名的 SSL 证书来启动 HTTPS 服务。

