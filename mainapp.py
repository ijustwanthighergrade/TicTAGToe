from flask import Flask, app, redirect, session, request, jsonify, Response, url_for, abort, Blueprint,render_template
from flask_sqlalchemy import SQLAlchemy
import os,sys
import json
import requests
from bs4 import BeautifulSoup
import lxml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

from model import Mysql
import src,model

url = {
    'fb':'https://www.facebook.com/hashtag/',
    'ig':'...',
    'twitter':'...',

}


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

    return render_template('index.html', result = result, return_dict = return_dict,RelTagName=['test1','test2','test3'])


#抓取FB貼文資訊
@app.route("/info")
def Info():
    socialName = ''
    tagName = ''
    options = Options()
    options.add_argument("--disable-notifications")
    edge = webdriver.Edge('./mesdgedriver', options=options)

    # time.sleep(3)
    edge.get("https://www.facebook.com/hashtag/美食")
    # edge.get(f"{url[socialName]}{tagName}")
    for x in range(1, 4):
        edge.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(6) 
    
    soup = BeautifulSoup(edge.page_source, 'lxml')

    #發文內容
    texts = soup.find_all('div', {'class': 'xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs x126k92a'}) 
    post_text = []

    #發文者名稱
    names = soup.find_all('a', {'class': 'x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xt0b8zv xo1l8bm'})
    post_name = []

    #發文社團
    clubs = soup.find_all('a', {'class': 'x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f'}) 
    post_club = []

    #發文時間
    posts = soup.find_all('div', {'class': 'du4w35lb k4urcfbm l9j0dhe7 sjgh65i0'})
    time_list = []

    



    for text in texts:
        text1 = text.find('div', {'dir': 'auto'})
        if text1:
            post_text.append(text1.string)
            print(text1.string) 
    
    for name in names:
        name1 = name.find('b')
        if name1:
            post_name.append(name1.string)
    
    for club in clubs:
        club1 = club.find('span')
        if club1:
            post_club.append(club.string)

    for post in posts:
        time_tag = post.find('span', {'class': 'a8c37x1j ni8dbmo4 stjgntxs l9j0dhe7'})
        if time_tag:
            post_time = time_tag.find('span', {'class': 'timestampContent'}).string
            time_list.append(post_time)
            print(post_time)



    edge.quit()

    return render_template('info.html', post_text = post_text, post_name = post_name, post_club = post_club, time_list = time_list)
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


