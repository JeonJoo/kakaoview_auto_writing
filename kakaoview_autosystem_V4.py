# 조선일보, 중앙일보, 동아일보, 한국일보, 국민일보, 서울신문 사설 자동 크롤링 시스템

# import library
from selenium import webdriver as wd
import os
import pandas as pd
import crawling_function
import crawling_function_V2
import kaview_write
from crawling_function import *
from crawling_function_V2 import *
from kaview_write import login_count

print("----------library import success")



if not os.path.exists('D:/python_venv/kakaoview_autosystem'):
    print('경로없음_새 경로 생성')
    os.mkdir('D:/python_venv/kakaoview_autosystem')

# 시간별, 날짜별 컨트롤
now = time

# 유튜브 크롤링 관련
header = ['1분미만', '호갱구조대', '사망여우']
df1 = pd.read_csv('D:/python_venv/kakaoview_autosystem/youtube_contents_count.csv', sep=',', names=header)
youtube_counts = list(df1.loc[0])

print('변수 설정 완료')


print("----------load chrome web driver ")
options = wd.ChromeOptions()
# options.add_argument('--headless')        # Head-less 설정
# options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = wd.Chrome('./driver/chromedriver.exe', options=options)
driver.implicitly_wait(10)    # 명시적 대기
print("Done")



### -------------------------------------------------- 블로그 시작 ----------------------------------------------------------------
# 간단하개 크롤링
crawling_function.d_on(driver)
IComparison_D_on_target = IComparison_D_on_target_list.pop()

crawling_function.new_writting_detection_check(IComparison_D_on_target, 0)
Inew_d_on_writting_detection = int(I_D_on_update_count.pop())

if Inew_d_on_writting_detection < IComparison_D_on_target:
    new_writting = IComparison_D_on_target - Inew_d_on_writting_detection
    print('간단하개 새 글 확인 :', new_writting)

    for i in range(new_writting):
        kaview_write.kaview_write_cat_on_a_flowerpot(driver, strBlog_title, D_on_url_list, D_on_content_list, login_count, i)

elif Inew_d_on_writting_detection >= IComparison_D_on_target:
    print('간단하개 새 글 없음')
    
# 호시탐탐플랜츠 크롤링
crawling_function.hosi(driver)
IComparison_hosi_target = int(IComparison_hosi_target_list.pop())

crawling_function.new_writting_detection_check(0, IComparison_hosi_target)
Inew_hosi_writting_detection = int(I_hosi_update_count.pop())

if Inew_hosi_writting_detection < IComparison_hosi_target:
    strBlog_title = strBlog_title[5:]
    new_writting = IComparison_hosi_target - Inew_hosi_writting_detection
    print('호시탐탐플랜츠 새 글 확인 :', new_writting)

    for j in range(new_writting):
        kaview_write.kaview_write_cat_on_a_flowerpot(driver, strBlog_title, hosi_url_list, hosi_content_list, login_count, j)

elif Inew_hosi_writting_detection >= IComparison_hosi_target:
    print('호시탐탐플랜츠 새 글 없음')

# new_writting_detection 초기화
crawling_function.new_writting_detection_check(IComparison_D_on_target, IComparison_hosi_target)
### -------------------------------------------------- 블로그 끝 ----------------------------------------------------------------








### -------------------------------------------------- 사설을 읽다, 실검봇, 날씨의 아이 등록 시작 ----------------------------------------------------------------
try:
    if (now.localtime().tm_hour >= 6) & (now.localtime().tm_hour < 14):    # 조간

        # 날씨의아이
        kaview_write.kaview_write_weather(driver)
        kaview_write.kaview_write_microdust(driver)
        kaview_write.kaview_write_astro(driver)
        kaview_write.kaview_write_realtime_subway(driver)

        # 집회 및 시위 정보
        crawling_function_V2.seoulmetro(driver)
        IComparison_seoulmetro_target = int(IComparison_seoulmetro_target_list.pop())
        crawling_function_V2.new_writting_chk(IComparison_seoulmetro_target)
        if int(Iseoulmetro_update_count_list.pop()) == 0:
            print('지하철 시위 발생')
            kaview_write.kaview_write_protests_info(driver, Strseoulmetro_title_list, Strseoulmetro_url_list, 0)

        else:
            print('집회 및 시위 발생')
            kaview_write.kaview_write_protests_info(driver, Strseoulmetro_title_list, Strseoulmetro_url_list, 1)



        # ----------오전 실검 시작
        crawling_function_V2.silgeom(driver)
        silgeom_url_list_456 = silgeom_url_list[3:6]
        silgeom_url_list_7890 = silgeom_url_list[6:10]

        try:
            for k in range(3):
                kaview_write.kaview_write_silgeom1(driver, silgeom_title, silgeom_url_list, login_count, k)

            kaview_write.kaview_write_silgeom2(driver, silgeom_url_list_456, login_count)
            kaview_write.kaview_write_silgeom2(driver, silgeom_url_list_7890, login_count)
        except:
            pass
        # ----------오전 실검 끝
        
        if(now.localtime().tm_wday < 5):  #평일
            crawling_function.seoul(driver)
            kaview_write.kaview_write(driver, strTitle, seoul_url_list, login_count)
    
            crawling_function.chosunilbo(driver)
            kaview_write.kaview_write(driver, strTitle, chosun_url_list, login_count)
    
            crawling_function.joongangilbo(driver)
            kaview_write.kaview_write(driver, strTitle, joongang_url_list, login_count)
    
            crawling_function.dongailbo(driver)
            kaview_write.kaview_write(driver, strTitle, donga_url_list, login_count)
    
            crawling_function.hankookilbo(driver)
            kaview_write.kaview_write(driver, strTitle, hankook_url_list, login_count)
    
            crawling_function.kmib(driver)
            kaview_write.kaview_write(driver, strTitle, km_url_list, login_count)

        elif(now.localtime().tm_wday != 6): # 월 - 토
            crawling_function.chosunilbo(driver)
            kaview_write.kaview_write(driver, strTitle, chosun_url_list, login_count)
    
            crawling_function.joongangilbo(driver)
            kaview_write.kaview_write(driver, strTitle, joongang_url_list, login_count)
    
            crawling_function.dongailbo(driver)
            kaview_write.kaview_write(driver, strTitle, donga_url_list, login_count)
    
            crawling_function.hankookilbo(driver)
            kaview_write.kaview_write(driver, strTitle, hankook_url_list, login_count)
    
            crawling_function.kmib(driver)
            kaview_write.kaview_write(driver, strTitle, km_url_list, login_count)

        kaview_write.exit_function()
    
    elif (now.localtime().tm_hour >= 19) & (now.localtime().tm_hour <=23):

        # ----------오후 실검 시작
        crawling_function_V2.silgeom(driver)
        silgeom_url_list_456 = silgeom_url_list[3:6]
        silgeom_url_list_7890 = silgeom_url_list[6:10]

        try:
            for k in range(3):
                kaview_write.kaview_write_silgeom1(driver, silgeom_title, silgeom_url_list, login_count, k)

            kaview_write.kaview_write_silgeom2(driver, silgeom_url_list_456, login_count)
            kaview_write.kaview_write_silgeom2(driver, silgeom_url_list_7890, login_count)
        except:
            pass
        # ----------오후 실검 끝
        
        
        # ----------유튜브 크롤링
        # ---------------------1분미만 시작--------------------------
        crawling_function_V2.one_minute(driver, int(youtube_counts[0]))
        if int(youtube_counts[0]) < int(I1min_update_count_list[0]):
            df1['1분미만'] = I1min_update_count_list.pop()
            df1.to_csv("D:/python_venv/kakaoview_autosystem/youtube_contents_count.csv", header=False, index=False)

            for i in range(len(Str1min_title_list)):
                kaview_write.kaview_write_youtube(driver, Str1min_title_list[i], '1분미만', Str1min_url_list[i], login_count)

        elif int(youtube_counts[0]) == int(I1min_update_count_list[0]):
            print("새 영상 없음")
        # ---------------------1분미만 끝-----------------------------
        #           ------------------------------------
        # ---------------------호갱구조대 시작--------------------------
        crawling_function_V2.hogang(driver, int(youtube_counts[1]))
        if int(youtube_counts[1]) < int(Ihogang_update_count_list[0]):
            df1['호갱구조대'] = Ihogang_update_count_list.pop()
            df1.to_csv("D:/python_venv/kakaoview_autosystem/youtube_contents_count.csv", header=False, index=False)

            for i in range(len(Strhogang_title_list)):
                kaview_write.kaview_write_youtube(driver, Strhogang_title_list[i], '호갱구조대', Strhogang_url_list[i], login_count)

        elif int(youtube_counts[1]) == int(Isamang_update_count_list[0]):
            print("새 영상 없음")
        # ---------------------호갱구조대 끝----------------------------
        #           ------------------------------------
        # ---------------------사망여우 시작--------------------------
        crawling_function_V2.samang(driver, int(youtube_counts[2]))
        if int(youtube_counts[2]) < int(Isamang_update_count_list[0]):
            df1['사망여우'] = Isamang_update_count_list.pop()
            df1.to_csv("D:/python_venv/kakaoview_autosystem/youtube_contents_count.csv", header=False, index=False)

            for i in range(len(Strsamang_title_list)):
                kaview_write.kaview_write_youtube(driver, Strsamang_title_list[i], '사망여우', Strsamang_url_list[i], login_count)

        elif int(youtube_counts[2]) == int(Isamang_update_count_list[0]):
            print("새 영상 없음")
        # ---------------------사망여우 끝----------------------------

        # ----------유튜브 크롤링
        if (now.localtime().tm_wday < 5): # 평일
            crawling_function.hani(driver)
            kaview_write.kaview_write(driver, strTitle, hani_url_list, login_count)
    
            crawling_function.hankyung(driver)
            kaview_write.kaview_write(driver, strTitle, hankyung_url_list, login_count)
    
            crawling_function.mk(driver)
            kaview_write.kaview_write(driver, strTitle, mk_url_list, login_count)
    
    
        elif (now.localtime().tm_wday == 5): # 토요일
            crawling_function.hani(driver)
            kaview_write.kaview_write(driver, strTitle, hani_url_list, login_count)
    
           
        elif (now.localtime().tm_wday == 6): # 일요일
            crawling_function.hankyung(driver)
            kaview_write.kaview_write(driver, strTitle, hankyung_url_list, login_count)
    
            crawling_function.mk(driver)
            kaview_write.kaview_write(driver, strTitle, mk_url_list, login_count)

        kaview_write.exit_function()
    
    else:
        print('사설 크롤링 일정 없음 | 요일 및 시간을 확인하세요.')
        input('종료를 원하면 ENTER를 누르세요')

except:
    print('에러 확인 필요')
    input('종료를 원하면 ENTER를 누르세요')


