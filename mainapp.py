from flask import Flask, app, redirect, session, request, jsonify, Response, url_for, abort, Blueprint,render_template
from flask_sqlalchemy import SQLAlchemy
import os,sys

import src,model


#主程式初始化
app = model.app

#初始化功能模組
tools_CommonTools = src.CommonTools.CommonTools()


# 首頁
@app.route("/")
def Index():
    
    return render_template('index.html')


if __name__ == '__main__':
    app.run('0.0.0.0',port=8080,debug=True)