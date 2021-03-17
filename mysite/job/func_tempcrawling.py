from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pymysql
import time 
import random
import os

#-- URL Code Dict 설정
mysql = pymysql.connect(host='13.125.250.249', port=59425, user='lcs', password='lcs', db='tempdb', charset='utf8mb4', autocommit=True)
cursor = mysql.cursor(pymysql.cursors.DictCursor)
# data 변수에 직군 분류 코드 저장(중복 검사)
cursor.execute("Select * from test_F")
data = cursor.fetchall() 
idlst = []
for infor in data:
    idlst.append(infor['ID'])

query_insert = "INSERT INTO test_F VALUES ('%s', '%s', '%s', '%s', '%s')"


#-- 크롬드라이버 설정 
chrome_option = Options() #초기화
# chrome_option.add_argument("headless") # 창 업는 모드
path = os.getcwd() # 설치한 Chromdriver 절대 경로설정
driver  = webdriver.Chrome(path+'/chromedriver.exe', chrome_options= chrome_option) # driver 선언
driver2  = webdriver.Chrome(path+'/chromedriver.exe', chrome_options= chrome_option) # driver 선언


#-- 페이지 연결 및 페이지 이동/검색에 필요한 변수들
home_link_1 = "https://www.wanted.co.kr/wdlist/%s"
home_link_2 = "https://www.wanted.co.kr/wdlist/%s/%s"
basic_xpath = "/html/body/div[1]/div/div[3]/div[2]/div/ul/li[%s]/div/a"
target_xpath = "/html/body/div[1]/div/div[3]/div[1]/div[1]/div[1]/div[2]/section[1]/p[%s]/span"
SCROLL_PAUSE_TIME = 2

testdict =[ {'code_parent':'999', 'code_details':'10057'}, {'code_parent':'510', 'code_details':'10126'}]

for infor in testdict: #data
    code_p = infor['code_parent']
    code_d = infor['code_details']
    # URL 유형 선택
    if code_p == '999':
        list_link = home_link_1 % code_d
    elif code_p != '999':
        list_link = home_link_2 % (code_p, code_d)
    # page 열기
    driver.get(list_link)
    # page scroll 
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
    
    page_len = len(driver.find_elements_by_class_name('_3D4OeuZHyGXN7wwibRM5BJ'))  # 페이지 내 채용공고 수

    for i in range(3): #page_len
        elements = driver.find_element_by_xpath(basic_xpath % str(i+1))
        # 필요 정보 = [링크, 공고ID, 회사명, 공고명]
        url_position = elements.get_attribute('href')
        id_position = elements.get_attribute('data-position-id')
        company_name = elements.get_attribute('data-company-name')
        position_name = elements.get_attribute('data-position-name')
        if id_position in idlst: # DB에 있는 경우 패스
            pass
        else:
            # 채용 공고 페이지 이동
            driver2.get(url_position)

            try:
                maintask = driver2.find_element_by_xpath(target_xpath % "2").text
                qual1 = driver2.find_element_by_xpath(target_xpath % "3").text
                qual2 = driver2.find_element_by_xpath(target_xpath % "4").text
                cursor.execute(query_insert % (code_d, id_position, maintask, qual1, qual2))
                print("data is registered!")
                time.sleep(random.randrange(1,5))
            except:
                time.sleep(5)
                driver2.get(driver2.current_url)
                maintask = driver2.find_element_by_xpath(target_xpath % "2").text
                qual1 = driver2.find_element_by_xpath(target_xpath % "3").text
                qual2 = driver2.find_element_by_xpath(target_xpath % "4").text
                cursor.execute(query_insert % (code_d, id_position, maintask, qual1, qual2))
                print("data is registered!")
                time.sleep(random.randrange(1,5))
                
        time.sleep(10)

mysql.close()