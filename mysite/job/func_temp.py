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

for i in range(1, 12):
    xp_home = '/html/body/div/div/div/div[%s]/a[%s]'
    for j in range(1, 10):
        try:
            elements = driver.find_element_by_xpath(xp_home % (str(i), str(j)))
            elements_href=elements.get_attribute('href')
            elements_split = elements_href.split('/wdlist')[-1]
            num = len(elements_split.split('/'))
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
        except:
            pass


# xp_home = '/html/body/div/div/div/div[%s]/a[%s]'
# ele = driver.find_element_by_xpath(xp_home % (str(1), str(1)))
# ele.get_attribute('href')