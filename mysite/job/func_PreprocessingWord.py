import pymysql
from konlpy.tag import Okt
from konlpy.tag import Kkma
import re
import pymysql

##########################################################################
#-- 함수 & 변수 설정
##########################################################################
# 특수문자 제거 함수
def cleanText(readData):
    text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》•]', '', readData)
    return text

# Nltk를 위한 한국어 삭제 함수
def del_korean(text):
    txt = text 
    hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
    result=hangul.findall(txt)
    return result

# 한국어 전처리를 위한 okt 호출
okt = Okt()
# 한국어 불용어 불러오기
with open("stopword_korean.txt", "r", encoding="utf-8") as stopword_korean_file:
    stopword_korean = stopword_korean_file.read()
    stopword_korean = stopword_korean.split(',')
    

##########################################################################
#-- DB 연결
##########################################################################
mysql = pymysql.connect(host='3.35.0.250', port=55614, user='lcs', password='lcs', db='JOB', charset='utf8mb4', autocommit=True)
cursor = mysql.cursor(pymysql.cursors.DictCursor)
# 채용 공고 불러오기
cursor.execute("SELECT * FROM Flyers LIMIT 5")
data = cursor.fetchall()
mysql.close() # DB 적입 시 삭제 



##########################################################################
#-- 단어 전처리
##########################################################################
for infor in data:
    tlst=[]
    for tempcol in ['Maintask', 'Qual', 'Pre_Qual']:
        txt = cleanText(infor[tempcol])
        for tempword in okt.pos(txt):
            if tempword[1] in ['Noun', 'Adjective']: # 명사 & 형용사 추출
                if len(tempword[0]) > 1: # 한 글자 삭제
                    if tempword[0] not in stopword_korean: # 불용어 제거
                        tlst.append(tempword[0])
    
    print('%s | %s: ' % (infor['code_details'], infor['ID_num']),tlst)
    print('#'*80)