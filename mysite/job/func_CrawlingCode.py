from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import pymysql


#-- 크롬드라이버 설정 
chrome_option = Options() #초기화
chrome_option.add_argument("headless") # 창 없는 모드
path = os.getcwd() # 설치한 Chromdriver 절대 경로설정
driver  = webdriver.Chrome(path+'/chromedriver.exe', chrome_options= chrome_option) # driver 선언

#-- 임시 페이지 연결
driver.get('file:///C:/Users/LCS/Documents/Project/99.Personal_JobAbility/code.html') # 임시 페이지 절대 경로

#-- 저장할 DB 연결
mysql = pymysql.connect(host='3.34.97.206', port=58997, user='lcs', password='lcs', db='tempdb', charset='utf8mb4', autocommit=True)
cursor = mysql.cursor(pymysql.cursors.DictCursor)
query_1 = 'INSERT INTO Code_parent VALUES ("%s", "%s")'
query_2 = 'INSERT INTO Code_details VALUES ("%s", "%s", "%s")'

# 주요 직군 코드 
for i in range(1, 12):
    xp_home = '/html/body/div/div/div/div[%s]/a[%s]'
    for j in range(1, 10):
        try:
            elements = driver.find_element_by_xpath(xp_home % (str(i), str(j)))
            elements_href = elements.get_attribute('href')
            elements_split = elements_href.split('/wdlist')[-1]
            num = len(elements_split.split('/'))
            if num == 2:
                code_num = elements_split.split('/')[-1]
                xp_name = xp_home % (str(i), str(j)) + '/h2'
                code_name = driver.find_element_by_xpath(xp_name).text
                cursor.execute(query_1 % (code_num, code_name))
            elif num ==3:
                code_num = elements_split.split('/')[-2]
                code_details_num = elements_split.split('/')[-1]
                xp_name = xp_home % (str(i), str(j)) + '/h3'
                code_name = driver.find_element_by_xpath(xp_name).text
                cursor.execute(query_2 % (code_num, code_details_num, code_name))
        except:
            pass


# 기타 직군 코드
others_num = '999'
cursor.execute('INSERT INTO Code_parent VALUES ("999", "기타")')
for i in range(1, 10):
    xp = '/html/body/div/div/div/div[12]/a[%s]'
    elements = driver.find_element_by_xpath(xp % str(i))
    elements_href= elements.get_attribute('href')
    elements_split = elements_href.split('/wdlist')[-1]
    code_details_num = elements_split.split('/')[-1]
    code_name = driver.find_element_by_xpath(xp % str(i) + '/h2').text
    cursor.execute(query_2 % (others_num, code_details_num, code_name))


mysql.close()

