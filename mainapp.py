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
from datetime import datetime
from PIL import Image

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

#上傳照片
app.config['UPLOAD_FOLDER'] = 'static/img/uploads/'

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
        # 根據資料表出現的Hashtag次數羅列全站熱門
        sql = """
            SELECT h.TagName, COUNT(hr.TagId) as Count
            FROM hashtag_relationship hr
            JOIN hashtag h ON hr.TagId = h.TagId
            GROUP BY hr.TagId, h.TagName
            ORDER BY Count DESC
            LIMIT 10
        """
        # 根據資料表出現的Hashtag次數搜尋列顯示前三名
        sqlsearch = """
            SELECT h.TagName, COUNT(hr.TagId) as Count
            FROM hashtag_relationship hr
            JOIN hashtag h ON hr.TagId = h.TagId
            GROUP BY hr.TagId, h.TagName
            ORDER BY Count DESC
            LIMIT 3
        """

        cursor.execute(sql)
        hot_tags = cursor.fetchall()
        cursor.execute(sqlsearch)
        hot_3tags = cursor.fetchall()

        return render_template('index.html', hot_tags=hot_tags, hot_3tags=hot_3tags)


# 搜尋結果頁面
@app.route("/searchres", methods=['GET'])
def SearchRes():
    # 取得傳回的參數，此參數需傳回至前端
    # 撈取知識地圖資料，並傳回前端
    key = request.args.get('keyword') or ''
    tagName = str(key)
    nodeData = []
    linkData = []

    # sqlname = 'SELECT Owner FROM hashtag WHERE TagName = "%s";' % (tagName)
    # cursor.execute(sqlname)
    # result = cursor.fetchone()

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
    memId = "M1685006880" #目前寫死
    sql = 'select * from member where MemId = "%s";' % (memId)
    cursor.execute(sql)
    result = cursor.fetchone()
    memName = result[1]
    memImg = result[5]
    memAtId = result[6]
    sql = 'select * from hashtag where Owner = "%s" AND TagType = 6;' % (memId)
    cursor.execute(sql)
    results = cursor.fetchall()
    tags = []
    for result in results:
        tags.append(result[1])
    sql = 'select * from member_social_link where MemId = "%s";' % (memId)
    cursor.execute(sql)
    results = cursor.fetchall()
    links = []
    for result in results:
        if "twitter" in result[1]:
            icon = "twitter"
            path = "M5.026 15c6.038 0 9.341-5.003 9.341-9.334 0-.14 0-.282-.006-.422A6.685 6.685 0 0 0 16 3.542a6.658 6.658 0 0 1-1.889.518 3.301 3.301 0 0 0 1.447-1.817 6.533 6.533 0 0 1-2.087.793A3.286 3.286 0 0 0 7.875 6.03a9.325 9.325 0 0 1-6.767-3.429 3.289 3.289 0 0 0 1.018 4.382A3.323 3.323 0 0 1 .64 6.575v.045a3.288 3.288 0 0 0 2.632 3.218 3.203 3.203 0 0 1-.865.115 3.23 3.23 0 0 1-.614-.057 3.283 3.283 0 0 0 3.067 2.277A6.588 6.588 0 0 1 .78 13.58a6.32 6.32 0 0 1-.78-.045A9.344 9.344 0 0 0 5.026 15z"
        elif "facebook" in result[1]:
            icon = "facebook"
            path = "M16 8.049c0-4.446-3.582-8.05-8-8.05C3.58 0-.002 3.603-.002 8.05c0 4.017 2.926 7.347 6.75 7.951v-5.625h-2.03V8.05H6.75V6.275c0-2.017 1.195-3.131 3.022-3.131.876 0 1.791.157 1.791.157v1.98h-1.009c-.993 0-1.303.621-1.303 1.258v1.51h2.218l-.354 2.326H9.25V16c3.824-.604 6.75-3.934 6.75-7.951z"
        elif "instagram" in result[1]:
            icon = "instagram"
            path = "M8 0C5.829 0 5.556.01 4.703.048 3.85.088 3.269.222 2.76.42a3.917 3.917 0 0 0-1.417.923A3.927 3.927 0 0 0 .42 2.76C.222 3.268.087 3.85.048 4.7.01 5.555 0 5.827 0 8.001c0 2.172.01 2.444.048 3.297.04.852.174 1.433.372 1.942.205.526.478.972.923 1.417.444.445.89.719 1.416.923.51.198 1.09.333 1.942.372C5.555 15.99 5.827 16 8 16s2.444-.01 3.298-.048c.851-.04 1.434-.174 1.943-.372a3.916 3.916 0 0 0 1.416-.923c.445-.445.718-.891.923-1.417.197-.509.332-1.09.372-1.942C15.99 10.445 16 10.173 16 8s-.01-2.445-.048-3.299c-.04-.851-.175-1.433-.372-1.941a3.926 3.926 0 0 0-.923-1.417A3.911 3.911 0 0 0 13.24.42c-.51-.198-1.092-.333-1.943-.372C10.443.01 10.172 0 7.998 0h.003zm-.717 1.442h.718c2.136 0 2.389.007 3.232.046.78.035 1.204.166 1.486.275.373.145.64.319.92.599.28.28.453.546.598.92.11.281.24.705.275 1.485.039.843.047 1.096.047 3.231s-.008 2.389-.047 3.232c-.035.78-.166 1.203-.275 1.485a2.47 2.47 0 0 1-.599.919c-.28.28-.546.453-.92.598-.28.11-.704.24-1.485.276-.843.038-1.096.047-3.232.047s-2.39-.009-3.233-.047c-.78-.036-1.203-.166-1.485-.276a2.478 2.478 0 0 1-.92-.598 2.48 2.48 0 0 1-.6-.92c-.109-.281-.24-.705-.275-1.485-.038-.843-.046-1.096-.046-3.233 0-2.136.008-2.388.046-3.231.036-.78.166-1.204.276-1.486.145-.373.319-.64.599-.92.28-.28.546-.453.92-.598.282-.11.705-.24 1.485-.276.738-.034 1.024-.044 2.515-.045v.002zm4.988 1.328a.96.96 0 1 0 0 1.92.96.96 0 0 0 0-1.92zm-4.27 1.122a4.109 4.109 0 1 0 0 8.217 4.109 4.109 0 0 0 0-8.217zm0 1.441a2.667 2.667 0 1 1 0 5.334 2.667 2.667 0 0 1 0-5.334z"
        linkItem = {
            "icon": icon,
            "path": path,
            "link": result[1]
        }
        links.append(linkItem)
    sql = 'select * from post where Owner = "%s"' % (memId)
    cursor.execute(sql)
    results = cursor.fetchall()
    posts = []
    for result in results:
        time = result[6]
        print(time)
        datetime_obj = datetime.strptime(time, "%Y-%m-%d-%H:%M:%S")
        formatted_date = datetime_obj.strftime("%Y/%m/%d")
        postItem = {
            "title": result[1],
            "time": formatted_date
        }
        posts.append(postItem)
    
    user = {
        "name": memName,
        "atid": memAtId,
        "image": memImg,
        "tags": tags,
        "links": links,
        "posts": posts
    }

    return render_template('individual.html', user=user)


# 他人頁面
@app.route("/otherpeople", methods=['POST', 'GET'])
def Otherpeople():
    # 利用會員Id取得會員資料，並傳送至前端

    return render_template('other_people.html')


# 修改個人資訊頁面
@app.route("/infomodify", methods=['POST', 'GET'])
def Infomodify():
    memId = "M1685006880" #目前寫死
    sql = f"select * from member where MemId = '{memId}';"
    cursor.execute(sql)
    result = cursor.fetchone()
    name = result[1]
    memAtId = result[6]
    email = result[2]
    sql = f"select * from hashtag where Owner = '{memId}' and TagType = 6;"
    cursor.execute(sql)
    results = cursor.fetchall()
    tags = []
    for result in results:
        tags.append(result[1])
    sql = f"select * from member_social_link where Memid = '{memId}';"
    cursor.execute(sql)
    results = cursor.fetchall()
    links = []
    for result in results:
        # if "twitter" in result[1]:
        #     linkName = "Twitter"
        # elif "facebook" in result[1]:
        #     linkName = "Facebook"
        # elif "instagram" in result[1]:
        #     linkName = "Instagram"
        links.append(result[1])
    
    user = {
        "name": name,
        "atId": memAtId,
        "email": email,
        "tags": tags,
        "links": links
    }

    return render_template('info_modify.html', user = user)


# 個人記事頁面
@app.route("/personalnotes", methods=['POST', 'GET'])
def Personalnotes():

    return render_template('personal_notes.html')


# 編輯記事頁面
@app.route("/editnote", methods=['POST', 'GET'])
def Editnote():

    return render_template('edit_note.html')


# 新增記事頁面
@app.route("/newnote", methods=['POST', 'GET'])
def Newnote():
    if request.method == 'POST':
        memId = "M1685006880"
        title = str(request.values.get('title'))
        location = str(request.values.get('location'))
        tag = str(request.values.get('tag'))
        content = str(request.values.get('content'))
        time = str(datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))
        timestamp = int(datetime.now().timestamp())
        postId = str("P%s" % (timestamp))
        sql = f"INSERT INTO `post` (`DataId`, `Title`, `Content`, `PostType`, `Owner`, `Status`, `CreateTime`, `Hashtag`, `Location`) VALUES ('{postId}', '{title}', '{content}', 5, '{memId}', 1, '{time}', '{tag}', '{location}');"
        cursor.execute(sql)
        return redirect(url_for('Individual'))

    return render_template('new_note.html')


# 有關hashtag記事頁面
@app.route("/listnoteshashtag", methods=['POST', 'GET'])
def Listnoteshashtag():

    return render_template('list_notes_hashtag.html')


# 好友列表頁面
@app.route("/friendlist", methods=['POST', 'GET'])
def Friendlist():

    return render_template('friend_list.html')


# 歷史查詢頁面
@app.route("/history", methods=['POST', 'GET'])
def History():
 # 根據資料表出現的Hashtag次數羅列全站熱門
        sql = """
            SELECT h.TagName, COUNT(hr.TagId) as Count
            FROM hashtag_relationship hr
            JOIN hashtag h ON hr.TagId = h.TagId
            GROUP BY hr.TagId, h.TagName
            ORDER BY Count DESC
            LIMIT 10
        """
        # 根據資料表出現的Hashtag次數搜尋列顯示前三名
        sqlsearch = """
            SELECT h.TagName, COUNT(hr.TagId) as Count
            FROM hashtag_relationship hr
            JOIN hashtag h ON hr.TagId = h.TagId
            GROUP BY hr.TagId, h.TagName
            ORDER BY Count DESC
            LIMIT 3
        """

        cursor.execute(sql)
        hot_tags = cursor.fetchall()
        cursor.execute(sqlsearch)
        hot_3tags = cursor.fetchall()

        return render_template('history.html', hot_tags=hot_tags, hot_3tags=hot_3tags)


# 客服中心頁面
@app.route("/customerservice", methods=['POST', 'GET'])
def Customerservice():

    return render_template('customer_service.html')


# 客服諮詢紀錄頁面
@app.route("/consultationrecord", methods=['POST', 'GET'])
def Consultationrecord():

    return render_template('consultation_record.html')


# 關於我們頁面
@app.route("/aboutus", methods=['POST', 'GET'])
def Aboutus():

    return render_template('about_us.html')

# Hashtag管理頁面
@app.route("/hashtag_manage", methods=['POST', 'GET'])
def Hashtagmanage():

    return render_template('hashtag_manage.html')
        
##############新增物件頁面測試用############
#user_TargetName=[];
#user_ObjName=[];
#user_Type=[];
#user_Des=[];
#user_Targetid=[];
#user_nf=[];
#user_n=[];

# Hashtag管理_新增物件頁面
@app.route("/hashtag_manage_new", methods=['GET', 'POST'])
def Hashtagmanagenew():
    if request.method == 'POST':
        if 'Picfile' in request.files:
            image = request.files['Picfile']
            TargetName = request.form['TargetName'],
            ObjName = request.form['TargetName'],
            Type = request.form['Type'],
            Description = request.form['Description'], 
            if image.filename != '':    

        #user_TargetName.append(TargetName)
        #user_ObjName.append(TargetName)
        #user_Type.append(Type)
        #user_Des.append(Description)
        #user_i.append(image)

                # Convert to JPEG format and Save image
                target_id = "T" + str(int(time.time()))
                new_filename = target_id+'.jpg'
                now = datetime.now()
                create_time = now.strftime('%Y-%m-%d %H:%M')
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
                image.save(save_path)
                image_path = "../static/img/uploads/" + new_filename
        #user_Targetid.append(target_id)
        #user_nf.append(new_filename)
        #user_n.append(image_path)
               
                sql = 'INSERT INTO img_target (TargetId, TargetName, ObjName, Type, Description, CreateTime, ImagePath) VALUES (%s, %s, %s, %s, %s, %s, %s)'
                data = (target_id, TargetName, ObjName, Type, Description, create_time, image_path)
            
            #target_id_to_delete = "T1693142334";  刪除測試用

            try:
                cursor.execute(sql, data)
                #delete_sql = 'DELETE FROM img_target WHERE TargetId = %s' 刪除測試用
                #cursor.execute(delete_sql, (target_id_to_delete,)) 刪除測試用
                #db.commit() 刪除測試用
                db.commit()
                #print("Insertion successful")
                return redirect(url_for('Hashtagmanage'))

            except Exception as e:
                db.rollback()
                #print("Insertion failed:", str(e))

    return render_template('hashtag_manage_new.html')
    #測試用：user_TargetName=user_TargetName,user_n=user_n, user_ObjName=user_ObjName, user_Type= user_Type, user_Des=user_Des, user_Targetid=user_Targetid, user_nf=user_nf, user_n=user_n

# Hashtag編輯頁面
@app.route("/hashtag_manage_edit", methods=['POST', 'GET'])
def Hashtagmanageedit():

    return render_template('hashtag_manage_edit.html')

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


#新增好友
@app.route("/addfriend", methods=['POST'])
def AddFriend():
    # 取得MemId
    selfMemId = ''
    newFriendId = request.values.get('memId')

    try:
        sql = f'INSERT INTO member_relationship VALUE ({selfMemId}, {newFriendId})'
        cursor.execute(sql)
        db.commit()

        return jsonify(**{'res':'success'})

    except:
        db.rollback()
        return jsonify(**{'res':'fail'})


#刪除好友
@app.route("/deletefriend", methods=['POST'])
def DeleteFriend():
    # 取得MemId
    selfMemId = ''
    friendId = request.values.get('memId')

    try:
        sql = f'Delete FROM member_relationship WHERE MemId=\'{selfMemId}\' AND ObjId=\'{friendId}\';'
        cursor.execute(sql)
        db.commit()
        return jsonify(**{'res':'success'})

    except:
        db.rollback()
        return jsonify(**{'res':'fail'})


#查詢好友列表
@app.route("/getfriendlist", methods=['POST'])
def GetFriendList():
    # 取得MemId
    selfMemId = ''
    try:
        sql = f'Select FROM member_relationship WHERE MemId=\'{selfMemId}\';'
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        return jsonify(**{'res':'success'})

    except:
        db.rollback()
        return jsonify(**{'res':'fail'})


#變更好友間狀態、關係
@app.route("/changefriendstatus", methods=['POST'])
def ChangeFriendStatus():
    # 取得MemId
    selfMemId = ''
    friendId = request.values.get('memId')
    status = request.values.get('status')

    # ! 目前資料表沒有Status這個欄位，需要討論是否新增該欄位
    try:
        status = int(status)
    except:
      status = 1

    try:
        sql = f'UPDATE member_relationship SET Status={status} WHERE MemId=\'{selfMemId}\' AND ObjId=\'{friendId}\';'
        cursor.execute(sql)
        db.commit()
        return jsonify(**{'res':'success'})

    except:
        db.rollback()
        return jsonify(**{'res':'fail'})
############################## ajax ##############################


############################## fetch ##############################

@app.route("/add_tag", methods=['POST'])
def add_tag():
    data = request.get_json()
    tag = str(data.get('tag', None))
    print(tag)
    memId = "M1685006880" #目前寫死
    time = str(datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))
    timestamp = int(datetime.now().timestamp())
    tagId = str("H%s" % (timestamp))
    print(tagId)
    try:
        sql = f"insert into hashtag values ('{tagId}', '{tag}', 6, '{memId}', 1, '{tag}', '{time}');"
        result = cursor.execute(sql)
        db.commit()
        return jsonify({"result": "Add successful"}), 200
    except:
        db.rollback()
        return jsonify({"result": "Add failed"}), 400

@app.route("/delete_tag", methods=['POST'])
def delete_tag():
    data = request.get_json()
    tag = str(data.get('tag', None))
    memId = "M1685006880" #目前寫死
    try:
        sql = f"delete from hashtag where Owner = '{memId}' and TagName = '{tag}' and TagType = 6;"
        result = cursor.execute(sql)
        db.commit()
        return jsonify({"result": "Delete successful"}), 200
    except:
        db.rollback()
        return jsonify({"result": "Delete failed"}), 400

@app.route("/add_link", methods=['POST'])
def add_link():
    data = request.get_json()
    link = str(data.get('link', None))
    memId = "M1685006880" #目前寫死
    time = str(datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))
    try:
        sql = f"insert into member_social_link values ('{memId}', '{link}', '{time}');"
        print(sql)
        result = cursor.execute(sql)
        print(result)
        db.commit()
        return jsonify({"result": "Add successful"}), 200
    except:
        db.rollback()
        return jsonify({"result": "Add failed"}), 400

@app.route("/delete_link", methods=['POST'])
def delete_link():
    data = request.get_json()
    link = str(data.get('link', None))
    memId = "M1685006880" #目前寫死
    try:
        sql = f"delete from member_social_link where MemId = '{memId}' and SocialLink = '{link}';"
        result = cursor.execute(sql)
        db.commit()
        return jsonify({"result": "Delete successful"}), 200
    except:
        db.rollback()
        return jsonify({"result": "Delete failed"}), 400
    
@app.route("/update_info", methods=['POST'])
def update_info():
    data = request.get_json()
    name = str(data.get('name', None))
    memAtId = str(data.get('id', None))
    email = str(data.get('email', None))
    memId = "M1685006880" #目前寫死
    try:
        sql = f"update member set MemName = '{name}', Email = '{email}', MemAtId = '{memAtId}' where MemId = '{memId}';"
        cursor.execute(sql)
        db.commit()
        return jsonify({"result": "Update successful"}), 200
    except:
        db.rollback()
        return jsonify({"result": "Update failed"}), 400
    
@app.route("/update_cancel", methods=['GET'])
def update_cancel():
    memId = "M1685006880" #目前寫死
    sql = f"select * from member where MemId = '{memId}';"
    cursor.execute(sql)
    result = cursor.fetchone()
    name = result[1]
    memAtId = result[6]
    email = result[2]
    user = {
        "name": name,
        "id": memAtId,
        "email": email
    }
    return jsonify(**user), 200

############################## fetch ##############################


if __name__ == '__main__':
    app.run('0.0.0.0',port=8082,debug=True)


# 程式結束時釋放資料庫資源
cursor.close()
db.close()  # 關閉連線


