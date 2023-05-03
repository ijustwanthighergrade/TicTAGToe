from flask import Flask, app, redirect, session, request, jsonify, Response, url_for, abort, Blueprint,render_template
from flask_sqlalchemy import SQLAlchemy
import os,sys
import json
from model import Mysql

import src,model


#主程式初始化
app = Flask(__name__,static_url_path ='/static/')

#初始化功能模組
tools_CommonTools = src.CommonTools.CommonTools()

# 呼叫 Mysql() 函式以獲取 db 變數
db, cursor = Mysql()
cursor = db.cursor()


# select test
def select_city(cityid, cityname):
    # mysql語句
    select_user_sql = 'select * from city where ID="%s" and Name="%s";' % (cityid, cityname)
    # 執行mysql語句
    result = cursor.execute(select_user_sql)
    db.commit()
    # 如果返回了一條資料，則登入成功，否則登入失敗
    if 1 == result:
        result = True
    else:
        result = False
        print('there is no user where userid="%s and password="%s"!!' % (cityid, cityname))
    return result


############################## page ##############################
# 首頁
@app.route("/")
def Index():
    cityid = 1
    cityname = "Kabul"

    data = request.get_data()

    result = select_city(cityid = cityid, cityname = cityname)
    if not result:
        print('city where cityid="%s and cityname="%s" found!!' % (cityid, cityname))
    
    return_dict = {'success': result}

    return render_template('index.html', result = result, return_dict = return_dict)
############################## page ##############################


# * ajax return format => oRes = {'res':'success or fail', 'data':[], 'msg':'error only'}
# * ajax return example => return jsonify(**oRes)
############################## ajax ##############################

############################## ajax ##############################


if __name__ == '__main__':
    app.run('0.0.0.0',port=8080,debug=True)


# 程式結束時釋放資料庫資源
cursor.close()
db.close()  # 關閉連線


