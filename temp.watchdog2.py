'''
Author: LetMeFly
Date: 2025-02-08 14:48:06
LastEditors: LetMeFly.xyz
LastEditTime: 2025-02-08 14:48:06
'''
import time
from flask import Flask
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 定义 hello 函数
def hello():
    print("Hello! 文件发生了变化。")

# 定义事件处理类
class MyEventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        # 当任何文件系统事件发生时调用 hello 函数
        hello()

# 创建 Flask 应用
app = Flask(__name__)

# 创建观察者对象和事件处理对象
observer = Observer()
event_handler = MyEventHandler()
# 监控的文件夹路径
path = 'case'
# 安排观察者监控指定路径，并使用指定的事件处理程序
observer.schedule(event_handler, path, recursive=True)
# 启动观察者
observer.start()

# 定义一个路由，用于测试 Flask 应用
@app.route('/')
def index():
    return 'Hello, World!'

# 定义一个函数，在应用上下文销毁时停止观察者
@app.teardown_appcontext
def stop_observer(exception=None):
    if observer.is_alive():
        observer.stop()
        observer.join()

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except KeyboardInterrupt:
        if observer.is_alive():
            observer.stop()
            observer.join()