from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time 
import pymysql
import re

def cleanText(readData): 
    #텍스트에 포함되어 있는 특수 문자 제거 
    text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》•]', '', readData) 
    return text

#-- URL Code Dict 설정
mysql = pymysql.connect(host='13.124.250.48', port=51747, user='lcs', password='lcs', db='JOB', charset='utf8mb4', autocommit=True)
cursor = mysql.cursor(pymysql.cursors.DictCursor)

cursor.execute("SELECT * FROM temp_fail")
data = cursor.fetchall()
mysql.close()

tlst = []
for infor in data:
    t1 = infor['t1']
    t2 = infor['t2']
    tlst.append([t1, t2])


tlst2= [['1606,555'],['723','56271'],['727','56271'],['1651','654'],['56271', '727']]
i = 1
for infor in tlst2:
    if infor in tlst:
        print("%d번 중복" % i)
        i += 1
    else:
        i += 1


