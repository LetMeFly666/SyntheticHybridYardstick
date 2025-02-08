'''
Author: LetMeFly
Date: 2025-02-08 17:27:01
LastEditors: LetMeFly.xyz
LastEditTime: 2025-02-08 17:33:27
'''
from flask import Flask, render_template
import os


# 指定自定义模板文件夹路径
src_dir = os.path.dirname(os.path.abspath(__file__))
# 构建自定义模板文件夹的路径
# template_folder = os.path.join(src_dir, '..', 'static', 'html')
template_folder = os.path.join(os.getcwd(), 'static/html')
print(template_folder)
# app = Flask(__name__, template_folder=template_folder)
app = Flask(__name__)
app.template_folder = os.path.join(os.getcwd(), 'static/html')

@app.route('/')
def index():
    return render_template('oneCase.html')

def main():
    app.run(debug=True)
    
if __name__ == '__main__':
    main()