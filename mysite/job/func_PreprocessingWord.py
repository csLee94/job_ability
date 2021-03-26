import pymysql
from konlpy.tag import Okt # 한글용
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
# nltk.download('stopwords')
# nltk.download('punkt')
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
    
# 영어 불용어 불러오기 
stopword_eng = set(stopwords.words('english'))

##########################################################################
#-- DB 연결
##########################################################################
mysql = pymysql.connect(host='15.164.102.130', port=55677, user='lcs', password='lcs', db='JOB', charset='utf8mb4', autocommit=True)
cursor = mysql.cursor(pymysql.cursors.DictCursor)
# 채용 공고 불러오기
cursor.execute("SELECT * FROM Flyers LIMIT 5")
data = cursor.fetchall()
# mysql.close() # DB 적입 시 삭제 



##########################################################################
#-- 단어 전처리
##########################################################################
for infor in data:
    code_details = infor['code_details']
    for tempcol in ['Maintask', 'Qual', 'Pre_Qual']:
        txt = cleanText(infor[tempcol])
        # okt를 이용한 한국어 낱말 분리
        for tempword in okt.pos(txt):
            if tempword[1] in ['Noun', 'Adjective']: # 명사 & 형용사 추출
                if len(tempword[0]) > 1: # 한 글자 삭제
                    if tempword[0] not in stopword_korean: # 불용어 제거
                        # cursor.execute("INSERT INTO testword VALUES ('%s', '%s')" % (code_details, tempword[0]))
                        print("okt: ",tempword[0])
        # 영어 분리
        for tempword in word_tokenize(txt):
            if tempword not in stopword_eng: # 불용어 제거
                if len(tempword) >1: # 한  글자 단어 삭제
                    tempword = del_korean(tempword)
                    if len(tempword) > 0:
                        print("nltk:",tempword[0])
                      # curosr.execute("INSERT INTO testword VALUES ('%s', '%s')" % (code_details, tempword))
                    

mysql.close()

