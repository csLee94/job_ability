from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time 
#-- 크롬드라이버 설정 
chrome_option = Options() #초기화
# chrome_option.add_argument("headless") # 창 없는 모드
path = os.getcwd() # 설치한 Chromdriver 절대 경로설정
driver  = webdriver.Chrome(path+'/chromedriver.exe', chrome_options= chrome_option) # driver 선언
# driver2  = webdriver.Chrome(path+'/chromedriver.exe', chrome_options= chrome_option) # driver 선언
target_xpath = "/html/body/div[1]/div/div[3]/div[1]/div[1]/div[1]/div[2]/section[1]/p[%s]/span"


driver.get("https://www.wanted.co.kr/wd/41577")
# driver.execute_script("window.scrollTo(0,400)")

for tmpnm in range(1,3):
    driver.execute_script("window.scrollTo(0,%s)" % str(300*tmpnm))
    time.sleep(1)     
maintask = driver.find_element_by_xpath(target_xpath % "2").text
qual1 = driver.find_element_by_xpath(target_xpath % "3").text
qual2 = driver.find_element_by_xpath(target_xpath % "4").text

print("성공: %s, %s, %s" % (maintask[:10], qual1[:10], qual2[:10])) # 필요없을 때 삭제

