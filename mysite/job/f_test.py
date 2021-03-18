from datetime import datetime 
import pymysql
import time

# 실패한 URL 다시 불러와서 list 만들고 재시도 & 재시도 한 목록 삭제
mysql = pymysql.connect(host='3.35.230.239', port=58747, user='lcs', password='lcs', db='tempdb', charset='utf8mb4', autocommit=True)
cursor = mysql.cursor(pymysql.cursors.DictCursor)
# cursor.execute('SELECT * FROM Fail_crawling')
# data = cursor.fetchall()

start_retry = datetime.now()
time.sleep(5)

for i in range(2):
    cursor.execute("INSERT INTO testemp VALUES ('%s')" % str(datetime.now()))
    time.sleep(2)

cursor.execute("SELECT * FROM testemp where time < '%s'" % str(start_retry))
data2 = cursor.fetchall()
print(len(data2))
    



mysql.close()