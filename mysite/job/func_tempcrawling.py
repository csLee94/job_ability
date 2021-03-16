from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time 
import random 
import pymysql 

#-- URL Code Dict 설정
mysql = pymysql.connect(host='3.34.188.141', port=57825, user='lcs', password='lcs', db='tempdb', charset='utf8mb4', autocommit=True)
cursor = mysql.cursor(pymysql.cursors.DictCursor)
cursor.execute("Select * from Code_details")
data = cursor.fetchall() # data 변수에 직군 분류 코드 저장
query_insert = "INSERT INTO test_F VALUES ('%s', '%s', '%s', '%s', '%s')"
code_d = '648'

#-- 크롬드라이버 설정 
chrome_option = Options() #초기화
# chrome_option.add_argument("headless") # 창 업는 모드
path = os.getcwd() # 설치한 Chromdriver 절대 경로설정
driver  = webdriver.Chrome(path+'/chromedriver.exe', chrome_options= chrome_option) # driver 선언
driver2 = webdriver.Chrome(path+'/chromedriver.exe', chrome_options= chrome_option) # driver 선언
basic_link = 'https://www.wanted.co.kr/wdlist/517/648'
basic_xpath = '/html/body/div[1]/div/div[3]/div[2]/div/ul/li[%s]/div/a'
driver.get(basic_link)


SCROLL_PAUSE_TIME = 2
#마지막 시점의 창 높이 저장
last_height =driver.execute_script("return document.body.scrollHeight")
while True:
    #scroll down to bottom 
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #wait to load page
    time.sleep(SCROLL_PAUSE_TIME)
    #마지막 창 로딩을 위해 살짝 스크롤 올리기
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight-50);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    #새로운 높이가 이전 높이와 변하지 않았으면 스크롤 종료
    if new_height == last_height:
        break

    last_height = new_height

page_len = len(driver.find_elements_by_class_name('_3D4OeuZHyGXN7wwibRM5BJ'))
target_xpath = "/html/body/div[1]/div/div[3]/div[1]/div[1]/div[1]/div[2]/section[1]/p[%s]/span"
                
for i in range(5):
    try:
        elements = driver.find_element_by_xpath(basic_xpath % str(i+1))
        url_position = elements.get_attribute('href')
        id_position = elements.get_attribute('data-position-id')
        company_name = elements.get_attribute('data-company-name')
        position_name = elements.get_attribute('data-position-name')
        driver2.get(url_position)
        maintask = driver2.find_element_by_xpath(target_xpath % "2").text
        qual1 = driver2.find_element_by_xpath(target_xpath % "3").text
        qual2 = driver2.find_element_by_xpath(target_xpath % "4").text
        cursor.execute(query_insert % (code_d, id_position, maintask, qual1, qual2))
        print("data is registered!")
        time_nm = random.randrange(1,5)
        time.sleep(time_nm)
    except:
        driver2.get(driver2.current_url)
        time.sleep(5)
        maintask = driver2.find_element_by_xpath(target_xpath % "2").text
        qual1 = driver2.find_element_by_xpath(target_xpath % "3").text
        qual2 = driver2.find_element_by_xpath(target_xpath % "4").text
        cursor.execute(query_insert % (code_d, id_position, maintask, qual1, qual2))
        print("data is registered!")
        time_nm = random.randrange(1,5)
        time.sleep(time_nm)

mysql.close()