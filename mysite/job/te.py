import pymysql
import pandas as pd

#-- URL Code Dict 설정
mysql = pymysql.connect(host='52.79.243.255', port=54092, user='lcs', password='lcs', db='JOB', charset='utf8mb4', autocommit=True)
cursor = mysql.cursor(pymysql.cursors.DictCursor)

cursor.execute("SELECT * FROM Code_details")
data_code = cursor.fetchall()
lst_code = [infor['code_details'] for infor in data_code]
query = "select name_details, word, count from NUM_Words inner join Code_details on NUM_Words.code_details = Code_details.code_details where Code_details.code_details=%s limit 5;"

df = pd.DataFrame()
for code in lst_code:
    cursor.execute(query % code)
    data = cursor.fetchall()
    tdf = pd.DataFrame(data)
    df = pd.concat([df,tdf])

df.to_excel("./temp.xlsx")