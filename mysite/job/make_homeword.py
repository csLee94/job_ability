import pymysql 
import pandas as pd

mysql = pymysql.connect(host='52.79.243.255', port=54092, user='lcs', password='lcs', db='JOB', charset='utf8mb4', autocommit=True)
cursor = mysql.cursor(pymysql.cursors.DictCursor)

cursor.execute("SELECT * FROM Code_details")
code_data = cursor.fetchall()

code_lst = [infor['code_details'] for infor in code_data]
home_word = open('./home_word.txt', 'a')
html_code = '''
        <div class="row">
            <div class="col-4" style="color: #800080; font-weight: bold;">
                %s
            </div>
            <div class="col-sm">
                %s
            </div>
            <div class="col-sm">
                %s
            </div>
            <div class="col-sm">
                %s
            </div>
            <div class="col-sm">
                %s
            </div>
            <div class="col-sm">
                %s
            </div>
        </div>
        '''

query = "select name_details, word, count from NUM_Words inner join Code_details on NUM_Words.code_details = Code_details.code_details where Code_details.code_details=%s limit 5;"

df = pd.DataFrame()
for code in code_lst:
    cursor.execute(query % code)
    data = cursor.fetchall()
    word_lst=[]
    for infor in data:
        name = infor['name_details']
        word_lst.append(infor['word'])
    try:
        home_word.write(html_code % (name, word_lst[0], word_lst[1], word_lst[2], word_lst[3], word_lst[4]))
    except:
        pass
    tmpdf = pd.DataFrame(data)
    df = pd.concat([df,tmpdf])

home_word.close()
df.to_excel('./homeword.xlsx')

