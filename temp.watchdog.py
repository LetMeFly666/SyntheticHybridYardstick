'''
Author: LetMeFly
Date: 2025-02-08 14:39:58
LastEditors: LetMeFly.xyz
LastEditTime: 2025-02-08 14:40:03
'''
import time
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

if __name__ == "__main__":
    # 监控的文件夹路径
    path = 'case'
    # 创建事件处理对象
    event_handler = MyEventHandler()
    # 创建观察者对象
    observer = Observer()
    # 安排观察者监控指定路径，并使用指定的事件处理程序
    observer.schedule(event_handler, path, recursive=True)
    # 启动观察者
    observer.start()
    try:
        while True:
            # 让主线程休眠，以保持程序运行
            time.sleep(1)
    except KeyboardInterrupt:
        # 当用户按下 Ctrl+C 时，停止观察者
        observer.stop()
    # 等待观察者线程结束
    observer.join()