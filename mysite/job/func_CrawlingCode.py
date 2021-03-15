from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import pymysql

#-- 크롬드라이버 설정 
chrome_option = Options() #초기화
chrome_option.add_argument("headless")
path = os.getcwd() # 설치한 Chromdriver 절대 경로설정
driver  = webdriver.Chrome(path+'/chromedriver.exe', chrome_options= chrome_option) # driver 선언

#-- 임시 페이지 연결
driver.get('file:///C:/Users/pc1/Documents/%230.LCS/project_job/code.html') # 임시 페이지 절대 경로

#-- 저장할 DB 연결
mysql = pymysql.connect(host='3.36.125.12', port=56754, user='lcs', password='lcs', db='tempdb', charset='utf8mb4', autocommit=True)
cursor = mysql.cursor(pymysql.cursors.DictCursor)
query_1 = 'INSERT INTO Code_parent VALUES ("%s", "%s")'

#-- 직군 분류 코드 가져오기
# for i in range(11): # 대분류 
#     try:
#         xp_1 = '/html/body/div/div/div/div[%s]/a[1]'  # 대분류_코드 num xpath
#         code_num = driver.find_element_by_xpath(xp_1 % str(i+1)).get_attribute('href')
#         code_num = code_num.split('wdlist/')[-1]
#         xp_2 = '/html/body/div/div/div/div[%s]/a[1]/h2' # 대분류_코드 name xpath
#         code_name = driver.find_element_by_xpath(xp_2 % str(i+1)).text
#         # print(query % (str(code_num), str(code_name)))
#         cursor.execute(query_1 % (str(code_num), str(code_name)))
#     except:
#         print('pass')

for i in range(1, 12):
    xp_home = '/html/body/div/div/div/div[%s]/a[%s]'
    
    for j in range(1, 10):
        elements = driver.find_element_by_xpath(xp_home % (str(i), str(j)))
        elements_split=elements.get_attribute('href').split('/wdlist')[-1]
        num = elements_split.split('/')
        if num == 2:
            code_num = elements_split.split('/')[-1]
            xp_name = xp_home % (str(i), str(j)) + '/h2'
            code_name = driver.find_element_by_xpath(xp_name).text
            print(code_num, code_name)
        elif num ==3:
            code_num = elements_split.split('/')[-2]
            code_details_num = elements_split.split('/')[-1]
            xp_name = xp_home % (str(i), str(j)) + '/h3'
            code_name = driver.find_element_by_xpath(xp_name).text
            print(code_num, code_details_num, code_name)

mysql.close()

# # /html/body/div/div/div/div[4]/a[1]/h2
# # /html/body/div/div/div/div[4]/a[8]/h3
# /html/body/div/div/div/div[12]/a[5]/h2
# /html/body/div/div/div/div[12]/a[9]/h2
# /html/body/div/div/div/div[11]/a[8]/h3