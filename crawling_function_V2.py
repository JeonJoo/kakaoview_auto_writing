# import library
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup as bs
import crawling_function
import os
import time
print("----------library import success")

# 실검봇 관련
silgeom_url_list = []
silgeom_title = []


# 다정남 관련
wk_url_list = []
wk_title = []

IComparison_seoulmetro_target_list = []
Iseoulmetro_update_count_list = []
Strseoulmetro_title_list = []
Strseoulmetro_url_list = []


I1min_update_count_list = []
Str1min_title_list = []
Str1min_url_list = []


Ihogang_update_count_list = []
Strhogang_title_list = []
Strhogang_url_list = []


Isamang_update_count_list = []
Strsamang_title_list = []
Strsamang_url_list = []


Iddookddak_update_count_list = []
Strddookddak_title_list = []
Strddookddak_url_list = []


Ibaewoonpig_update_count_list = []
Strbaewoonpig_title_list = []
Strbaewoonpig_url_list = []
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
def one_minute(driver, youtube_counts):
    print("1분미만 새영상 확인중")
    oneminute_url_1 = "https://vling.net/ko/channel/UC2xkO7XCiStWfR3fKbzkbqw"
    driver.get(oneminute_url_1)
    print("접속 완료")
    time.sleep(3)
    one_min_target = int(driver.find_element(By.CSS_SELECTOR, '#scroll_mobile > section > section > div.ChannelInfo_pageContainer__LzEII > div.ChannelInfo_flexBox__FJwVH > div.BasicInfo_container__U7ibC > div.BasicInfo_contentBox__XbFCR > div.BasicInfo_infoBox__CZgyS > ul > li:nth-child(4) > p').text)
    I1min_update_count_list.append(one_min_target)

    if youtube_counts < one_min_target:
        content_counts = one_min_target - youtube_counts
        oneminute_url_2 = 'https://www.youtube.com/results?search_query=1%EB%B6%84%EB%AF%B8%EB%A7%8C'
        driver.get(oneminute_url_2)
        soup = bs(driver.page_source, 'lxml')
        a_tag = soup.select('h3 > a')
        youtube = 'https://www.youtube.com'
        for idx in range(content_counts):
            Str1min_url_list.append(youtube + a_tag[idx].get('href'))
            Str1min_title_list.append(a_tag[idx].get('title'))

    return I1min_update_count_list, Str1min_title_list, Str1min_url_list


def hogang(driver, youtube_counts):
    print("호갱구조대 새영상 확인중")
    hogang_url_1 = "https://vling.net/ko/channel/UCbVcA0cFsYE8sTHQdl8b9Ww"
    driver.get(hogang_url_1)
    print("접속 완료")
    time.sleep(3)
    hogang_target = int(driver.find_element(By.CSS_SELECTOR, '#scroll_mobile > section > section > div.ChannelInfo_pageContainer__LzEII > div.ChannelInfo_flexBox__FJwVH > div.BasicInfo_container__U7ibC > div.BasicInfo_contentBox__XbFCR > div.BasicInfo_infoBox__CZgyS > ul > li:nth-child(4) > p').text)
    Ihogang_update_count_list.append(hogang_target)

    if youtube_counts < hogang_target:
        content_counts = hogang_target - youtube_counts
        hogang_url_2 = 'https://www.youtube.com/results?search_query=%ED%98%B8%EA%B0%B1%EA%B5%AC%EC%A1%B0%EB%8C%80'
        driver.get(hogang_url_2)
        soup = bs(driver.page_source, 'lxml')
        a_tag = soup.select('h3 > a')
        youtube = 'https://www.youtube.com'
        for idx in range(content_counts):
            Strhogang_url_list .append(youtube + a_tag[idx].get('href'))
            Strhogang_title_list.append(a_tag[idx].get('title'))

    return Ihogang_update_count_list, Strhogang_title_list, Strhogang_url_list



def samang(driver, youtube_counts):
    print("사망여우 새영상 확인중")
    samang_url_1 = "https://vling.net/ko/channel/UCuyN3WjEZW41qVji8TWUPeQ"
    driver.get(samang_url_1)
    print("접속 완료")
    time.sleep(3)
    samang_target = int(driver.find_element(By.CSS_SELECTOR, '#scroll_mobile > section > section > div.ChannelInfo_pageContainer__LzEII > div.ChannelInfo_flexBox__FJwVH > div.BasicInfo_container__U7ibC > div.BasicInfo_contentBox__XbFCR > div.BasicInfo_infoBox__CZgyS > ul > li:nth-child(4) > p').text)
    Isamang_update_count_list.append(samang_target)

    if youtube_counts < samang_target:
        content_counts = samang_target - youtube_counts
        samang_url_2 = 'https://www.youtube.com/results?search_query=%EC%82%AC%EB%A7%9D%EC%97%AC%EC%9A%B0'
        driver.get(samang_url_2)
        soup = bs(driver.page_source, 'lxml')
        a_tag = soup.select('h3 > a')
        youtube = 'https://www.youtube.com'
        for idx in range(content_counts):
            Strsamang_url_list .append(youtube + a_tag[idx].get('href'))
            Strsamang_title_list.append(a_tag[idx].get('title'))

    return Isamang_update_count_list, Strsamang_title_list, Strsamang_url_list



def ddookddak(driver, youtube_counts):
    print("뚝딱이형 새영상 확인중")
    ddookddak_url_1 = "https://vling.net/ko/channel/UC0htUSwcxfSGNfK_5Q28JkA"
    driver.get(ddookddak_url_1)
    print("접속 완료")
    time.sleep(3)
    ddookddak_target = int(driver.find_element(By.CSS_SELECTOR, '#scroll_mobile > section > section > div.ChannelInfo_pageContainer__LzEII > div.ChannelInfo_flexBox__FJwVH > div.BasicInfo_container__U7ibC > div.BasicInfo_contentBox__XbFCR > div.BasicInfo_infoBox__CZgyS > ul > li:nth-child(4) > p').text)
    Iddookddak_update_count_list.append(ddookddak_target)

    if youtube_counts < ddookddak_target:
        content_counts = ddookddak_target - youtube_counts
        ddookddak_url_2 = 'https://www.youtube.com/results?search_query=1%EB%B6%84%EC%9A%94%EB%A6%AC%EB%9A%9D%EB%94%B1%EC%9D%B4%ED%98%95'
        driver.get(ddookddak_url_2)
        soup = bs(driver.page_source, 'lxml')
        a_tag = soup.select('h3 > a')
        youtube = 'https://www.youtube.com'
        for idx in range(content_counts):
            Strddookddak_url_list .append(youtube + a_tag[idx].get('href'))
            Strddookddak_title_list.append(a_tag[idx].get('title'))

    return Iddookddak_update_count_list, Strddookddak_title_list, Strddookddak_url_list



def baewoonpig(driver, youtube_counts):
    print("배운돼지 새영상 확인중")
    baewoonpig_url_1 = "https://vling.net/ko/channel/UC5T4b53jVkm07JbYoyYiu7A"
    driver.get(baewoonpig_url_1)
    print("접속 완료")
    time.sleep(3)
    baewoonpig_target = int(driver.find_element(By.CSS_SELECTOR, '#scroll_mobile > section > section > div.ChannelInfo_pageContainer__LzEII > div.ChannelInfo_flexBox__FJwVH > div.BasicInfo_container__U7ibC > div.BasicInfo_contentBox__XbFCR > div.BasicInfo_infoBox__CZgyS > ul > li:nth-child(4) > p').text)
    Ibaewoonpig_update_count_list.append(baewoonpig_target)

    if youtube_counts < baewoonpig_target:
        content_counts = baewoonpig_target - youtube_counts
        baewoonpig_url_2 = 'https://www.youtube.com/results?search_query=%EB%A8%B9%EC%96%B4%EC%9C%A0+%EB%B0%B0%EC%9A%B4%EB%8F%BC%EC%A7%80'
        driver.get(baewoonpig_url_2)
        soup = bs(driver.page_source, 'lxml')
        a_tag = soup.select('h3 > a')
        youtube = 'https://www.youtube.com'
        for idx in range(content_counts):
            Strbaewoonpig_url_list .append(youtube + a_tag[idx].get('href'))
            Strbaewoonpig_title_list.append(a_tag[idx].get('title'))

    return Ibaewoonpig_update_count_list, Strbaewoonpig_title_list, Strbaewoonpig_url_list




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