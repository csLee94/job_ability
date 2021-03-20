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
mysql = pymysql.connect(host='3.34.135.34', port=56351, user='lcs', password='lcs', db='JOB', charset='utf8mb4', autocommit=True)
cursor = mysql.cursor(pymysql.cursors.DictCursor)
query_insert = "INSERT INTO Flyers VALUES ('%s', '%s', '%s', '%s', '%s','%s', '%s')"

#-- 크롬드라이버 설정 
chrome_option = Options() #초기화
# chrome_option.add_argument("headless") # 창 없는 모드
path = os.getcwd() # 설치한 Chromdriver 절대 경로설정
target_xpath = "/html/body/div[1]/div/div[3]/div[1]/div[1]/div[1]/div[2]/section[1]/p[%s]/span"

# 채용 공고 페이지 이동
driver2  = webdriver.Chrome(path+'/chromedriver.exe', chrome_options= chrome_option) # driver 선언
driver2.get('https://www.wanted.co.kr/wd/56822')

code_d = '873'
id_position ='temp'
company_name ='t2'
position_name = 't3'

for tmpnm in range(1,3):
    driver2.execute_script("window.scrollTo(0,%s)" % str(300*tmpnm))
    time.sleep(1)    
maintask = cleanText(driver2.find_element_by_xpath(target_xpath % "2").text)
qual1 = cleanText(driver2.find_element_by_xpath(target_xpath % "3").text)
qual2 = cleanText(driver2.find_element_by_xpath(target_xpath % "4").text)
cursor.execute(query_insert % (code_d, id_position, maintask, qual1, qual2, company_name, position_name))

mysql.close()
driver2.close()
# time.sleep(random.randrange(1,5)).