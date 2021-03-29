import re
from konlpy.tag import Okt # 한글용
from konlpy.tag import Kkma 

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

import pymysql
from collections import Counter

def del_korean(text):
    txt = text 
    hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
    result=hangul.findall(txt)
    if len(result) > 0:
        return str(result[0])
    elif len(result) == 0:
        return ""

def cleanText(readData):
    text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》•]', '', readData)
    return text

def unique_value(lst):
    temp_set = set(lst)
    result = list(temp_set)
    return result

# 한국어 불용어 불러오기
with open("stopword_korean.txt", "r", encoding="utf-8") as stopword_korean_file:
    stopword_korean = stopword_korean_file.read()
    stopword_korean = stopword_korean.split(',')

stopword_eng = set(stopwords.words('english'))

##########################################################################
#-- DB 연결
##########################################################################
mysql = pymysql.connect(host='13.125.126.170', port=57910, user='lcs', password='lcs', db='JOB', charset='utf8mb4', autocommit=True)
cursor = mysql.cursor(pymysql.cursors.DictCursor)
# 채용 공고 불러오기
cursor.execute("SELECT * FROM Flyers")
data = cursor.fetchall()
mysql.close()


okt = Okt()
kkma = Kkma()

okt_lst =[]
kkma_lst=[]
nltk_lst =[]
wn = 0 #삭제
sn = 0 #삭제
tn = len(data)*3

for infor in data:
    for col in ['Maintask', 'Qual', 'Pre_Qual']:
        txt = cleanText(infor[col])
        # okt
        try:
            for tempword in okt.pos(txt):
                if tempword[1] in ['Noun', 'Adjective']: # 명사 & 형용사 추출
                    if len(tempword[0]) > 1: # 한 글자 삭제
                        if tempword[0] not in stopword_korean: # 불용어 제거
                            okt_lst.append(tempword[0])
                            okt_lst = unique_value(okt_lst)
            # kkma
            for tempword in kkma.pos(txt):
                if tempword[1] in ['NNG', 'NNP', 'OL']: # 명사 & 형용사 추출
                    if len(tempword[0]) > 1: # 한 글자 삭제
                        if tempword[1] == 'OL': #영어일 경우
                            if tempword[0] not in stopword_eng: # 불용어 제거
                                kkma_lst.append(tempword[0])
                        else:
                            if tempword[0] not in stopword_korean: # 불용어 제거
                                kkma_lst.append(tempword[0])
                        kkma_lst = unique_value(kkma_lst)  
            #nltk
            for tempword in word_tokenize(txt):
                tempword = del_korean(tempword)
                if len(tempword) > 1:
                    nltk_lst.append(tempword)
                    nltk_lst = unique_value(nltk_lst)
            sn += 1 #삭제
            ratio = int((sn/tn)*100) #삭제
            print("Complete: %d / %d | 진행률: %d" % (sn, tn, ratio) +'%') #삭제
        except:
            wn += 1 #삭제
            print("Something is wrong: %d" % wn) #삭제


remove_lst =[]
for txt in kkma_lst:
    if txt in nltk_lst:
        remove_lst.append(txt)

for txt in remove_lst:
    kkma_lst.remove(txt)
        
init_user_corpus = open('corpus.txt', 'a', encoding='utf8')
for txt in kkma_lst:
    if txt not in okt_lst:
        init_user_corpus.write(txt+'\n')
init_user_corpus.close()



