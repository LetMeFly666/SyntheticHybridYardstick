'''
Author: LetMeFly
Date: 2025-02-08 17:21:20
LastEditors: LetMeFly.xyz
LastEditTime: 2025-02-08 17:24:59
'''
from flask import Flask, render_template

# 指定自定义模板文件夹路径
app = Flask(__name__, template_folder='static/html')

@app.route('/')
def index():
    return render_template('oneCase.html')

if __name__ == '__main__':
    app.run(debug=True)