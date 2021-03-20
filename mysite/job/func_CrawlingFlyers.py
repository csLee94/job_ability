from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pymysql
import time 
import random
import os
from datetime import datetime
import re

def cleanText(readData):
    text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》•]', '', readData)
    return text

#-- URL Code Dict 설정
mysql = pymysql.connect(host='3.34.135.34', port=56351, user='lcs', password='lcs', db='JOB', charset='utf8mb4', autocommit=True)
cursor = mysql.cursor(pymysql.cursors.DictCursor)
# data 변수에 직군 분류 코드 저장(중복 검사)
cursor.execute("Select * from Flyers")
data_id = cursor.fetchall() 
idlst = []
for infor in data_id:
    idlst.append(infor['ID_num'])

query_insert = "INSERT INTO Flyers VALUES ('%s', '%s', '%s', '%s', '%s','%s', '%s')"
suc_nm = 1
fail_nm = 1

#-- 크롬드라이버 설정 
chrome_option = Options() #초기화
chrome_option.add_argument("headless") # 창 없는 모드
path = os.getcwd() # 설치한 Chromdriver 절대 경로설정
driver   = webdriver.Chrome(path+'/chromedriver.exe', chrome_options= chrome_option) # driver 선언
driver2  = webdriver.Chrome(path+'/chromedriver.exe', chrome_options= chrome_option) # driver 선언


#-- 페이지 연결 및 페이지 이동/검색에 필요한 변수들
home_link_1 = "https://www.wanted.co.kr/wdlist/%s"
home_link_2 = "https://www.wanted.co.kr/wdlist/%s/%s"
basic_xpath = "/html/body/div[1]/div/div[3]/div[2]/div/ul/li[%s]/div/a"
target_xpath = "/html/body/div[1]/div/div[3]/div[1]/div[1]/div[1]/div[2]/section[1]/p[%s]/span"
SCROLL_PAUSE_TIME = 2

cursor.execute("Select * from Code_details")
data_code = cursor.fetchall() 

for infor in data_code:
    code_p = infor['code_parent']
    code_d = infor['code_details']
    if code_p == '999':
        list_link = home_link_1 % code_d
    elif code_p != '999':
        list_link = home_link_2 % (code_p, code_d)

    driver.get(list_link)
    #-- page scroll 
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

    for i in range(page_len):
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
                time.sleep(1)
                maintask = cleanText(driver2.find_element_by_xpath(target_xpath % "2").text)
                qual1 = cleanText(driver2.find_element_by_xpath(target_xpath % "3").text)
                qual2 = cleanText(driver2.find_element_by_xpath(target_xpath % "4").text)
                cursor.execute(query_insert % (code_d, id_position, maintask, qual1, qual2, company_name, position_name))
                print("data is registered!: 총 %d개" % suc_nm) # 필요없을 때 삭제
                suc_nm += 1
                time.sleep(random.randrange(1,3))
            except:
                try:
                    driver2.get(driver2.current_url)   
                    time.sleep(3)
                    maintask = cleanText(driver2.find_element_by_xpath(target_xpath % "2").text)
                    qual1 = cleanText(driver2.find_element_by_xpath(target_xpath % "3").text)
                    qual2 = cleanText(driver2.find_element_by_xpath(target_xpath % "4").text)
                    cursor.execute(query_insert % (code_d, id_position, maintask, qual1, qual2, company_name, position_name))
                    print("data is registered!: 총 %d개" % suc_nm) # 필요없을 때 삭제
                    suc_nm += 1
                    time.sleep(random.randrange(1,3))
                except:
                    fail_url = driver2.current_url
                    cursor.execute("INSERT INTO Fail_Crawling VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (code_d, id_position, fail_url, company_name, position_name, str(datetime.now())))
                    print("Failed data: 총 %d개" % fail_nm)
                    fail_nm += 1 
                    time.sleep(5)
        


# 실패한 데이터 재수집 
# now = datetime.now() # 시작 시간
cursor.execute('SELECT * FROM Fail_Crawling')
data_fail = cursor.fetchall()

for infor in data_fail:
    try:
        code_d = infor['code_d']
        id_position = infor['ID_num']
        company_name = infor['Company_nm']
        position_name = infor['Flyer_title']
        url = infor['url']
        driver2.get(url)
        time.sleep(5)
        maintask = cleanText(driver2.find_element_by_xpath(target_xpath % "2").text)
        qual1 = cleanText(driver2.find_element_by_xpath(target_xpath % "3").text)
        qual2 = cleanText(driver2.find_element_by_xpath(target_xpath % "4").text)
        cursor.execute(query_insert % (code_d, id_position, maintask, qual1, qual2, company_name, position_name))
        time.sleep(1)
    except:
        try:
            driver2.get(url)  
            time.sleep(7)
            maintask = cleanText(driver2.find_element_by_xpath(target_xpath % "2").text)
            qual1 = cleanText(driver2.find_element_by_xpath(target_xpath % "3").text)
            qual2 = cleanText(driver2.find_element_by_xpath(target_xpath % "4").text)
            cursor.execute(query_insert % (code_d, id_position, maintask, qual1, qual2, company_name, position_name))
            cursor.execute("DELETE FROM Fail_Crawling where ID_num = '%s'" % id_position)
            time.sleep(1)
        except:
            pass
            # cursor.execute("INSERT INTO Fail_crawling VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (code_d, id_position, fail_url, company_name, position_name, str(datetime.now())))
            # print("Failed data: 총 %d개" % fail_nm)

mysql.close()