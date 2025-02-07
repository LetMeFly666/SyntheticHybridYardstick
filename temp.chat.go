/*
 * @Author: LetMeFly
 * @Date: 2025-02-06 16:22:30
 * @LastEditors: LetMeFly.xyz
 * @LastEditTime: 2025-02-07 22:46:12
 */
flask运行时如何启动浏览器的对应页面

---
flask运行时如何启动浏览器？如果是以下代码则第二行不会被执行，直到程序终止
app.run(host='shy.local.letmefly.xyz', port=4140, debug=True)
webbrowser.open('http://shy.local.letmefly.xyz:4140')

python的threading等两个线程都结束再结束

---
def run_flask():
    app.run(host='shy.local.letmefly.xyz', port=4140, debug=True)

def open_browser():
    webbrowser.open('http://shy.local.letmefly.xyz:4140')

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    time.sleep(1.5)
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.start()
    flask_thread.join()
    browser_thread.join()

这段代码报错

Exception in thread Thread-1:
Traceback (most recent call last):
  File "F:\OtherApps\Program\Python\Python\lib\threading.py", line 954, in _bootstrap_inner
    self.run()
  File "F:\OtherApps\Program\Python\Python\lib\threading.py", line 892, in run
    self._target(*self._args, **self._kwargs)
  File "F:\OtherApps\Program\Git\Store\Store56_SeekJudgeHybrid\SeekJudgeHybrid\server.py", line 63, in run_flask
    app.run(host='shy.local.letmefly.xyz', port=4140, debug=True)
  File "F:\OtherApps\Program\Python\Python\lib\site-packages\flask\app.py", line 889, in run
    run_simple(t.cast(str, host), port, self, **options)
  File "F:\OtherApps\Program\Python\Python\lib\site-packages\werkzeug\serving.py", line 1097, in run_simple
    run_with_reloader(
  File "F:\OtherApps\Program\Python\Python\lib\site-packages\werkzeug\_reloader.py", line 439, in run_with_reloader
    signal.signal(signal.SIGTERM, lambda *args: sys.exit(0))
  File "F:\OtherApps\Program\Python\Python\lib\signal.py", line 47, in signal
    handler = _signal.signal(_enum_to_int(signalnum), _enum_to_int(handler))
ValueError: signal only works in main thread of the main interpreter


---

请解释：browser_thread.join()

---

解释python threading的join