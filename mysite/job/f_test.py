from datetime import datetime 
from datetime import timedelta
import pymysql
import time

# 실패한 URL 다시 불러와서 list 만들고 재시도 & 재시도 한 목록 삭제
mysql = pymysql.connect(host='3.36.114.246', port=51368, user='lcs', password='lcs', db='tempdb', charset='utf8mb4', autocommit=True)
cursor = mysql.cursor(pymysql.cursors.DictCursor)



query = "INSERT INTO Fail_crawling VALUES ('temp_%s', '%s')"
for i in range(10):
    strtime = str(datetime.now() + timedelta(days=-i))
    cursor.execute(query % (str(i), strtime))
    cursor.execute("INSERT INTO Fail_crawling VALUES ('temp_20', '%s')" % str(datetime.now() + timedelta(days=2)))
start_retry = datetime.now()
time.sleep(10)
cursor.execute('SELECT * FROM Fail_crawling')
data = cursor.fetchall()

for i in range(10):
    if i % 2 == 0:
        infor = data[i]
        url = infor['url']
        cursor.execute("INSERT INTO Fail_crawling VALUES ('%s', '%s')" % ('temp', str(datetime.now())))
    else: 
        pass

print("SELECT * FROM Fail_crawling WHERE time < '%s'" % str(start_retry))
cursor.execute("DELETE FROM Fail_crawling WHERE time < '%s'" % str(start_retry))
tempdata = cursor.fetchall()
print(len(tempdata))

mysql.close()
