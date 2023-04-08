# import library
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup as bs
import crawling_function
import os
import time
import random
import re
print("----------library import success")


# 유블라인드 모음 관련
blind_url_list = []
blind_title = []

#--------------------------------------------블라인드 모음 시작------------------------------------------------------------------
def blind(driver):
    print("블라인드 접속 중")
    blind_url = "https://www.teamblind.com/kr/"
    driver.get(blind_url)
    print("접속 완료")
    print("블라인드 토픽베스트 크롤링 시작")
    for i in range(2, 12):
        blind_url_list.append(driver.find_element(By.CSS_SELECTOR, '#wrap > section > div > div > div > div.topic-list.best > div:nth-child(' + str(i) + ') > a').get_attribute('href'))
        blind_title.append(driver.find_element(By.CSS_SELECTOR, '#wrap > section > div > div > div > div.topic-list.best > div:nth-child(' + str(i) + ') > a').text)

    return blind_url_list, blind_title



#--------------------------------------------블라인드 모음 끝--------------------------------------------------------------------
