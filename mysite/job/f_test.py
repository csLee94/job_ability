from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time 
import random 
import pymysql 
from datetime import datetime

now = datetime.now()
print(type(str(now)))
print(str(now))


#-- 크롬드라이버 설정 
chrome_option = Options() #초기화
chrome_option.add_argument("headless") # 창 업는 모드
path = os.getcwd() # 설치한 Chromdriver 절대 경로설정
driver  = webdriver.Chrome(path+'/chromedriver.exe', chrome_options= chrome_option) # driver 선언

driver.get('https://www.naver.com/')

print(type(driver.current_url))
print(driver.current_url)
