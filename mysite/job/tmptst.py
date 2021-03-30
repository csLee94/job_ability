import pymysql 
import pandas as pd

mysql = pymysql.connect(host='3.34.91.54', port=55634, user='lcs', password='lcs', db='JOB', charset='utf8mb4', autocommit=True)
cursor = mysql.cursor(pymysql.cursors.DictCursor)

cursor.execute("SELECT * FROM Code_details")
code_data = cursor.fetchall()

code_lst = [infor['code_details'] for infor in code_data]

df = pd.DataFrame()
for code in code_lst:
    cursor.execute("SELECT * FROM NUM_Words WHERE code_details=%s" % code)
    data = cursor.fetchall()
    tmpdf = pd.DataFrame(data)
    df = pd.concat([df,tmpdf])

df.to_excel('./temp.xlsx')

