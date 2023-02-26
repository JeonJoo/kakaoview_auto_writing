# import library
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup as bs
import crawling_function
import os
import time
import random
import re
print("----------library import success")


# 실검봇 관련
silgeom_url_list = []
silgeom_title = []


# 날씨의 아이, 먹진심 관련
wk_url_list = []
wk_title = []

IComparison_seoulmetro_target_list = []
Iseoulmetro_update_count_list = []
Strseoulmetro_title_list = []
Strseoulmetro_url_list = []

Iupdate_count_list = []
title_list = []
url_list = []


#--------------------------------------------실검봇 시작------------------------------------------------------------------
def silgeom(driver):
    #  시그널 실검 크롤링
    print("시그널 접속 중")
    silgeom_url = "https://www.signal.bz/"
    driver.get(silgeom_url)
    print("접속 완료")


    
    print("시그널 실시간 검색어 크롤링 시작")
    iCrawling_count = 10
    for i in range(1, 3):
        for j in range(1, 6):
            try:
                silgeom_url_list.append((driver.find_element(By.CSS_SELECTOR, '#app > div > main > div > section > div > section > section:nth-child(2) > div:nth-child(2) > div > div:nth-child(' + str(i) + ') > div:nth-child(' + str(j) +') > a').get_attribute('href')))
                silgeom_title.append((driver.find_element(By.CSS_SELECTOR, '#app > div > main > div > section > div > section > section:nth-child(2) > div:nth-child(2) > div > div:nth-child(' + str(i) + ') > div:nth-child(' + str(j) + ') > a > span.rank-text')).text)
            except:
                iCrawling_count -= 1
                pass

    iException_count = 10 - iCrawling_count
    print("성공 : " + str(iCrawling_count), "실패 : " + str(iException_count))
    if iException_count == 10:
        crawling_function.crawling_fail()

    return silgeom_title, silgeom_url_list





#--------------------------------------------실검봇 끝------------------------------------------------------------------




#--------------------------------------------날씨의 아이 시작------------------------------------------------------------------
def seoulmetro(driver):
    print("서울교통공사 접속 중")
    seoulmetro_url = "http://www.seoulmetro.co.kr/kr/board.do?menuIdx=546"
    driver.get(seoulmetro_url)
    print("접속 완료")

    driver.find_element(By.CSS_SELECTOR, '#sk').send_keys('열차운행 지연')
    driver.find_element(By.CSS_SELECTOR,'#searchForm > fieldset > ul > li.bbsl-sc-text > span > input[type=image]').click()
    time.sleep(0.5)
    IComparison_seoulmetro_target_list.append(driver.find_element(By.CSS_SELECTOR, '#contents > div.tbl-box1 > table > tbody > tr:nth-child(1) > td.num.t-disn.bd1').text)
    Strseoulmetro_title_list.append(driver.find_element(By.CSS_SELECTOR,'#contents > div.tbl-box1 > table > tbody > tr:nth-child(1) > td.td-lf.bd2 > a').text)
    Strseoulmetro_url_list.append(driver.find_element(By.CSS_SELECTOR,'#contents > div.tbl-box1 > table > tbody > tr:nth-child(1) > td.td-lf.bd2 > a').get_attribute('href'))

    return IComparison_seoulmetro_target_list, Strseoulmetro_title_list, Strseoulmetro_url_list

#--------------------------------------------날씨의 아이 끝------------------------------------------------------------------







#--------------------------------------------유튜브 크롤링 시작------------------------------------------------------------------
def youtube_crawling(driver, youtube_counts, url1, url2, timesleep=3):
    driver.get(url1)
    print("접속 완료")
    time.sleep(timesleep)
    try:
        Itarget_counts = int(driver.find_element(By.CSS_SELECTOR, '#scroll_mobile > section > section > div.ChannelInfo_pageContainer__LzEII > div.ChannelInfo_flexBox__FJwVH > div.BasicInfo_container__U7ibC > div.BasicInfo_contentBox__XbFCR > div.BasicInfo_infoBox__CZgyS > ul > li:nth-child(4) > p').text)
    except:
        print('재실행')
        print(driver, youtube_counts, url1, url2)
        youtube_crawling(driver, youtube_counts, url1, url2, 7)
    print('Vling 통과')
    Iupdate_count_list.append(Itarget_counts)

    if youtube_counts < Itarget_counts:
        content_counts = Itarget_counts - youtube_counts
        print("**새 영상 확인**", content_counts)
        driver.get(url2)
        soup = bs(driver.page_source, 'lxml')
        a_tag = soup.select('h3 > a')
        youtube = 'https://www.youtube.com'
        for idx in range(content_counts):
            url_list.append(youtube + a_tag[idx].get('href'))
            title = a_tag[idx].get('title')
            only_BMP_pattern = re.compile("["u"\U00010000-\U0010FFFF""]+", flags=re.UNICODE)
            title_list.append(only_BMP_pattern.sub(r'', title))


    elif youtube_counts >= Itarget_counts:
        driver.get(url2)
        driver.find_element(By.CSS_SELECTOR, '#more > yt-formatted-string').click()     # 8개 더 보기
        soup = bs(driver.page_source, 'lxml')
        a_tag = soup.select('h3 > a')
        youtube = 'https://www.youtube.com'

        idx = random.randint(0, 9)
        print(idx)
        url_list.append(youtube + a_tag[idx].get('href'))
        title = a_tag[idx].get('title')
        only_BMP_pattern = re.compile("["u"\U00010000-\U0010FFFF""]+", flags=re.UNICODE)
        title_list.append(only_BMP_pattern.sub(r'', title))

    return Iupdate_count_list, title_list, url_list




#--------------------------------------------유튜브 크롤링 끝------------------------------------------------------------------






def new_writting_chk(IComparison_seoulmetro_target):
    print("new_writting_chk 체크")
    if not os.path.isfile("D:/python_venv/kakaoview_autosystem/new_writting_chk.txt"):
        print("new_writting_chk 파일 없음")
        f = open("new_writting_chk.txt", "w")
        f.write(str(IComparison_seoulmetro_target))
        f.close()
        print("new_writting_chk 생성")

    elif(os.path.isfile("new_writting_chk.txt")):
        with open("new_writting_chk.txt", "r") as f:
            Strnew_writting_chk = int(f.read())
            f.close()

            if(Strnew_writting_chk != IComparison_seoulmetro_target):
                Iseoulmetro_update_count_list.append(0)
                f = open("new_writting_chk.txt", "w")
                f.write(str(IComparison_seoulmetro_target))
                print('*****새 공지 확인')
                f.close()
            else:
                Iseoulmetro_update_count_list.append(1)
                print('새 공지 없음')
    return Iseoulmetro_update_count_list
