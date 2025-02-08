###
 # @Author: LetMeFly
 # @Date: 2025-02-08 22:26:26
 # @LastEditors: LetMeFly.xyz
 # @LastEditTime: 2025-02-08 22:26:42
###
# 启动对话：
curl -X POST http://localhost:5000/start_chat
# 返回 {"chatId": "生成的UUID"}

# 获取实时流式数据：
curl http://localhost:5000/chatData/{chatId}
curl http://localhost:5000/chatData/a433a090-3aa0-4e4e-b281-71c0c80c7f90
curl http://localhost:5000/chatData/37ba325a-3f20-4894-bb1e-baa2d87a7f7e
curl http://localhost:5000/chatData/1d748b24-0876-4913-ba80-1e9ca0200154

# 查询对话状态：
curl http://localhost:5000/chatStatus/{chatId}
curl http://localhost:5000/chatStatus/a433a090-3aa0-4e4e-b281-71c0c80c7f90
curl http://localhost:5000/chatStatus/37ba325a-3f20-4894-bb1e-baa2d87a7f7e
curl http://localhost:5000/chatStatus/1d748b24-0876-4913-ba80-1e9ca0200154