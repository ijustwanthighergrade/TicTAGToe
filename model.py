import pymysql

config = {
    'host':'localhost',
    'port':3306,
    'user':'root',
    'passwd':'1234',
    'db':'tictagtoe',
    'charset':'utf8mb4',
    # 資料庫內容以字典格式輸出
    #'cursorclass':pymysql.cursors.DictCursor,
}

# 連接資料庫
def Mysql():
    # 連接資料庫
    #db = pymysql.connect(host="localhost", port=3306, user="root", passwd="root", db="Geek_Web", charset="utf8mb4")
    db = pymysql.connect(**config)
    #cursor()方法獲取操作游標 
    cursor = db.cursor()
 
    try:
        print('success')
        return (db, cursor)
 
    except:
        print("資料庫訪問失敗") 
                     

