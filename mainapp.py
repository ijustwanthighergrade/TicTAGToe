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
    # if request.method == 'GET':
    #     CurrentData = request.args.getlist('')
    
    # if request.method == 'POST':
    #     CurrentData = request.form.getlist('')

    return render_template('index.html', RelTagName=['test1','test2','test3'])


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
        time.sleep(5) 
    
    soup = BeautifulSoup(edge.page_source, 'lxml')

    #獨立貼文
    posts = soup.find_all('div', {'class': 'x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z'})
    post_item = []

    for post in posts:
        #發文者名稱
        name = post.find('a', {'class': 'x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xt0b8zv xo1l8bm'})
        if name is not None:
            name1 = name.find('b')
        else:
            name = post.find('a', {'class':'x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f'})
            if name is not None:
                name1 = name.find('strong').find('span')
            else:
                name = post.find('a', {'class': 'x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f'})
                if name is not None:
                    name1 = name.find('span', {'class', 'xt0psk2'}).find('span')
                else:
                    name1 = " "
        
        if name1 is not None:
            name1 = name1.text
        else:
            continue

        #發文社團
        club = post.find('a', {'class': 'x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f'})
        if club is not None:
            club1 = club.find('span')
        else:
            club1 = " "
        
        if club1 is not None:
            club1 = club1.text

        #發文時間
        timme = post.find('a', {'class': 'x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xt0b8zv xo1l8bm'})
        if timme is not None:
            timme1 = timme.find('span')
        else:
            timme1 = " "

        # if timme1 is not None:
        #     timme1 = timme1.text

        #發文內容
        text = post.find('div', {'class': 'xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs x126k92a'}) 
        text3 = ""
        if text:
            text1 = text.find_all('div', {'dir': 'auto'})
            for text2 in text1:
                text3 += str(text2.text) + "\n"
        else:
            text = " "
        
        if text3 is not None:
            text3 = text3
        else:
            text3 = " "

        #發文hashtag
        hashtag = post.find('div', {'class': 'xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs x126k92a'})
        post_hashtag_collect = []
        hashtag3 = ""
        if hashtag:
            hashtag1 = hashtag.find_all('span')
            for hashtag2 in hashtag1:
                hashtag3 = hashtag2.find('a', {'class': 'x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv x1qq9wsj xo1l8bm'})
                if hashtag3:
                    post_hashtag_collect.append(hashtag3.string)
                else:
                    post_hashtag_collect.append(" ")
        else:
            post_hashtag_collect.append(" ")
        
        #每篇貼文的資訊
        post_detail = {}
        post_detail = {
            "post_name": name1,
            "post_club": club1,
            "post_time": timme1,
            "post_text": text3,
            "post_hashtag": post_hashtag_collect
        }

        print(post_detail)

        #所有貼文的集合
        post_item.append(post_detail)
        
        

    
    # for name in names:
    #     name1 = name.find('b')
    #     if name1:
    #         post_name.append(name1.string)
    
    # for club in clubs:
    #     club1 = club.find('span')
    #     if club1:
    #         post_club.append(club1.string)

    # for timme in times:
    #     time_tag = timme.find('span')
    #     if time_tag:
    #         time_list.append(time_tag.string)
    #         print(time_tag)

    # for hashtag in hashtags:
    #     hashtag1 = hashtag.find_all('span')
    #     post_hashtag_collect = []
    #     for hashtag2 in hashtag1:
    #         hashtag3 = hashtag2.find('a', {'class': 'x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv x1qq9wsj xo1l8bm'})
    #         if hashtag3:
    #             post_hashtag_collect.append(hashtag3.string)
    #             print(post_hashtag_collect)
    #         else:
    #             post_hashtag.append(" ")
    #     post_hashtag.append(post_hashtag_collect)

    

    edge.quit()

    return render_template('info.html', post_item = post_item)
############################## page ##############################


# * ajax return format => oRes = {'res':'success or fail', 'data':[], 'msg':'error only'}
# * ajax return example => return jsonify(**oRes)
############################## ajax ##############################
@app.route("/testajax",methods=['GET','POST'])
def TestAjax():
    if request.method == 'GET':
        CurrentData = request.args.getlist('test')
    
    if request.method == 'POST':
        CurrentData = request.form.getlist('test')
    print(CurrentData)
    return jsonify(**{'data':CurrentData})

############################## ajax ##############################


if __name__ == '__main__':
    app.run('0.0.0.0',port=8080,debug=True)


# 程式結束時釋放資料庫資源
cursor.close()
db.close()  # 關閉連線


