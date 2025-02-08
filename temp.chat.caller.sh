###
 # @Author: LetMeFly
 # @Date: 2025-02-08 22:11:29
 # @LastEditors: LetMeFly.xyz
 # @LastEditTime: 2025-02-08 22:30:03
### 
# 启动对话：
curl -X POST http://localhost:5000/start_chat
# 返回 {"chatId": "生成的UUID"}

# 获取实时流式数据：
curl http://localhost:5000/chatData/{chatId}
curl http://localhost:5000/chatData/b8eb5072-72f8-425f-96f2-e3a2f868de54
curl http://localhost:5000/chatData/ee5ac863-ed71-4b02-bf1a-2e46cd6f37a1
curl http://localhost:5000/chatData/748b8389-d88a-4e75-bee9-c548167acdbd

# 查询对话状态：
curl http://localhost:5000/chatStatus/{chatId}
curl http://localhost:5000/chatStatus/b8eb5072-72f8-425f-96f2-e3a2f868de54
curl http://localhost:5000/chatStatus/ee5ac863-ed71-4b02-bf1a-2e46cd6f37a1
curl http://localhost:5000/chatStatus/748b8389-d88a-4e75-bee9-c548167acdbd