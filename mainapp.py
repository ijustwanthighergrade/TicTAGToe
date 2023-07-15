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
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.edge.service import Service

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

tagName = ""

############################## function ##############################
#獲取爬蟲抓下的貼文內，所有相關的hashtag集合
def extract_hashtags(content):
    hashtags = re.findall(r'#(\w+)', content)
    return hashtags
############################## function ##############################

############################## page ##############################
# 首頁
@app.route("/", methods=['POST', 'GET'])
def Index():
    return render_template('index.html')


# 搜尋結果頁面
@app.route("/searchres", methods=['GET'])
def SearchRes():
    # 取得傳回的參數，此參數需傳回至前端
    # 撈取知識地圖資料，並傳回前端
    key = request.args.get('keyword') or ''
    tagName = str(key)
    nodeData = []
    linkData = []
    # tagName = "CYIM"
    sql = 'select * from hashtag where TagName = "%s";' % (tagName)
    cursor.execute(sql)
    result = cursor.fetchone()
    if result is not None:
        tagId = result[0]
        category1 = result[2]
        description1 = result[5]
        category3 = ""

        if category1 == 1:
            category3 = "people"
        elif category1 == 2:
            category3 = "place"
        elif category1 == 3:
            category3 = "obj"
        elif category1 == 4:
            category3 = "tag"
        else:
            category3 = "post"

        node1 = {
            "key": tagId,
            "category": category3,
            "text": tagName,
            "description": description1,
            "type": category3
        }
        nodeData.append(node1)
                
        sql = 'select * from hashtag_relationship where TagId = "%s";' % (tagId)
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            objId = row[1]
            relationshipType = row[2]
            if relationshipType == 1:
                sql = 'select * from img_target where TargetId = "%s";' % (objId)
                cursor.execute(sql)
                result1 = cursor.fetchone()
                targetName = result1[2]
                category2 = result1[3]
                description2 = result1[4]
                imgPath = result1[6]
                category4 = ""

                if category2 == 1:
                    category4 = "people"
                elif category2 == 2:
                    category4 = "place"
                elif category2 == 3:
                    category4 = "obj"
                elif category2 == 4:
                    category4 = "tag"
                else:
                    category4 = "post"

                node2 = {
                    "key": objId,
                    "category": category4,
                    "text": targetName,
                    "description": description2,
                    "type": category4,
                    "imgPath": imgPath
                }
                link = {
                    "from": tagId,
                    "to": objId
                }
                nodeData.append(node2)
            else:
                sql = 'select * from post where DataId = "%s";' % (objId)
                cursor.execute(sql)
                result1 = cursor.fetchone()
                postType = result1[2]
                postType1 = ""

                if postType == 1:
                    postType1 = "people"
                elif postType == 2:
                    postType1 = "place"
                elif postType == 3:
                    postType1 = "obj"
                elif postType == 4:
                    postType1 = "tag"
                else:
                    postType1 = "post"

                node2 = {
                    "key": objId,
                    "category": postType1,
                    "text": objId,
                    "description": objId,
                    "type": postType1
                }
                link = {
                    "from": tagId,
                    "to": objId
                }
                nodeData.append(node2)
                linkData.append(link)
            
            sql = 'select * from hashtag_relationship where ObjId = "%s";' % (objId)
            cursor.execute(sql)
            result2 = cursor.fetchall()
            for row1 in result2:
                tagId1 = row1[0]
                sql = 'select * from hashtag where TagId = "%s";' % (tagId1)
                cursor.execute(sql)
                result3 = cursor.fetchone()
                tagName1 = result3[1]
                category5 = result3[2]
                description3 = result3[5]

                if category5 == 1:
                    category6 = "people"
                elif category5 == 2:
                    category6 = "place"
                elif category5 == 3:
                    category6 = "obj"
                elif category5 == 4:
                    category6 = "tag"
                else:
                    category6 = "post"

                node3 = {
                    "key": tagId1,
                    "category": category6,
                    "text": tagName1,
                    "description": description3,
                    "type": category6
                }
                link1 = {
                    "from": objId,
                    "to": tagId1
                }
                nodeData.append(node3)
                linkData.append(link1)

        nodeData = [x for i, x in enumerate(nodeData) if x not in nodeData[:i]]
        linkData = [x for i, x in enumerate(linkData) if x not in linkData[:i]]

        print(nodeData)
        print(linkData)
    else:
        print(f"資料庫之中並沒有#{tagName}這個hashtag!!")

    return render_template('search.html', nodeData = nodeData, linkData = linkData,Keyword=key)


# 個人頁面
@app.route("/individual", methods=['POST', 'GET'])
def Individual():
    # 利用session 取得會員Id

    # 利用會員Id取得會員資料，並傳送至前端

    return render_template('individual.html')
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


#搜尋FB貼文頁面
@app.route("/search_FB", methods=['POST'])
def search_FB():
    post_item = [] 
    if request.method == 'POST':
        key = request.form['keyword']
        page = request.form.get('page') or 1
        page = int(page)
        socialName = "https://www.facebook.com/hashtag/"
        tagName = str(key)
        url = socialName + tagName

        options = Options()
        options.add_argument("--disable-notifications")
        # edge = webdriver.Edge('./mesdgedriver', options=options)
        # 創建Edge服務物件，指定驅動程式的路徑
        service = Service('./mesdgedriver')
        # 創建Edge瀏覽器物件，傳入選項和服務物件
        edge = webdriver.Edge(service=service, options=options)
        edge.get("https://www.facebook.com/")
    
        email = edge.find_element(By.ID, "email")
        password = edge.find_element(By.ID, "pass")
        
        email.send_keys('ebo68885@omeie.com')
        password.send_keys('zxcvb12345')
        password.submit()

        time.sleep(4)
        edge.get(url)
        # edge.get(f"{url[socialName]}{tagName}")
        time.sleep(4)
        time1 = 0
        for x in range(page*3):
            edge.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            if x < (page-1) * 3:
                continue
            else:
                time.sleep(4) 
        
        soup = BeautifulSoup(edge.page_source, 'lxml')

        #獨立貼文
        posts = soup.find_all('div', {'class': 'x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z'})
        post_item = []

        for post in posts:
            #發文者頭貼
            image = post.find('image')
            if image is not None:
                image1 = image.get('xlink:href')
            else:
                image1 = " "

            #發文者名稱
            name = post.find('a', {'class': 'x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xt0b8zv xo1l8bm'})
            print(name)
            if name:
                name1 = name.find('span')
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
            
            print(name1)

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
            timme = post.find('span', {'class': 'x4k7w5x x1h91t0o x1h9r5lt x1jfb8zj xv2umb2 x1beo9mf xaigb6o x12ejxvf x3igimt xarpa2k xedcshv x1lytzrv x1t2pt76 x7ja8zs x1qrby5j'}).find('a')
            if timme is not None:
                timme1 = timme.find('span').text
            else:
                timme1 = ""

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

            #發文內容圖片
            pictures = post.find_all('img', {'class': 'x1ey2m1c xds687c x5yr21d x10l6tqk x17qophe x13vifvy xh8yej3'})
            picture_url = []
            if pictures is not None:
                for picture in pictures:
                    picture_item = picture.get('src')
                    picture_url.append(picture_item)
                video4 = ""

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
            #         else:
            #             post_hashtag_collect.append(" ")
            # else:
            #     post_hashtag_collect.append(" ")
            
            #貼文讚數
            # likes = post.find('span', {'class': 'xrbpyxo x6ikm8r x10wlt62 xlyipyv x1exxlbk'}).find('span')
            # if likes is not None:
            #     likes1 = likes.find('span', {'class': 'xt0b8zv x1e558r4'}).text
            likes1 = ""

            #貼文留言數
            comments = post.find('div', {'class': 'x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x2lah0s x193iq5w xeuugli xg83lxy x1h0ha7o x10b6aqq x1yrsyyn'})
            # print(comments)
            if comments is not None:
                comments1 = comments.find('span', {'class': 'x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xi81zsa'}).text
            else:
                comments1 = "0"

            #每篇貼文的資訊
            post_detail = {}
            post_detail = {
                "post_image": image1,
                "post_name": name1,
                "post_club": club1,
                "post_time": timme1,
                "post_text": text3,
                "post_picture": picture_url,
                "post_video": video4,
                "post_hashtag": post_hashtag_collect,
                "post_likes": likes1,
                "post_comments": comments1
            }

            #所有貼文的集合
            post_item.append(post_detail)

        edge.quit()

        data = {
            'post_item': post_item
        }


    return jsonify(**data) 
############################## ajax ##############################


if __name__ == '__main__':
    app.run('0.0.0.0',port=8082,debug=True)


# 程式結束時釋放資料庫資源
cursor.close()
db.close()  # 關閉連線


