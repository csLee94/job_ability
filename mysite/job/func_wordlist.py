import pymysql

##########################################################################
#-- DB 연결
##########################################################################
mysql = pymysql.connect(host='15.164.96.251', port=54258, user='lcs', password='lcs', db='JOB', charset='utf8mb4', autocommit=True)
cursor = mysql.cursor(pymysql.cursors.DictCursor)

cursor.execute('truncate NUM_Words')
cursor.execute('SELECT code_details from Code_details')

code_data = cursor.fetchall()
code_list = [infor['code_details'] for infor in code_data]

for code in code_list:
    cursor.execute("SELECT word, count(word) FROM testword WHERE code_details=%s GROUP BY word ORDER by count(word) DESC LIMIT 100" % code)
    data = cursor.fetchall()
    for infor in data:
        cursor.execute("INSERT INTO NUM_Words VALUES ('%s', '%s', '%s')" % (code, infor['word'], infor['count(word)']))


mysql.close()