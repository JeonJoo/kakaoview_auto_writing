# 사설 크롤링 함수

# import library
from selenium.webdriver.common.by import By
import sys
import os
import random
import re
print("----------library import success")

# 사설 크롤링 관련
chosun_url_list = []
joongang_url_list = []
donga_url_list = []
hankook_url_list = []
km_url_list = []
seoul_url_list = []
hani_url_list = []
hankyung_url_list = []
mk_url_list = []

# 간단하개 관련
D_on_url_list = []
D_on_content_list = []
D_on_total_writting_list = []
IComparison_D_on_target_list = []
I_D_on_update_count = []


#호시탐탐 관련
hosi_url_list = []
hosi_content_list = []
hosi_total_writting_list = []
IComparison_hosi_target_list = []
I_hosi_update_count = []

strTitle = []
strBlog_title = []

# 크라우드픽 관련
crowdpic_url = []


def new_writting_detection_check(IComparison_D_on_target, IComparison_hosi_target):
    print("new_writting_detection 체크")
    if not os.path.isfile("D:/python_venv/kakaoview_autosystem/new_writting_detection.txt"):
        print("new_writting_detection 파일 없음")
        f = open("new_writting_detection.txt", "w")
        f.write(str(IComparison_D_on_target) + ', ')
        f.write('^' + str(IComparison_hosi_target))
        Inew_d_on_writting_detection = IComparison_D_on_target
        Inew_hosi_writting_detection = IComparison_hosi_target
        I_D_on_update_count.append(Inew_d_on_writting_detection)
        I_hosi_update_count.append(Inew_hosi_writting_detection)
        f.close()
        print("new_writting_detection 생성")

    elif(os.path.isfile("new_writting_detection.txt")):
        with open("new_writting_detection.txt", "r") as f:
            Strnew_writting_detection = f.read()
            f.close()

            if (Strnew_writting_detection.find(',') >= 0) & (Strnew_writting_detection.find('^') >= 0) & (IComparison_hosi_target == 0):
                I_D_on_detection = Strnew_writting_detection.find(',')
                Strnew_d_on_writting_detection = Strnew_writting_detection[:I_D_on_detection]
                I_D_on_update_count.append(Strnew_d_on_writting_detection)
                print('간단하개 기존글 개수 :', Strnew_d_on_writting_detection)

            elif (Strnew_writting_detection.find(',') >= 0) & (Strnew_writting_detection.find('^') >= 0) & (IComparison_D_on_target == 0):
                I_hosi_detection = Strnew_writting_detection.find('^')
                Inew_hosi_writting_detection = int(Strnew_writting_detection[I_hosi_detection + 1:])

                if Inew_hosi_writting_detection == 0:
                    f = open("new_writting_detection.txt", "w")
                    f.write(str(IComparison_D_on_target) + ', ')
                    f.write('^' + str(IComparison_hosi_target))
                    f.close()
                    print('기존글 개수 최신화')
                else:
                    I_hosi_update_count.append(Inew_hosi_writting_detection)
                    print('호시탐탐 기존글 개수 :', Inew_hosi_writting_detection)

            else:
                print("기존글 개수 최신화")
                f = open("new_writting_detection.txt", "w")
                f.write(str(IComparison_D_on_target) + ', ')
                f.write('^' + str(IComparison_hosi_target))
                I_D_on_update_count.append(IComparison_D_on_target)
                I_hosi_update_count.append(IComparison_hosi_target)
                f.close()

    return I_D_on_update_count, I_hosi_update_count


def crawling_fail():
    print("크롤링에 실패하였습니다")
    input("ENTER 를 눌러 종료하세요")
    sys.exit()


def d_on(driver):
    # 간단하개 새글 크롤링
    print("간단하개 접속 중")
    D_on_url = "https://blog.naver.com/PostList.naver?blogId=best_ih&skinType=&skinId=&from=menu"
    ### iframe 관련 코드가 작동하지 않아 회피
    driver.get(D_on_url)
    print("접속 완료")

    D_on_total_writting_list.append(driver.find_element(By.CSS_SELECTOR, '#category-list > div > ul > li.allview > span').text)
    IComparison_D_on_target = D_on_total_writting_list.pop()
    IComparison_D_on_target = int(IComparison_D_on_target[1:-1])
    print('간단하개 블로그 전체 글 수 :', IComparison_D_on_target)
    IComparison_D_on_target_list.append(IComparison_D_on_target)

    print('목록열기')
    driver.find_element(By.CSS_SELECTOR, '#toplistSpanBlind').click()

    title_list = []
    for i in range(1, 6):
        try:
            D_on_url_list.append((driver.find_element(By.CSS_SELECTOR, '#listTopForm > table > tbody > tr:nth-child(' + str(i) + ') > td.title > div > span > a').get_attribute('href')))
            title = driver.find_element(By.CSS_SELECTOR, '#listTopForm > table > tbody > tr:nth-child(' + str(i) + ') > td.title > div > span > a').text
            only_BMP_pattern = re.compile("["u"\U00010000-\U0010FFFF""]+", flags=re.UNICODE)
            title_list.append(only_BMP_pattern.sub(r'', title))
        except:
            pass

    print("제목, 설명 분리 작업")
    for title in title_list:
        Ititle_end_point = title.find(']')
        strBlog_title.append(title[1:Ititle_end_point])
        D_on_content_list.append(title[Ititle_end_point + 2:])


    print('Done')
    return strBlog_title, D_on_content_list, D_on_url_list, IComparison_D_on_target_list


def hosi(driver):
    # 호시탐탐플랜트 새글 크롤링
    print("호시탐탐플랜츠 접속 중")
    hosi_url = "https://blog.naver.com/PostList.naver?blogId=sz4940&skinType=&skinId=&from=menu"
    ### iframe 관련 코드가 작동하지 않아 회피
    driver.get(hosi_url)
    print("접속 완료")
    hosi_total_writting_list.append(driver.find_element(By.CSS_SELECTOR, '#category-list > div > ul > li.allview > span').text)
    IComparison_hosi_target = hosi_total_writting_list.pop()
    IComparison_hosi_target = int(IComparison_hosi_target[1:-1])
    print('호시탐탐 블로그 전체 글 수 :', IComparison_hosi_target)
    IComparison_hosi_target_list.append(IComparison_hosi_target)

    # 새글 확인
    new_writting_detection_check(0, IComparison_hosi_target)

    print('목록열기')
    driver.find_element(By.CSS_SELECTOR, '#toplistSpanBlind').click()

    for i in range(1,6):
        hosi_url_list.append((driver.find_element(By.CSS_SELECTOR, '#listTopForm > table > tbody > tr:nth-child(' + str(i) + ') > td.title > div > span > a').get_attribute('href')))
        title = driver.find_element(By.CSS_SELECTOR, '#listTopForm > table > tbody > tr:nth-child(' + str(i) + ') > td.title > div > span > a').text
        only_BMP_pattern = re.compile("["u"\U00010000-\U0010FFFF""]+", flags=re.UNICODE)
        strBlog_title.append(only_BMP_pattern.sub(r'', title))
        hosi_content_list.append('호시탐탐플랜츠')

        if i == 5:
            print(strBlog_title)
            print(hosi_content_list)
            print(hosi_url_list)
            print('Done')

    return strBlog_title, hosi_content_list, hosi_url_list, IComparison_hosi_target_list

#--------------------------------------------크라우드픽 크롤링 시작------------------------------------------------------------------
def crowd_pic(driver):
    print("크라우드픽 접속 중")
    crowd_url = "https://www.crowdpic.net/@powwow94"
    driver.get(crowd_url)
    img_total_counts = int(driver.find_element(By.CSS_SELECTOR, '#profile-detail-info-container > div.profile-dashboard-wrap > div:nth-child(1) > span.fr.color444141.album-count').text)
    random_sample_list = random.sample(range(1, img_total_counts), 3)
    for i in range(3):
        crowdpic_url.append(driver.find_element(By.CSS_SELECTOR, '#grid-wrap > a:nth-child('+ str(random_sample_list[i]) +')').get_attribute('href'))
    return crowdpic_url


#--------------------------------------------크라우드픽 크롤링 끝------------------------------------------------------------------


#--------------------------------------------조간신문------------------------------------------------------------------

# 조선일보 사설 크롤링
def chosunilbo(driver):
    print("----------조선일보 url crawling start")
    url = "https://www.chosun.com/opinion/editorial/"
    driver.get(url)

    # 사설 페이지에서 사진이 등록 안되면 기존의 url 과 다른 곳에 제목이 위치하게 됨.
    ## 예외처리를 하고 리스트에서 제거
    iCrawling_count = 3
    for i in range(1, 4):
        try:
            chosun_url_list.append((driver.find_element(By.CSS_SELECTOR, '#main > div.story-feed > div > div:nth-child(' + str(i) + ') > div > div > div > div.story-card.story-card--art-left.\|.flex.flex--wrap > div.story-card-block.story-card-right.\|.grid__col--sm-8.grid__col--md-8.grid__col--lg-8 > div.story-card-component.story-card__headline-container.\|.text--overflow-ellipsis.text--left > a').get_attribute('href')))
        except:
            iCrawling_count -= 1
            pass
    iException_count = 3 - iCrawling_count
    print("성공 : " + str(iCrawling_count), "실패 : " + str(iException_count))
    if iException_count == 3:
        crawling_fail()
    strTitle.append("조선일보 사설")
    return strTitle, chosun_url_list

# 동아일보 사설 크롤링
def dongailbo(driver):
    print("----------동아일보 url crawling start")
    url = "https://www.donga.com/news/Series/70040100000001"
    driver.get(url)

    iCrawling_count = 3
    for i in range(2, 5):
        try:
            donga_url_list.append((driver.find_element(By.CSS_SELECTOR, '#content > div:nth-child(' + str(i) + ') > div.rightList > span.tit > a').get_attribute('href')))
        except:
            iCrawling_count -= 1
            pass
    iException_count = 3 - iCrawling_count
    print("성공 : " + str(iCrawling_count), "실패 : " + str(iException_count))
    if iException_count == 3:
        crawling_fail()
    strTitle.append("동아일보 사설")
    return strTitle, donga_url_list

# 중앙일보 사설 크롤링
def joongangilbo(driver):
    print("----------중앙일보 url crawling start")
    url = "https://www.joongang.co.kr/opinion/editorialcolumn"
    driver.get(url)

    iCrawling_count = 3
    for i in range(1, 4):
        try:
            joongang_url_list.append((driver.find_element(By.CSS_SELECTOR, '#story_list > li:nth-child(' + str(i) + ') > div > h2 > a').get_attribute('href')))
        except:
            iCrawling_count -= 1
            pass
    iException_count = 3 - iCrawling_count
    print("성공 : " + str(iCrawling_count), "실패 : " + str(iException_count))
    if iException_count == 3:
        crawling_fail()
    strTitle.append("중앙일보 사설")
    return strTitle, joongang_url_list

# 한국일보 사설 크롤링
def hankookilbo(driver):
    print("----------한국일보 url crawling start")
    url = "https://www.hankookilbo.com/Opinion/HK01"
    driver.get(url)

    iCrawling_count = 3
    for i in range(1, 4):
        try:
            hankook_url_list.append((driver.find_element(By.CSS_SELECTOR, 'body > div.wrap.imp-section > div.container > div > div.sub-contents > div.col-main > div > div.tab-contents.caladd > ul > li:nth-child(' + str(i) + ') > div.text-box > h3 > a').get_attribute('href')))
        except:
            iCrawling_count -= 1
            pass
    iException_count = 3 - iCrawling_count
    print("성공 : " + str(iCrawling_count), "실패 : " + str(iException_count))
    if iException_count == 3:
        crawling_fail()
    strTitle.append("한국일보 사설")
    return strTitle, hankook_url_list

# 국민일보 사설 크롤링
def kmib(driver):
    print("----------국민일보 url crawling start")
    url = "https://m.kmib.co.kr/list.asp?sid1=opi"
    driver.get(url)

    iCrawling_count = 3
    for i in range(1, 4):
        try:
            km_url_list.append((driver.find_element(By.CSS_SELECTOR, '#con > ul > li:nth-child(' + str(i) + ') > a').get_attribute('href')))
        except:
            iCrawling_count -= 1
            pass
    iException_count = 3 - iCrawling_count
    print("성공 : " + str(iCrawling_count), "실패 : " + str(iException_count))
    if iException_count == 3:
        crawling_fail()
    strTitle.append("국민일보 사설")
    return strTitle, km_url_list

# 서울신문 사설 크롤링
def seoul(driver):
    print("----------서울신문 url crawling start")
    url = "https://www.seoul.co.kr/news/newsList.php?section=editorial"
    driver.get(url)

    iCrawling_count = 3
    for i in range(1, 4):
        try:
            seoul_url_list.append((driver.find_element(By.CSS_SELECTOR, '#articleListDiv > ul > li:nth-child(' + str(i) + ') > div.tit.lineclamp2 > a').get_attribute('href')))
        except:
            iCrawling_count -= 1
            pass
    iException_count = 3 - iCrawling_count
    print("성공 : " + str(iCrawling_count), "실패 : " + str(iException_count))
    if iException_count == 3:
        crawling_fail()
    strTitle.append("서울신문 사설")
    return strTitle, seoul_url_list

#--------------------------------------------석간신문------------------------------------------------------------------

# 한겨례신문 사설 크롤링
def hani(driver):
    print("----------한겨레신문 url crawling start")
    url = "https://www.hani.co.kr/arti/opinion/editorial/list1.html"
    driver.get(url)

    iCrawling_count = 3
    try:
        hani_url_list.append((driver.find_element(By.CSS_SELECTOR, '#section-left-scroll-in > div.section-list-area > div.list.first > div > h4 > a').get_attribute('href')))
    except:
        iCrawling_count -= 1
        pass

    try:
        hani_url_list.append((driver.find_element(By.CSS_SELECTOR, '#section-left-scroll-in > div.section-list-area > div:nth-child(3) > div > h4 > a').get_attribute('href')))
    except:
        iCrawling_count -= 1
        pass

    try:
        hani_url_list.append((driver.find_element(By.CSS_SELECTOR, '#section-left-scroll-in > div.section-list-area > div:nth-child(4) > div > h4 > a').get_attribute('href')))
    except:
        iCrawling_count -= 1
        pass
    iException_count = 3 - iCrawling_count
    print("성공 : " + str(iCrawling_count), "실패 : " + str(iException_count))
    if iException_count == 3:
        crawling_fail()
    strTitle.append("한겨레신문 사설")
    return strTitle, hani_url_list

# 한국경제 사설 크롤링
def hankyung(driver):
    print("----------한국경제 url crawling start")
    url = "https://www.hankyung.com/opinion/0001"
    driver.get(url)

    iCrawling_count = 3
    for i in range(1, 4):
        try:
            hankyung_url_list.append((driver.find_element(By.CSS_SELECTOR, '#container > div.wrap_cont > div.inner_list > ul:nth-child(2) > li:nth-child(' + str(i) + ') > div.article > h3 > a').get_attribute('href')))
        except:
            iCrawling_count -= 1
            pass

    iException_count = 3 - iCrawling_count
    print("성공 : " + str(iCrawling_count), "실패 : " + str(iException_count))
    if iException_count == 3:
        crawling_fail()
    strTitle.append("한국경제 사설")
    return strTitle, hankyung_url_list

# 매일경제 사설 크롤링
def mk(driver):
    print("----------매일경제 url crawling start")
    url = "https://www.mk.co.kr/opinion/editorial/"
    driver.get(url)

    iCrawling_count = 3
    for i in range(1, 4):
        try:
            mk_url_list.append((driver.find_element(By.CSS_SELECTOR, '#list_area > li:nth-child(' + str(i) + ') > a').get_attribute('href')))
        except:
            iCrawling_count -= 1
            pass

    iException_count = 3 - iCrawling_count
    print("성공 : " + str(iCrawling_count), "실패 : " + str(iException_count))
    if iException_count == 3:
        crawling_fail()
    strTitle.append("매일경제 사설")
    return strTitle, mk_url_list