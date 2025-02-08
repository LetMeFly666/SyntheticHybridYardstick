'''
Author: LetMeFly
Date: 2025-02-08 13:00:34
LastEditors: LetMeFly.xyz
LastEditTime: 2025-02-08 13:04:42
'''
import os
from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/static/js/<path:filename>')
def js(filename):
    static_js_path = os.path.join(app.root_path, 'static', 'js')
    print(f"Looking for file: {filename} in directory: {static_js_path}")  # 调试输出
    return send_from_directory(static_js_path, filename)

if __name__ == '__main__':
    app.run(debug=True)