from flask import Flask, app, redirect, session, request, jsonify, Response, url_for, abort, Blueprint,render_template
from flask_sqlalchemy import SQLAlchemy
import os,sys
import json
import requests
import time
import re
from datetime import datetime
from PIL import Image
from bs4 import BeautifulSoup
import lxml
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.by import By
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename

from model import Mysql
import src,model

url = {
    'fb':'https://www.facebook.com/hashtag/',
    'ig':'...',
    'twitter':'...',
}


#主程式初始化
app = Flask(__name__,static_url_path ='/static/')
app.secret_key = '29hPoRZOsSVj5RRD'

#初始化功能模組
tools_CommonTools = src.CommonTools.CommonTools()

# 呼叫 Mysql() 函式以獲取 db 變數
db, cursor = Mysql()
cursor = db.cursor()

tagName = ""

#上傳照片
app.config['UPLOAD_FOLDER'] = 'static/img/uploads/'

# Init login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "Login"

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(member_id):
    if member_id == "M1685006123":
        sql = f'select * from sys_admin where MemId = "{member_id}";'
        cursor.execute(sql)
        admin = cursor.fetchone()
        if admin is None:
            return
        user = User()
        user.id = member_id
        return user

    sql = f'select * from member where MemId = "{member_id}";'
    cursor.execute(sql)
    member = cursor.fetchone()
    if member is None:
        return
    user = User()
    user.id = member_id
    return user

############################## function ##############################
#獲取爬蟲抓下的貼文內，所有相關的hashtag集合
def extract_hashtags(content):
    hashtags = re.findall(r'#(\w+)', content)
    return hashtags
############################## function ##############################

############################## page ##############################
# 首頁
@app.route("/", methods=['POST', 'GET'])
@login_required 
def Index():
        memId = current_user.id
        print(f'current user: {memId}')
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


# 登入頁面
@app.route("/login", methods=['POST', 'GET'])
def Login():
    if request.method == 'POST':
        email = request.values.get('email')
        password = request.values.get('password')

        sql = f'select * from sys_admin where Account = "{email}" and Password = "{password}";'
        cursor.execute(sql)
        admin = cursor.fetchone()
        if admin:
            member_id = admin[0]
            user = User()
            user.id = member_id
            login_user(user)
            return redirect(url_for('Index'))
        
        sql = f'select * from member where Email = "{email}" and Password = "{password}";'
        cursor.execute(sql)
        member = cursor.fetchone()
        if member:
            member_id = member[0]
            user = User()
            user.id = member_id
            login_user(user)
            return redirect(url_for('Index'))
        else:
            return render_template('login.html', error=True)
    logout_msg = request.values.get('logout_msg')
    register_msg = request.values.get('msg')
    register_msg_success = None
    register_msg_fail = None
    if register_msg == "註冊成功":
        register_msg_success = register_msg
    else:
        register_msg_fail = register_msg

    return render_template('login.html', msg_success=register_msg_success, msg_fail=register_msg_fail, logout_msg=logout_msg)


# 登出
@app.route("/logout")
def Logout():
    logout_user()
    return redirect(url_for('Login', logout_msg='登出成功'))


# 註冊
@app.route("/add/member", methods=['POST'])
def add_member():
    email = request.values.get('email_register')
    password = request.values.get('password_register')
    name = request.values.get('name')
    id = request.values.get('ID')
    picture = request.files['picture']
    at_id = f"@{id}"
    time = str(datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))
    timestamp = int(datetime.now().timestamp())
    mem_id = f"M{timestamp}"

    # 檢查是否有圖片檔案
    if picture:
        # 儲存圖片
        picture.save(os.path.join('static/img/uploads', picture.filename))
        picture_path = f'../static/img/uploads/{picture.filename}'
        print("成功儲存")
    else:
        picture_path = ''  # 如果沒有圖片，設定為空字串或其他適合的預設值
        print("儲存失敗")

    sql = f"insert into member values ('{mem_id}', '{name}', '{email}', 1, '{time}', '{picture_path}', '{at_id}', '{password}');"
    try:
        cursor.execute(sql)
        db.commit()
        return redirect(url_for('Login', msg='註冊成功'))
    except:
        db.rollback()
        return redirect(url_for('Login', msg='註冊成功'))


# 搜尋結果頁面
@app.route("/searchres", methods=['GET'])
@login_required 
def SearchRes():
    # 取得傳回的參數，此參數需傳回至前端
    # 撈取知識地圖資料，並傳回前端
    key = request.args.get('keyword') or ''
    tagName = str(key)
    nodeData = []
    linkData = []
    dictCategoryType = {
        1:"people",
        2:"place",
        3:"obj",
        4:"tag",
        5:"post",
    }

    sql = 'select * from hashtag where TagName = "%s" and Status = %s;' % (tagName, 1)
    print(sql)
    cursor.execute(sql)
    result = cursor.fetchone()
    if result is not None:
        tagId = result[0]

        node1 = {
            "key": tagId,
            "category": dictCategoryType[result[2]],
            "text": tagName,
            "description": result[5],
            "type": dictCategoryType[result[2]]
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

                node2 = {
                    "key": objId,
                    "category": dictCategoryType[result1[3]],
                    "text": targetName,
                    "description": result1[4],
                    "type": dictCategoryType[result1[3]],
                    "imgPath": result1[6]
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

                node2 = {
                    "key": objId,
                    "category": dictCategoryType[result1[3]],
                    "text": objId,
                    "description": objId,
                    "type": dictCategoryType[result1[3]]
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
                sql = 'select * from hashtag where TagId = "%s" and Status = %s;' % (tagId1, 1)
                cursor.execute(sql)
                result3 = cursor.fetchone()

                node3 = {
                    "key": tagId1,
                    "category": dictCategoryType[result3[2]],
                    "text": result3[1],
                    "description": result3[5],
                    "type": dictCategoryType[result3[2]]
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
@login_required 
def Individual():
    # 利用session 取得會員Id
    # 利用會員Id取得會員資料，並傳送至前端
    if request.method == 'POST':
        memId = request.values.get('mem') or current_user.id
    
    else:
        memId = request.args.get('mem') or current_user.id

    if memId == current_user.id:
        mode = 'self'
    
    else:
        mode = 'other'

    print(memId)
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
            "time": formatted_date,
            "postId": result[0]
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

    return render_template('individual.html', user=user,Mode=mode)


# 修改個人資訊頁面
@app.route("/infomodify", methods=['POST', 'GET'])
@login_required 
def Infomodify():
    memId = current_user.id
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
@login_required 
def Personalnotes():
    memId = current_user.id
    postId = request.values.get('postId')
    sql = f"select * from post where DataId = '{postId}' and Owner = '{memId}';"
    cursor.execute(sql)
    result = cursor.fetchone()
    # tag = result[7]
    # tagList = tag.split(" ")
    postItem = {
        "location": result[8],
        "time": result[6],
        "tags": result[7],
        "title": result[1],
        "content": result[2],
        "id": result[0]
    }

    # Get the most recent post
    recent_post_sql = f"SELECT * FROM post WHERE Owner = '{memId}' ORDER BY CreateTime DESC LIMIT 1;"
    cursor.execute(recent_post_sql)
    recent_post_result = cursor.fetchone()
    recent_postItem = {
        "location": recent_post_result[8],
        "time": recent_post_result[6],
        "tags": recent_post_result[7],
        "title": recent_post_result[1],
        "content": recent_post_result[2],
        "id": recent_post_result[0]
    }

    return render_template('personal_notes.html', postItem=postItem, recent_postItem=recent_postItem, edit_model=True)

# 記事搜尋結果頁面
@app.route("/notes/<data_id>", methods=['GET'])
@login_required
def ResultNotes(data_id):
    sql = f"select * from post where DataId = '{data_id}';"
    cursor.execute(sql)
    result = cursor.fetchone()
    if result:
        user_id = result[4]
        sql = f"select * from member where MemId='{user_id}';"
        cursor.execute(sql)
        member_result = cursor.fetchone()
        postItem = {
            "location": result[8],
            "time": result[6],
            "tags": result[7],
            "title": result[1],
            "content": result[2],
            "id": result[0],
            "user_name": member_result[1]
        }
        return render_template('personal_notes.html', postItem=postItem, view_model=True)
    else:
        return redirect(url_for('Index'))

# 編輯記事頁面
@app.route("/editnote", methods=['POST', 'GET'])
@login_required 
def Editnote():

    return render_template('edit_note.html')


# 新增記事頁面
@app.route("/newnote", methods=['POST', 'GET'])
@login_required 
def Newnote():
    if request.method == 'POST':
        memId = current_user.id
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
@login_required 
def Listnoteshashtag():

    return render_template('list_notes_hashtag.html')


# 好友列表頁面
@app.route("/friendlist", methods=['POST', 'GET'])
@login_required 
def Friendlist():

    return render_template('friend_list.html')


# 歷史查詢頁面
@app.route("/history", methods=['POST', 'GET'])
@login_required 
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
@login_required 
def Customerservice():

    return render_template('customer_service.html')


# 客服諮詢紀錄頁面
@app.route("/consultationrecord", methods=['POST', 'GET'])
@login_required 
def Consultationrecord():

    return render_template('consultation_record.html')


# 關於我們頁面
@app.route("/aboutus", methods=['POST', 'GET'])
@login_required 
def Aboutus():

    return render_template('about_us.html')

# Hashtag管理頁面
@app.route("/hashtag_manage", methods=['POST', 'GET'])
@login_required 
def Hashtagmanage():
    sqlsearch = """
            SELECT TargetName
            FROM img_target
            WHERE TargetId IN (
            SELECT TargetId
            FROM member_img_target 
            WHERE MemId = 'M1685006880'
            )
            ORDER BY CreateTime DESC;
            ;
        """

    cursor.execute(sqlsearch)
    hashtag_manage = cursor.fetchall()

    return render_template('hashtag_manage.html', hashtag_manage=hashtag_manage)
        
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
@login_required 
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
                tag_id = "H" + str(int(time.time()))
                new_filename = target_id+'.jpg'
                now = datetime.now()
                create_time = now.strftime('%Y-%m-%d %H:%M')
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
                image.save(save_path)
                image_path = "../static/img/uploads/" + new_filename
        #user_Targetid.append(target_id)
        #user_nf.append(new_filename)
        #user_n.append(image_path)
                status="1"
                MemId="M1685006880" #先寫死
                TagType="6"

                sql = 'INSERT INTO img_target (TargetId, TargetName, ObjName, Type, Description, CreateTime, ImagePath) VALUES (%s, %s, %s, %s, %s, %s, %s)'
                data = (target_id, TargetName, ObjName, Type, Description, create_time, image_path)
                sql_2 = 'INSERT INTO member_img_target (TargetId, MemId, RelationshipType, status, CreateTime) VALUES (%s, %s, %s, %s, %s)'
                data_2 = (target_id, MemId, Type, status, create_time)
                sql_3 = 'INSERT INTO hashtag (TagId, TagName, TagType, Owner, Status, Description, CreateTime) VALUES (%s, %s, %s, %s, %s, %s, %s)'
                data_3 = (tag_id, TargetName, TagType, MemId, status, TargetName, create_time)
                sql_4 = 'INSERT INTO hashtag_relationship (TagId, ObjId, RelationshipType, Status, CreateTime) VALUES (%s, %s, %s, %s, %s)'
                data_4 = (tag_id, target_id, status, status, create_time)
            
            #target_id_to_delete = "T1693142334";  刪除測試用

            try:
                cursor.execute(sql, data)
                #delete_sql = 'DELETE FROM img_target WHERE TargetId = %s' 刪除測試用
                #cursor.execute(delete_sql, (target_id_to_delete,)) 刪除測試用
                #db.commit() 刪除測試用
                db.commit()
                cursor.execute(sql_2, data_2)
                db.commit()
                cursor.execute(sql_3, data_3)
                db.commit()
                cursor.execute(sql_4, data_4)
                db.commit()
                return redirect(url_for('Hashtagmanage'))

            except Exception as e:
                db.rollback()
                #print("Insertion failed:", str(e))

    return render_template('hashtag_manage_new.html')
    #測試用：user_TargetName=user_TargetName,user_n=user_n, user_ObjName=user_ObjName, user_Type= user_Type, user_Des=user_Des, user_Targetid=user_Targetid, user_nf=user_nf, user_n=user_n

# Hashtag編輯頁面
@app.route("/hashtag_manage_edit/<option>", methods=['POST', 'GET'])
@login_required 
def Hashtagmanageedit(option):
        sql = f"select * from img_target where TargetName= '{option}';"
        cursor.execute(sql)
        result = cursor.fetchone()   

        image_target_id=result[0]
        target_name = result[1]
        description=result[4]
        jpg_url=result[6]

        print(result)

        public_words = request.form.getlist('public_words[]')
        private_words = request.form.getlist('private_words[]')

        tag_id = "H" + str(int(time.time()))
        now = datetime.now()
        create_time = now.strftime('%Y-%m-%d %H:%M')
        relationshiptype="1"
        publicStatus="4"
        privateStatus="6"
        MemId="M1685006880"

        for word in public_words:
            sql = 'INSERT INTO hashtag_relationship (TagId, ObjId, RelationshipType, Status, CreateTime) VALUES (%s, %s, %s, %s, %s)'
            data = (tag_id, image_target_id, relationshiptype, relationshiptype, create_time)
            sql2 = 'INSERT INTO hashtag (TagId, TagName, TagType, Owner, Status, Description, CreateTime) VALUES (%s, %s, %s, %s, %s, %s, %s)'
            data2 = (tag_id, word, publicStatus, MemId, relationshiptype, word, create_time)

        for word in private_words:
            sql3 = 'INSERT INTO hashtag_relationship (TagId, ObjId, RelationshipType, Status, CreateTime) VALUES (%s, %s, %s, %s, %s)'
            data3 = (tag_id, image_target_id, relationshiptype, relationshiptype, create_time)
            sql4 = 'INSERT INTO hashtag (TagId, TagName, TagType, Owner, Status, Description, CreateTime) VALUES (%s, %s, %s, %s, %s, %s, %s)'
            data4 = (tag_id, word, privateStatus, MemId, relationshiptype, word, create_time)
            
            try:
                cursor.execute(sql, data)
                db.commit()
                cursor.execute(sql2, data2)
                db.commit()
                cursor.execute(sql3, data3)
                db.commit()
                cursor.execute(sql4, data4)
                db.commit()
                return redirect(url_for('Hashtagmanage'))

            except Exception as e:
                db.rollback()
                #print("Insertion failed:", str(e))
        
        return render_template('hashtag_manage_edit.html', target_name=target_name, description=description, jpg_url=jpg_url)

@app.route("/hashtag_review", methods=['GET'])
def HashtagReview():
    review_objs = []
    sql = f'select * from feedback;'
    cursor.execute(sql)
    results = cursor.fetchall()
    for result in results:
        tag_id = result[3]
        print(tag_id)
        sql = f'select * from hashtag where TagId = "{tag_id}";'
        cursor.execute(sql)
        res = cursor.fetchone()
        obj = {
            "tag_id": res[0],
            "tag_name": res[1],
            "reason": result[5]
        }
        print(obj)
        review_objs.append(obj)
    
    return render_template('hashtag_review.html', reviews=review_objs)

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
        browser = webdriver.Chrome(options=options)

        browser.get("https://www.facebook.com/")
        time.sleep(1)
        email = browser.find_element(By.ID, "email")
        password = browser.find_element(By.ID, "pass")
        email.send_keys('tictagtoe.im@gmail.com')
        password.send_keys('#TicTAGToe')
        password.submit()
        time.sleep(1)

        browser.get(url)
        time.sleep(4)
        for x in range(page*2): 
            browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            if x < (page-1) * 3:
                continue
            else:
                time.sleep(2) 
    
        soup = BeautifulSoup(browser.page_source, 'lxml')

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
            name = post.find('a', {'class': 'x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f'})
            if name is not None:
                name1 = name.find('span')
            else:
                name1 = " "
            try:
                if name1 is not None:
                    name1 = name1.text
            except Exception as e:
                print(f"A error occurred: {e}")
                continue

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
            pictures = post.find_all('img', {'class': 'x1ey2m1c xds687c x5yr21d x10l6tqk x17qophe x13vifvy xh8yej3 xl1xv1r'})
            picture_url = []
            if pictures is not None:
                for picture in pictures:
                    picture_item = picture.get('src')
                    picture_url.append(picture_item)
            
            pictures_multi = post.find_all('img', {'class': 'x1ey2m1c xds687c x5yr21d x10l6tqk x17qophe x13vifvy xh8yej3'})
            for picture in pictures_multi:
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
            
            #貼文讚數
            likes = post.find('span', {'class': 'xt0b8zv x2bj2ny xrbpyxo xl423tq'})
            if likes is not None:
                likes1 = likes.find('span', {'class': 'x1e558r4'})
                if likes1 is not None:
                    likes1 = likes1.text

            # likes1 = " "

            #貼文留言數
            comments = post.find('div', {'class': 'x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x2lah0s x193iq5w xeuugli xg83lxy x1h0ha7o x10b6aqq x1yrsyyn'})
            # print(comments)
            if comments is not None:
                comments1 = comments.find('span', {'class': 'x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xi81zsa'}).text
            else:
                comments1 = "0"

            #每篇貼文的資訊
            post_detail = {
                "post_image": image1,
                "post_name": name1,
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

        browser.quit()

        data = {
            'post_item': post_item
        }

    return jsonify(**data) 

#搜尋IG貼文頁面
@app.route("/search_IG", methods=['POST'])
def search_IG():
    post_item = [] 
    soup_list = []
    if request.method == 'POST':
        key = request.form['keyword']
        page = request.form.get('page') or 1
        page = int(page)
        socialName = "https://www.instagram.com/explore/tags/"
        tagName = str(key)
        url = socialName + tagName
        options = Options()
        options.add_argument("--disable-notifications")
        browser = webdriver.Chrome(options=options)

        browser.get("https://www.instagram.com/")
        time.sleep(1)
        email = browser.find_element(By.NAME, "username")
        password = browser.find_element(By.NAME, "password")
        login_btn = browser.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')
        email.send_keys('tictagtoe_hashtag')
        password.send_keys('tictagtoe_cycu')
        login_btn.click()
        time.sleep(4)
        store_btn = browser.find_element(By.TAG_NAME, 'button')
        store_btn.click()
        time.sleep(1)

        browser.get(url)
        time.sleep(2)
        for x in range(page*2): 
            browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            if x < (page-1) * 3:
                continue
            else:
                time.sleep(2) 
        soup = BeautifulSoup(browser.page_source, 'lxml')

        #取得每篇貼文的連結
        post_urls = []
        page_body = soup.find('article', {'class': '_aao7'}).find('div', {'class': '_aaq8'}).find_all('div')
        post_block = page_body[1]
        items = post_block.find('div').find_all('div')
        for rows in items:
            a_tag_block = rows.find_all('div')
            for block in a_tag_block:
                block_url = block.find('a')
                if block_url:
                    post_urls.append(block_url['href'])
        
        browser.quit() 

        post_urls = post_urls[:6]
        soup_list = get_ig_post_content(post_urls)

        for soup in soup_list:
            try:
                post_body = soup.find('div', {'class': 'x1yvgwvq x1dqoszc x1ixjvfu xhk4uv x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x178xt8z xm81vs4 xso031l xy80clv x78zum5 x1q0g3np xh8yej3'})
                primary_part = post_body.find('div', {'class': 'x4h1yfo'})\
                    .find('div', {'class': 'xvbhtw8 x78zum5 xdt5ytf x5yr21d x1n2onr6 xh8yej3'})\
                    .find('div', {'class': 'x5yr21d xw2csxc x1odjw0f x1n2onr6'})\
                    .find('div', {'class': 'x9f619 x78zum5 xdt5ytf x5yr21d x10l6tqk xh8yej3 xexx8yu x4uap5 x18d9i69 xkhd6sd'})\
                    .find('div', {'class': 'x5yr21d'})\
                    .find('ul', {'class': '_a9z6 _a9za'})\
                    .find('div', {'class': 'x1qjc9v5 x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x78zum5 xdt5ytf x2lah0s xk390pu xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 xggy1nq x11njtxf'})\
                    .find('li')\
                    .find('div', {'class': '_a9zm'})\
                    .find('div', {'class': '_a9zn _a9zo'})
                
                #貼文者頭貼
                post_image = primary_part.find('div', {'class': 'x1lliihq'})\
                    .find('div', {'class': 'x1lliihq'})\
                    .find('div', {'class': '_aarf _a9zp'})\
                    .find('a', {'class': 'x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk x78zum5 xdl72j9 xdt5ytf x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt xnz67gz x14yjl9h xudhj91 x18nykt9 xww2gxu x9f619 x1lliihq x2lah0s x6ikm8r x10wlt62 x1n2onr6 x1ykvv32 xougopr x159fomc xnp5s1o x194ut8o x1vzenxt xd7ygy7 xt298gk x1xrz1ek x1s928wv x1n449xj x2q1x1w x1j6awrg x162n7g1 x1m1drc7 x1ypdohk x4gyw5p _a6hd'})\
                    .find('img')['src']
                
                #貼文者名稱
                post_name = primary_part.find('div', {'class': '_a9zr'})\
                    .find('h2')\
                    .find('div', {'class': 'x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh xw3qccf x1n2onr6 x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1'})\
                    .find('div', {'class': 'xt0psk2'})\
                    .find('div', {'class': 'xt0psk2'})\
                    .find('a', {'class': 'x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x1lku1pv x1a2a7pz x6s0dn4 xjyslct x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 x1ypdohk x1i0vuye x1f6kntn xwhw2v2 xl56j7k x17ydfre x2b8uid xlyipyv x87ps6o x14atkfc xcdnw81 xjbqb8w xm3z3ea x1x8b98j x131883w x16mih1h x972fbf xcfux6l x1qhh985 xm0m39n xt0psk2 xt7dq6l xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x1n5bzlp xqnirrm xj34u2y x568u83'}).text                    
                
                #貼文內容
                post_content = primary_part.find('div', class_='_a9zr')\
                    .find('div', class_='_a9zs')\
                    .find('h1', class_='_aacl _aaco _aacu _aacx _aad7 _aade').text    

                #貼文時間            
                post_time = post_body.find('div', class_='x4h1yfo')\
                    .find('div', class_='xvbhtw8 x78zum5 xdt5ytf x5yr21d x1n2onr6 xh8yej3')\
                    .find('div', class_='x1xp8e9x x13fuv20 x178xt8z x9f619 x1yrsyyn x1pi30zi x10b6aqq x1swvt13 xh8yej3')\
                    .find('div', class_='x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1yztbdb x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1cy8zhl x1oa3qoh x1nhvcw1')\
                    .find('div', class_='_aacl _aaco _aacu _aacx _aad6 _aade _aaqb')\
                    .find('a', class_='x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _a6hd')\
                    .find('span', class_='x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye x1yxbuor xo1l8bm x1roi4f4 x1s3etm8 x676frb x10wh9bi x1wdrske x8viiok x18hxmgj')\
                    .find('time', class_='_aaqe').text
                
                picture_url = []
                #貼文圖片
                post_picture = post_body.find('div', class_='x6s0dn4 x1dqoszc xu3j5b3 xm81vs4 x78zum5 x1iyjqo2 x1tjbqro')\
                    .find('div', class_='x1lliihq xh8yej3')\
                    .find('div', class_='x1qjc9v5 x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x78zum5 xdt5ytf x2lah0s xk390pu xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 xggy1nq x11njtxf')\
                    .find('div')\
                    .find('div', class_='x1i10hfl')\
                    .find('div')\
                    .find('div', class_='_aagu')\
                    .find('div', class_='_aagv')\
                    .find('img')['src']
                picture_url.append(post_picture)

                #貼文讚數
                post_likes = post_body.find('div', class_='x4h1yfo')\
                    .find('div', class_='xvbhtw8 x78zum5 xdt5ytf x5yr21d x1n2onr6 xh8yej3')\
                    .find('div', class_='x1xp8e9x x13fuv20 x178xt8z x9f619 x1yrsyyn x1pi30zi x10b6aqq x1swvt13 xh8yej3')\
                    .find('section', class_='x12nagc')\
                    .find('div', class_='x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1n2onr6 x1plvlek xryxfnj x1iyjqo2 x2lwn1j xeuugli x1q0g3np xqjyukv x6s0dn4 x1oa3qoh x1nhvcw1')\
                    .find('div', class_='x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh xr1yuqi xkrivgy x4ii5y1 x1gryazu x1n2onr6 x1plvlek xryxfnj x1iyjqo2 x2lwn1j xeuugli xdt5ytf x1a02dak xqjyukv x1cy8zhl x1oa3qoh x1nhvcw1')\
                    .find('span', class_='x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xvs91rp xo1l8bm x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj')\
                    .find('a', class_='x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _a6hd')\
                    .find('span', class_='x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs xt0psk2 x1i0vuye xvs91rp x1s688f x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj')\
                    .find('span', class_='html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs').text
                
                #貼文hashtag
                post_hashtag = extract_hashtags(post_content)
                post_tags = ['#' + tag for tag in post_hashtag]       

                #每篇貼文的資訊
                post_detail = {
                    "post_image": post_image,
                    "post_name": post_name,
                    "post_time": post_time,
                    "post_text": post_content,
                    "post_picture": picture_url,
                    "post_video": "",
                    "post_hashtag": post_tags,
                    "post_likes": post_likes,
                    "post_comments": 0
                }
                post_item.append(post_detail)   
            except Exception as e:
                print(e)
                continue

        data = {
            'post_item': post_item
        }

    return jsonify(**data) 

def get_ig_post_content(url_list):
    ig_url = "https://www.instagram.com/"
    soup_list = []
    options = Options()
    options.add_argument("--disable-notifications")
    browser = webdriver.Chrome(options=options)
    browser.get(ig_url)
    time.sleep(1)
    email = browser.find_element(By.NAME, "username")
    password = browser.find_element(By.NAME, "password")
    login_btn = browser.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')
    email.send_keys('tictagtoe_hashtag')
    password.send_keys('tictagtoe_cycu')
    login_btn.click()
    time.sleep(4)
    store_btn = browser.find_element(By.TAG_NAME, 'button')
    store_btn.click()
    time.sleep(1)
    print(url_list)
    for url in url_list:
        post_url = f'{ig_url}{url}'
        browser.get(post_url)
        time.sleep(2)
        soup = BeautifulSoup(browser.page_source, 'lxml')
        soup_list.append(soup)
    browser.quit() 
    return soup_list

#搜尋twitter貼文頁面
@app.route("/search_twitter", methods=['POST'])
def search_twitter():
    post_item = [] 
    if request.method == 'POST':
        key = request.form['keyword']
        page = request.form.get('page') or 1
        page = int(page)
        url = f'https://twitter.com/search?q=(%23{key})%20lang%3Azh-tw&src=typed_query'
        options = Options()
        options.add_argument("--disable-notifications")
        browser = webdriver.Chrome(options=options)
        browser.get("https://twitter.com/")
        time.sleep(1)
        login_btn = browser.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/div/div/div[3]/div[5]/a')
        login_btn.click()
        time.sleep(2)
        email = browser.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')
        next_step_btn = browser.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]')
        email.send_keys('tictagtoe.im@gmail.com')
        next_step_btn.click()
        time.sleep(2)
        user_name = browser.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input')
        next_step_btn = browser.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div')
        user_name.send_keys('tictagtoe_cyim')
        next_step_btn.click()
        time.sleep(2)
        password = browser.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
        confirm_login_btn = browser.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div')
        password.send_keys('#TicTAGToe')
        confirm_login_btn.click()
        time.sleep(2)
        browser.get(url)
        time.sleep(2)

        for x in range(page*2): 
            browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            if x < (page-1) * 3:
                continue
            else:
                time.sleep(2) 
        soup = BeautifulSoup(browser.page_source, 'lxml')

        posts = soup.find_all('article', class_='css-1dbjc4n r-1loqt21 r-18u37iz r-1ny4l3l r-1udh08x r-1qhn6m8 r-i023vh r-o7ynqc r-6416eg')
        for post in posts:
            print("\n")
            # print(post)

            post_body = post.find('div', class_='css-1dbjc4n r-eqz5dr r-16y2uox r-1wbh5a2')\
                .find('div', class_='css-1dbjc4n r-16y2uox r-1wbh5a2 r-1ny4l3l')\
                .find_all('div', class_='css-1dbjc4n r-18u37iz')[1]\
                .find('div', class_='css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu')

            post_name = post_body.find('div', class_='css-1dbjc4n r-zl2h9q')\
                .find('div', class_='css-1dbjc4n r-k4xj1c r-18u37iz r-1wtj0ep')\
                .find('div', class_='css-1dbjc4n r-1d09ksm r-18u37iz r-1wbh5a2')\
                .find('div', class_='css-1dbjc4n r-1wbh5a2 r-dnmrzs r-1ny4l3l')\
                .find('div', class_='css-1dbjc4n r-1awozwy r-18u37iz r-1wbh5a2 r-dnmrzs r-1ny4l3l')  \
                .find('div', class_='css-1dbjc4n r-1awozwy r-18u37iz r-1wbh5a2 r-dnmrzs')\
                .find('div', class_='css-1dbjc4n r-1wbh5a2 r-dnmrzs')\
                .find('a', class_='css-4rbku5 css-18t94o4 css-1dbjc4n r-1loqt21 r-1wbh5a2 r-dnmrzs r-1ny4l3l')\
                .find('div', class_='css-1dbjc4n r-1awozwy r-18u37iz r-1wbh5a2 r-dnmrzs')\
                .find('div', class_='css-901oao r-1awozwy r-18jsvk2 r-6koalj r-37j5jr r-a023e6 r-b88u0q r-rjixqe r-bcqeeo r-1udh08x r-3s2u2q r-qvutc0')\
                .find('span', class_='css-901oao css-16my406 css-1hf3ou5 r-poiln3 r-bcqeeo r-qvutc0')\
                .find('span', class_='css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0').text
            # print(post_name)

            try:
                post_time = post_body.find('div', class_='css-1dbjc4n r-zl2h9q')\
                .find('div', class_='css-1dbjc4n r-k4xj1c r-18u37iz r-1wtj0ep')\
                .find('div', class_='css-1dbjc4n r-1d09ksm r-18u37iz r-1wbh5a2')\
                .find('div', class_='css-1dbjc4n r-1wbh5a2 r-dnmrzs r-1ny4l3l')\
                .find('div', class_='css-1dbjc4n r-1awozwy r-18u37iz r-1wbh5a2 r-dnmrzs r-1ny4l3l')  \
                .find('div', class_='css-1dbjc4n r-18u37iz r-1wbh5a2 r-13hce6t')\
                .find('div', class_='css-1dbjc4n r-1d09ksm r-18u37iz r-1wbh5a2')\
                .find('div', class_='css-1dbjc4n r-18u37iz r-1q142lx')\
                .find('a', class_='css-4rbku5 css-18t94o4 css-901oao r-14j79pv r-1loqt21 r-xoduu5 r-1q142lx r-1w6e6rj r-37j5jr r-a023e6 r-16dba41 r-9aw3ui r-rjixqe r-bcqeeo r-3s2u2q r-qvutc0')\
                .find('time').text
            except:
                continue
            # print(post_time)

            # print(post_body)
            post_content = post_body.find('div', class_='css-1dbjc4n')\
                .find('div', class_='css-901oao css-cens5h r-18jsvk2 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0')\
                .find('span', class_='css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0').text
            
            print(post_content)


            print("\n")

        browser.quit()

    return None

#搜尋本站貼文頁面
@app.route("/search_tictagtoe", methods=['POST'])
def search_tictagtoe():
    if request.method == 'POST':
        key = request.form['keyword']
        sql = 'select * from post;'
        cursor.execute(sql)
        results = cursor.fetchall()
        post_item = []
        for result in results:
            post_hashtag = result[7]
            if key in post_hashtag:
                poster = result[4]
                sql = f'select * from member where MemId = "{poster}";'
                cursor.execute(sql)
                member = cursor.fetchone()
                member_name = member[1]
                member_avatar = member[5]
                post_time = result[6]
                post_content = result[2]
                post_tag = extract_hashtags(result[7])
                post_img = ""
                post_vedio = ""
                post_like = 0
                post_comment = 0
                #每篇貼文的資訊
                post_detail = {
                    "post_image": member_avatar,
                    "post_name": member_name,
                    "post_time": post_time,
                    "post_text": post_content,
                    "post_picture": post_img,
                    "post_video": post_vedio,
                    "post_hashtag": post_tag,
                    "post_likes": post_like,
                    "post_comments": post_comment
                }
                #所有貼文的集合
                post_item.append(post_detail)
        data = {
            'post_item': post_item
        }
    return jsonify(**data) 

#新增好友
@app.route("/addfriend", methods=['POST'])
def AddFriend():
    # 取得MemId
    selfMemId = current_user.id
    newFriendId = request.values.get('memId')

    try:
        sql = f'INSERT INTO member_relationship VALUE ({selfMemId}, {newFriendId});'
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
    selfMemId = current_user.id
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
@app.route("/getfriendlist", methods=['GET','POST'])
def GetFriendList():
    try:
        sql = f'Select member_relationship.ObjId,MemName,ImagePath FROM member_relationship left join member on member_relationship.ObjId = member.MemId where member_relationship.MemId=\'{current_user.id}\' and member_relationship.Status>0 ;'
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        return jsonify(**{'res':'success','data':res})

    except Exception as e:
        db.rollback()
        return jsonify(**{'res':'fail','msg':str(e)})
    

#查詢會員
@app.route("/getmemlist", methods=['POST'])
def GetMemList():
    # 取得MemId
    memName = request.values.get('memName')
    try:
        sql = f'Select MemId,MemName,ImagePath FROM member where MemName=\'{memName}\';'
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        return jsonify(**{'res':'success','data':res})

    except:
        db.rollback()
        return jsonify(**{'res':'fail'})

#變更好友間狀態、關係
@app.route("/changefriendstatus", methods=['POST'])
def ChangeFriendStatus():
    # 取得MemId
    selfMemId = current_user.id
    friendId = request.values.get('memId')
    status = request.values.get('status') # 1: 正常,2: 傳送好友邀請

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
    tagType = data.get('tagType', None)
    status = data.get('status', None)
    print(tag)
    memId = current_user.id
    time = str(datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))
    timestamp = int(datetime.now().timestamp())
    tagId = str("H%s" % (timestamp))
    print(tagId)
    try:
        with db.cursor() as cursor:
            sql = f"insert into hashtag values ('{tagId}', '{tag}', {tagType}, '{memId}', {status}, '{tag}', '{time}');"
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
    memId = current_user.id
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
    memId = current_user.id
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
    memId = current_user.id
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
    memId = current_user.id
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
    memId = current_user.id
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

@app.route("/update/note", methods=['POST'])
def update_note():
    data = request.get_json()
    postId = data.get('postId', None)
    location = data.get('location', None)
    tags = data.get('tags', None)
    content = data.get('content', None)
    try:
        sql = f"update post set Content = '{content}', Hashtag = '{tags}', Location = '{location}' where DataId = '{postId}';"
        cursor.execute(sql)
        db.commit()
        return jsonify({"result": "Update successful"}), 200
    except:
        db.rollback()
        return jsonify({"result": "Update failed"}), 400

@app.route("/delete/note", methods=['POST'])
def delete_note():
    data = request.get_json()
    postId = data.get('postId', None)
    try:
        sql = f"delete from post where DataId = '{postId}';"
        cursor.execute(sql)
        db.commit()
        return jsonify({"result": "Delete successful"}), 200
    except:
        db.rollback()
        return jsonify({"result": "Delete failed"}), 400

@app.route('/add/hashtag/report', methods=['POST'])
def add_hashtag_report():
    data = request.get_json()
    tag_id = data.get('tag_id', None)
    memId = current_user.id
    time = str(datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))
    timestamp = int(datetime.now().timestamp())
    feedback_id = str("F%s" % (timestamp))
    print(feedback_id)
    try:
        sql = f"insert into feedback values ('{feedback_id}', 1, '{memId}', '{tag_id}', '', '新增的tag', '{time}');"
        cursor.execute(sql)
        db.commit()
        return jsonify({"result": "Add report successful"}), 200
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        return jsonify({"result": "Add report failed"}), 400

@app.route('/update/hashtag/status/report', methods=['POST'])
def update_hashtag_status_report():
    data = request.get_json()
    hashtagId = data.get('hashtagId', None)
    try:
        sql = f'update hashtag set Status = 2 where TagId = {hashtagId};'
        cursor.execute(sql)
        db.commit()
        return jsonify({"result": "Update successful"}), 200
    except:
        db.rollback()
        return jsonify({"result": "Update failed"}), 400

@app.route('/update/hashtag/status/accept', methods=['POST'])
def update_hashtag_status_accept():
    data = request.get_json()
    hashtagId = data.get('hashtagId', None)
    try:
        sql = f'update hashtag set Status = 1 where TagId = "{hashtagId}";'
        cursor.execute(sql)
        db.commit()
        sql = f'delete from feedback where TagId = "{hashtagId}";'
        cursor.execute(sql)
        db.commit()
        return jsonify({"result": "Update successful"}), 200
    except:
        db.rollback()
        return jsonify({"result": "Update failed"}), 400

@app.route('/update/hashtag/status/reject', methods=['DELETE'])
def update_hashtag_status_reject():
    data = request.get_json()
    hashtagId = data.get('hashtagId', None)
    try:
        sql = f'delete from hashtag where TagId = "{hashtagId}";'
        cursor.execute(sql)
        db.commit()
        sql = f'delete from feedback where TagId = "{hashtagId}";'
        cursor.execute(sql)
        db.commit()
        return jsonify({"result": "Delete successful"}), 200
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        return jsonify({"result": "Delete failed"}), 400

@app.route('/delete/hashtag', methods=['DELETE'])
def delete_hashtag():
    data = request.get_json()
    hashtagId = data.get('hashtagId', None)
    try:
        sql = f'delete from hashtag where TagId = "{hashtagId}";'
        cursor.execute(sql)
        db.commit()
        return jsonify({"result": "Delete successful"}), 200
    except:
        db.rollback()
        return jsonify({"result": "Delete failed"}), 400

@app.route('/public/hashtags', methods=['GET'])
def get_public_hashtags():
    try:
        hashtag_list = []
        sql = f'select TagName from hashtag where TagType = 4;'
        cursor.execute(sql)
        results = cursor.fetchall()
        for result in results:
            hashtag_list.append(result[0])
        return jsonify({'result': hashtag_list}), 200
    except Exception as e:
        return jsonify({'result': e}), 400

@app.route('/private/hashtags', methods=['GET'])
def get_private_hashtags():
    try:
        hashtag_list = []
        sql = f'select TagName from hashtag where TagType = 6;'
        cursor.execute(sql)
        results = cursor.fetchall()
        for result in results:
            hashtag_list.append(result[0])
        return jsonify({'result': hashtag_list}), 200
    except Exception as e:
        return jsonify({'result': e}), 400

@app.route('/check/public/hashtag', methods=['POST'])
def check_public_hashtag():
    data = request.get_json()
    tag_name = data.get('tag_name', None)
    sql = f'select * from hashtag where TagName = "{tag_name}" and TagType = 4;'
    cursor.execute(sql)
    result = cursor.fetchone()
    if result:
        return jsonify({'result': 'This hashtag already exists'})
    else:
        return jsonify({'result': 'This hashtag does not exist'})
    
@app.route('/check/private/hashtag', methods=['POST'])
def check_private_hashtag():
    data = request.get_json()
    tag_name = data.get('tag_name', None)
    sql = f'select * from hashtag where TagName = "{tag_name}" and TagType = 6;'
    cursor.execute(sql)
    result = cursor.fetchone()
    if result:
        return jsonify({'result': 'This hashtag already exists'})
    else:
        return jsonify({'result': 'This hashtag does not exist'})

@app.route('/get/public/hashtagId', methods=['POST'])
def get_public_hashtagId():
    data = request.get_json()
    tagName = data.get('tagName', None)
    try:
        with db.cursor() as cursor:
            sql = f'select * from hashtag where TagName = "{tagName}" and TagType = 4;'
            cursor.execute(sql)
            result = cursor.fetchone()
            tagId = result[0]
            print(f'tagId: {tagId}')
            return jsonify({'result': tagId})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'result': 'Error'}), 500

@app.route('/get/private/hashtagId', methods=['POST'])
def get_private_hashtagId():
    data = request.get_json()
    tagName = data.get('tagName', None)
    try:
        with db.cursor() as cursor:
            sql = f'select * from hashtag where TagName = "{tagName}" and TagType = 6;'
            cursor.execute(sql)
            result = cursor.fetchone()
            tagId = result[0]
            print(f'tagId: {tagId}')
            return jsonify({'result': tagId})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'result': 'Error'}), 500

@app.route('/add/hashtag/relationship', methods=['POST'])
def add_hashtag_relationship():
    data = request.get_json()
    tagId = data.get('tagId', None)
    dataId = data.get('dataId', None)
    time = str(datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))
    try:
        with db.cursor() as cursor:
            sql = f"insert into `hashtag_relationship` (`TagId`, `ObjId`, `RelationshipType`, `Status`, `CreateTime`) values ('{tagId}', '{dataId}', 2, 1, '{time}');"
            cursor.execute(sql)
        db.commit()
        return jsonify({'result': 'Add suceessful'}), 200
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        return jsonify({'result': 'Add failed'}), 400

@app.route('/add/note', methods=['POST'])
def add_note():
    data = request.get_json()
    memId = current_user.id
    title = data.get('title', None)
    location = data.get('location', None)
    member = data.get('member', None)
    content = data.get('content', None)
    tag = data.get('tag', None)

    print('#########################')
    print(tag)
    print('#########################')
    time = str(datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))
    timestamp = int(datetime.now().timestamp())
    postId = str("P%s" % (timestamp))
    try:
        sql = f"INSERT INTO `post` (`DataId`, `Title`, `Content`, `PostType`, `Owner`, `Status`, `CreateTime`, `Hashtag`, `Location`, `MemAtId`) VALUES ('{postId}', '{title}', '{content}', 5, '{memId}', 1, '{time}', '{tag}', '{location}', '{member}');"
        cursor.execute(sql)
        db.commit()

        
        return jsonify({'result': 'Add successful', 'postId': postId}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'result': 'Add failed'}), 400

############################## fetch ##############################


if __name__ == '__main__':
    app.run('0.0.0.0',port=8082,debug=True)


# 程式結束時釋放資料庫資源
cursor.close()
db.close()  # 關閉連線


