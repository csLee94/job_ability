from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pymysql
import time 
import random
import os
import re

def cleanText(readData):
    text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》•]', '', readData)
    return text


mysql = pymysql.connect(host='3.36.66.213', port=50270, user='lcs', password='lcs', db='JOB', charset='utf8mb4', autocommit=True)
cursor = mysql.cursor(pymysql.cursors.DictCursor)

flst = []
cursor.execute("SELECT code_details, ID_num FROM Flyers")
data = cursor.fetchall()
for infor in data:
    temp = [infor['code_details'], infor['ID_num']]
    flst.append(temp)    

cursor.execute("SELECT * FROM Fail_Crawling")
data_fail = cursor.fetchall()
target_xpath = "/html/body/div[1]/div/div[3]/div[1]/div[1]/div[1]/div[2]/section[1]/p[%s]/span"
query_insert = "INSERT INTO Flyers VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')"

#-- 크롬드라이버 설정 
chrome_option = Options() #초기화
# chrome_option.add_argument("headless") # 창 없는 모드
path = os.getcwd() # 설치한 Chromdriver 절대 경로설정
driver   = webdriver.Chrome(path+'/chromedriver.exe', chrome_options= chrome_option) # driver 선언


for infor in data_fail:
    code_d = str(infor['code_d'])
    id_position = str(infor['ID_num'])
    Company_nm = str(infor['Company_nm'])
    Flyer_title = str(infor['Flyer_title'])
    temp = [code_d, id_position]

    if temp in flst:
        cursor.execute("DELETE FROM Fail_Crawling WHERE code_d=%s AND ID_num=%s" % (code_d, id_position))
        print("삭제 완료")
    else:
        try:
            driver.get(infor['url'])
            time.sleep(5)
            maintask=cleanText(driver.find_element_by_xpath(target_xpath % "2").text)
            qual1=cleanText(driver.find_element_by_xpath(target_xpath % "3").text)
            qual2=cleanText(driver.find_element_by_xpath(target_xpath % "4").text)
            cursor.execute(query_insert % (code_d, id_position, maintask, qual1, qual2, Company_nm, Flyer_title))
            time.sleep(1)
            cursor.execute("DELETE FROM Fail_Crawling WHERE code_d='%s' AND ID_num='%s'" % (code_d, id_position))
            print("등록 및 삭제 완료: %s" % infor['url'])
        except:
            time.sleep(3)
            maintask=cleanText(driver.find_element_by_xpath(target_xpath % "2").text)
            maintask = maintask.rstrip('\ ')
            qual1=cleanText(driver.find_element_by_xpath(target_xpath % "3").text)
            qual1 = qual1.rstrip('\ ')
            qual2=cleanText(driver.find_element_by_xpath(target_xpath % "4").text)
            qual2 = qual2.rstrip('\ ')
            print(query_insert % (code_d, id_position, maintask, qual1, qual2, Company_nm, Flyer_title))
            cursor.execute(query_insert % (code_d, id_position, maintask, qual1, qual2, Company_nm, Flyer_title))
            time.sleep(1)
            cursor.execute("DELETE FROM Fail_Crawling WHERE code_d='%s' AND ID_num='%s'" % (code_d, id_position))
            print("등록 및 삭제 완료: %s" % infor['url'])



mysql.close()

