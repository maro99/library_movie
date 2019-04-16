from ..models.locations import *
from ..models.movie import *

import re
import requests
from bs4 import BeautifulSoup
import time
from urllib import parse
import json
from selenium import webdriver

import datetime

import ssl
import urllib
import urllib3
import urllib.request as req

import datetime
from urllib import parse

from dateutil.relativedelta import relativedelta
from django.utils import timezone


# 상영일 저장 기준 위한 변수들

# 당월 뽑기.
now_date =  datetime.datetime.now()
now_date_str = datetime.datetime.now().strftime('%Y-%m')

# 당월의 첫날 뽑기
now_year_str, now_month_str = now_date_str.split('-')
now_months_first_day =  datetime.datetime.strptime(f'{now_year_str}-{now_month_str}','%Y-%m')
now_months_first_day_aware = timezone.make_aware(now_months_first_day)

# 전월의 첫날 뽑기
before_months_first_day = now_months_first_day - relativedelta(months=1)
before_months_first_day_aware = timezone.make_aware(before_months_first_day)


# 다음월의 첫날 뽑기
after_months_first_day = now_months_first_day + relativedelta(months=1)
after_months_first_day_aware = timezone.make_aware(after_months_first_day)

# 다음월의 마지막날 뽑기
after_months_last_day = now_months_first_day + relativedelta(months=2) - datetime.timedelta(days=1)
after_months_last_day_aware = timezone.make_aware(after_months_last_day)



# Dict log # 크롤링 결과 담는 dict


dict_log = {
    "updated_movie": {
        "동대문구": {"num": 0,"list": []},
        "성동구": {"num": 0,"list": []},
        "광진구": {"num": 0,"list": []},
    },
    "no_extra_info_movie" : {
        "동대문구":{"num":0,"list":[]},
        "성동구":{"num":0,"list":[]},
        "광진구": {"num": 0,"list": []},
    },
    "deleted_movie": {
        "동대문구":{"num":0,"list":[]},
        "성동구":{"num":0,"list":[]},
        "광진구": {"num": 0,"list": []},
    },
    "total_movie": {
        "동대문구": {"before": 0, "now": 0, "after": 0},
        "성동구": {"before": 0, "now": 0, "after": 0},
        "광진구": {"before": 0, "now": 0, "after": 0},
    },
}




# 영화 제목
# 일시
# 장소

# http://www.l4d.or.kr/library/index.php?g_page=culture&m_page=culture04&cate=&part=0&libCho=TOL&libGroup=MA&year=2018&month=9

#     ##### 동대문구 크롤러##### (월별)
def dongdaemungu_movie_crawler(year,libGroup):

    # MA(동대문) 의 경우만 2페이지까지 크롤링
    page_num_list = ['1']
    if libGroup == 'MA':
        page_num_list = ['1','2']


    for page_num in page_num_list:

        params = {
            'currentPageNo':page_num,
            'manageCd': libGroup,
        }
        url = "https://www.l4d.or.kr/intro/menu/10111/program/30030/movieList.do?" + parse.urlencode(params)

        request = requests.get(url)
        response = request.text
        soup = BeautifulSoup(response, 'lxml')

        movie_lis = soup.select('ul.movie-list > li')

        for movie_li in movie_lis:
            #     print(movie_li)

            title = ""  # 제목

            when = ""  # 일시
            when_date_year = 0
            when_date_month = 0
            when_date_day = 0
            when_time_hour = 0
            when_time_minuite = 0
            runtime = 0  # 런타임
            place = ""  # 장소

            title = movie_li.select_one('dt.tit').get_text(strip=True)
            print(f'title: {title}')

            lis = movie_li.select('dd > ul.clearfix > li')
            for li in lis:

                #         print(li)
                if li.get_text().split(' ')[0].strip() == '상영일자':
                    when = "".join(li.get_text().split(' ')[1:]).strip()
                    print(f'when: {when}')

                    if re.findall('\s(\d\d\d\d).', when):
                        when_date_year = re.findall('\s(\d\d\d\d).', when)[0]

                    if re.findall('\d\d\d\d.(\d{1,2}).', when):
                        when_date_month = re.findall('\d\d\d\d.(\d{1,2}).', when)[0]

                    if re.findall('\d\d\d\d.\d*.(\d\d)', when):
                        when_date_day = re.findall('\d\d\d\d.\d*.(\d\d)', when)[0]

                    # 18:00 이런 식으로 표현될때만 이하 처리
                    if re.findall('(\d\d):', when):
                        when_time_hour = re.findall('(\d\d):', when)[0]
                        when_time_minuite = re.findall('\d\d:(\d\d)', when)[0]
                    # 18시 이런식으로 표현될땐 ~
                    elif re.findall('(\d+)\s*시', when):
                        when_time_hour = re.findall('(\d+)시', when)[0]
                    # 18시 30분 이런식으로 표현시
                    elif re.findall('\d+\s*시\s*(\d+)\s*분', when):
                        when_time_hour = re.findall('(\d+)\s*시\s*\d+\s*분', when)[0]
                        when_time_minuite = re.findall('\d+\s*시\s*(\d+)\s*분', when)[0]

                    print(f'when_date_year: {when_date_year}')
                    print(f'when_date_month: {when_date_month}')
                    print(f'when_date_day: {when_date_day}')
                    print(f'when_time_hour: {when_time_hour}')
                    print(f'when_time_minuite: {when_time_minuite}')


                elif li.get_text().split(' ')[0].strip() == '상영시간':
                    if re.findall('(\d+)', li.get_text()):
                        runtime = re.findall('(\d+)', li.get_text())[0]
                    print(f'runtime: {runtime}')

                elif li.get_text().split(' ')[0].strip() == '상영장소':
                    if li.get_text().split(':'):
                        place = li.get_text().split(':')[1].strip()
                    print(f'place: {place}')

            d = datetime.date(int(when_date_year), int(when_date_month), int(when_date_day))
            t = datetime.time(int(when_time_hour), int(when_time_minuite), 0)
            dt = datetime.datetime.combine(d, t)

            library = Library.objects.get(library_code=libGroup)
            # print(library)

            # 이전월의 첫날 <=  상영일 <= 다음달의 마지막일 때만 저장.

            if dt >= before_months_first_day and dt <= after_months_last_day and dt >= now_date:
                movie, movie_created_bool = Movie.objects.get_or_create(
                    library=library,
                    title=title,
                    when=dt,
                    place=place,
                    runtime=runtime,
                )

            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')



#    ##### 성동구 크롤러 ##### (페이지별) # 참고로 냄겨둠.
def seongdonggu_movie_crawler(area_code, year):
    # 페이지 1~3를 탐색해서 해당 월에 상영하는 작품만 가져오자.
    for page in range(1, 3):

        params = {
            'page': page
        }

        # url = "https://www.naver.com"
        # url = "https://www.sdlib.or.kr/SD/U07080.asp?viewtype=list"
        url = "https://www.sdlib.or.kr/" + area_code + "/U07080.asp?viewtype=list&" + parse.urlencode(params)
        #     url = "https://www.sdlib.or.kr/SD/U07080.asp?viewtype=list&page=1&libno="



        request = requests.get(url, verify=False)
        response = request.text


        # 이하 몇몇 시도들

        # ssl._create_default_https_context = ssl._create_unverified_context
        # res = req.urlopen(url)

        # context = ssl._create_unverified_context()
        # req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0',     "Accept": "text/html"})
        # html = urllib.request.urlopen(req,  context=context).read()


        # # req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        # # res = urllib.request.urlopen(req).read()
        #
        # context = ssl._create_unverified_context()
        # req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        #
        # res = urllib.request.urlopen(req,  context=context)


        soup = BeautifulSoup(response, 'lxml')

        table_rows = soup.select('table.table700 > tbody > tr')

        for row in table_rows:

            title = ""
            place = ""
            pic_url =""
            when_date_year = 0
            when_date_month = 0
            when_date_day = 0
            when_time_hour = 0
            when_time_minuite = 0
            runtime = 0

            for index, td in enumerate(row.select('td')):
                if index == 0:
                    time_date = td.get_text(strip=True)  # time_date : 2018-11-03
                    when_date_year = time_date.split('-')[0]
                    when_date_month = time_date.split('-')[1]
                    when_date_day = time_date.split('-')[2]
                    print(f'when_date_month : {when_date_month}')  # 날짜
                    print(f'when_date_day : {when_date_day}')


                elif index == 2:
                    time_hour = td.get_text(strip=True)
                    when_time_hour = time_hour.split(':')[0]
                    when_time_minuite = time_hour.split(':')[1]
                    print(f'when_time_hour : {when_time_hour}')  # 시작시간
                    print(f'when_time_minuite : {when_time_minuite}')

                elif index == 3:
                    title = td.get_text(strip=True)
                    print(f'title : {title}')  # 영화 제목
                elif index == 6:
                    runtime_pre = td.get_text(strip=True)
                    runtime = runtime_pre.split('분')[0]
                    print(f'runtime :  {runtime}')  # 상영시간

            d = datetime.date(int(when_date_year), int(when_date_month), int(when_date_day))
            t = datetime.time(int(when_time_hour), int(when_time_minuite), 0)
            dt = datetime.datetime.combine(d, t)

            library = Library.objects.get(library_code=area_code)
            print(library)

            if dt >= before_months_first_day and dt <= after_months_last_day:
                movie, movie_created_bool = Movie.objects.get_or_create(
                    library=library,
                    title=title,
                    when=dt,
                    place=place,
                    runtime=runtime,
                    # thumbnail_url=pic_url,  #  ---> 12.31/ get_or_create시 계속 중복 생성해서 여기선 업데이트 x
                )

            print('@@@@@@@@@@@@@@@@@@@@@@@@@')

        print(f'{page}@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')


# 정보화는 엘범형-->기존방식처럼 크롤링
# 나머지 체육센터, 구의3동은 게시판에서 '영화' 키워드 검색해서 정보 찾음.
def gwangjingu_movie_crawler(area_code, year, month):
    def get_soup(url):
        ssl._create_default_https_context = ssl._create_unverified_context
        res = req.urlopen(url)
        soup = BeautifulSoup(res, 'lxml')
        return soup

    # 정보화 경우 해당 url접속할때가 해당 달에 해당하는 page여서
    # 따로 month 변수 사용 안했다.

    if area_code == 'gjinfo':
        url = "https://www.gwangjinlib.seoul.kr/gjinfo/menu/10087/program/30020/movieList.do"
        soup = get_soup(url)

        movies = soup.select('ul.movie-list > li')
        for movie in movies:

            title = ""
            pic_url=""
            place = ""
            when_date_year = 0
            when_date_month = 1
            when_date_day = 1
            when_time_hour = 0
            when_time_minuite = 0
            runtime = 0

            pic_url = "https://www.gwangjinlib.seoul.kr" + movie.select_one('div.thumb > img').get('src')
            print(f'pic_url: {pic_url}') # 사진
            title_pre = movie.select_one('dl > dt')
            title = title_pre.contents[1].strip()
            print(f'title: {title}')  # 제목
            dds = movie.select('dl > dd')
            for index, dd in enumerate(dds):
                if index == 1:
                    runtime_pre = dd.contents[1].strip()
                    runtime = re.findall('(\d\d*)', runtime_pre)[0]
                    print(f'runtime: {runtime}')  # 런타임

                elif index == 3:
                    #                     print(f'상영일자 : {dd.contents[1]}') #상영일자(날짜 + 시간 ) # 2018.10.27(토) 오후 2시 or 오후2시, 오전1시
                    when = dd.contents[1]
                    when_date = re.findall("(\S*)\(", when)[0]  # 2018.10.27
                    when_date_year = when_date.split('.')[0]
                    when_date_month = when_date.split('.')[1]
                    when_date_day = when_date.split('.')[2]
                    print(f'when_date_year:{when_date_year}')
                    print(f'month : {when_date_month}')  # 상영 날짜
                    print(f'day : {when_date_day}')  #

                    when_time_pre = re.findall("\)\s*(.{4,6})시", when)[0]
                    #                     print(f'상영 시간 : {when_time_pre}') # 상영 시간  # 오후 2시
                    if '오후' in when_time_pre:
                        when_time_hour = int(re.findall("오후(.*\d*)", when_time_pre)[0].strip()) + 12

                    elif '오전' in when_time_pre:
                        when_time_hour = int(re.findall("오전(.*\d*)", when_time_pre)[0].strip())

                    print(f'when_time_hour :{when_time_hour}')

                    print('@@@@@@@@@@@@@@@@@@')



            d = datetime.date(int(when_date_year), int(when_date_month), int(when_date_day))
            t = datetime.time(int(when_time_hour), int(when_time_minuite), 0)
            dt = datetime.datetime.combine(d, t)

            library = Library.objects.get(library_code=area_code)
            print(library)

            if dt >= before_months_first_day and dt <= after_months_last_day and dt >= now_date:
                movie, movie_created_bool = Movie.objects.get_or_create(
                    library=library,
                    title=title,
                    when=dt,
                    place=place,
                    runtime=runtime,
                    # thumbnail_url=pic_url #  ---> 12.31/ get_or_create시 계속 중복 생성해서 여기선 업데이트 x
                )

    #         pass

    # 1. 먼저 해당 url에서 게시판 첫페이지의 글목록의 모든 글들의 text를 검색해서
    # '영화' 라는 키워드 가진 것 찾고
    # 2 .해당 a테그의 onclick 속성의 evenlis 인덱스 번호 가령 1334 를 얻는다.
    # 3. 주소에 그값을 붙여서 해당 글의 디테일로 들어간다.
    # 4. 글 안에서  상영날짜 : 등을 찾아서 각각 항목 크롤링.

    # *month 변수 사용해서 해당월+이전 월까지의 게시글만 크롤링 하겠다.

    elif area_code == 'jgsports':
        #         pass
        url = "https://www.gwangjinlib.seoul.kr/jgsports/menu/11005/program/30201/eventList.do"
        soup = get_soup(url)

        titles_blocks = soup.select('table.board-list > tbody > tr > td.title')

        for title_block in titles_blocks:

            title = ""
            pic_url = ""
            place = ""
            when_date_month = 0
            when_date_day = 0
            when_time_hour = 0
            when_time_minuite = 0
            runtime = 0


            # 해당 월 혹은 전 월의 숫자를 포함하는 것만 뽑음.
            if '영화' in title_block.get_text() and (
                    (str(month - 1)) in title_block.get_text() or (str(month)) in title_block.get_text() or (
            str(month + 1)) in title_block.get_text()):
                onclick_text = title_block.select_one('a').get('onclick')  # javascript:fnDetail('1254'); return false;
                post_index = re.findall("'(\d*)'", onclick_text)[0]  # 1254
                print(post_index)

                url = "https://www.gwangjinlib.seoul.kr/jgsports/menu/11005/program/30201/eventDetail.do?currentPageNo=1&eventIdx=" + post_index
                soup = get_soup(url)
                text = soup.select_one('table.board-view > tbody > tr > td.content').get_text()

                if re.findall("상영영화\s*:\s*(.*)\s*-", text):
                    title = re.findall("상영영화\s*:\s*(.*)", text)[0]
                print(f'title: {title}')  # 제목

                if re.findall("(\d*)월\s*\d*일", text):
                    when_date_month = re.findall("(\d*)월\s*\d*일", text)[0]
                if re.findall("\d*월\s*(\d*)일", text):
                    when_date_day = re.findall("\d*월\s*(\d*)일", text)[0]
                print(f'month: {when_date_month}')  # 상영날짜
                print(f'day: {when_date_day}')

                if re.findall("(\d*)시\s*\d*분", text):
                    when_time_hour = re.findall("(\d*)시\s*\d*분", text)[0]
                if re.findall("\d*시\s*(\d*)분", text):
                    when_time_minuite = re.findall("\d*시\s*(\d*)분", text)[0]
                print(f'when_time_hour: {when_time_hour}')  # 상영시간
                print(f'when_time_minuite: {when_time_minuite}')

                if re.findall("\((\d*)분\)", text):
                    runtime = re.findall("\((\d*)분\)", text)[0]  # 런타임
                print(f'runtime: {runtime}')

                if re.findall("상영장소\s*:\s*(.*)\s*-", text):
                    place = re.findall("상영장소\s*:\s*(.*)\s*-", text)[0]
                print(f'place: {place}')

                print('@@@@@@@@@@@@@@@@@@@@@@@@')

                d = datetime.date(int(year), int(when_date_month), int(when_date_day))
                t = datetime.time(int(when_time_hour), int(when_time_minuite), 0)
                dt = datetime.datetime.combine(d, t)

                library = Library.objects.get(library_code=area_code)
                print(library)

                if dt >= before_months_first_day and dt <= after_months_last_day and dt >= now_date:
                    movie, movie_created_bool = Movie.objects.get_or_create(
                        library=library,
                        title=title,
                        when=dt,
                        place=place,
                        runtime=runtime,
                        # thumbnail_url=pic_url   #  ---> 12.31/ get_or_create시 계속 중복 생성해서 여기선 업데이트 x
                    )



    #                 ○ 영화가 있는 수요일 무료영화상영 안내

    #                 - 문화가 있는 날(매월 마지막 수요일)사업의 확산 및 문화생활 향상에 기여하고자

    #                   다양한 연령대가 함께 즐길 수 있는 무료 영화를 상영합니다.

    #                 - 운영일시 : 9월 27일(목) 7시 30분 (111분) *추석연휴 휴관일로 인하여 9월만 목요일에 진행합니다.* ######

    #                 - 상영영화 :  당신, 거기 있어줄래요                                                     ######

    #                 - 이용대상 : 12세관람가

    #                 - 상영장소 : 중곡문화체육센터도서관 2층 이야기극장                #####

    #                 - 이용대상 : 도서관이용자 30명

    #                 - 별도의 접수없이 시간에 맞추어 방문하시어 관람하시면 됩니다.

    #                 - 문의사항 : 02-3408-4931

    elif area_code == 'gu3dong':
        url = "https://www.gwangjinlib.seoul.kr/gu3dong/menu/11002/program/30202/eventList.do"
        soup = get_soup(url)

        titles_blocks = soup.select('table.board-list > tbody > tr > td.title')

        for title_block in titles_blocks:

            title = ""
            pic_url = ""
            place = ""
            when_date_month = 0
            when_date_day = 0
            when_time_hour = 0
            when_time_minuite = 0
            runtime = 0


            fin_time_hour = 0
            fin_time_minuite = 0

            if '영화' in title_block.get_text() and (
                    (str(month - 1)) in title_block.get_text() or (str(month)) in title_block.get_text() or (
            str(month + 1)) in title_block.get_text()):
                onclick_text = title_block.select_one('a').get('onclick')  # javascript:fnDetail('1254'); return false;
                post_index = re.findall("'(\d*)'", onclick_text)[0]  # 1254
                print(post_index)

                url = "https://www.gwangjinlib.seoul.kr/jgsports/menu/11005/program/30201/eventDetail.do?currentPageNo=1&eventIdx=" + post_index
                soup = get_soup(url)
                text = soup.select_one('table.board-view > tbody > tr > td.content').get_text()

                if re.findall("영화명\s*:\s*(.*)\s", text):
                    title = re.findall("영화명\s*:\s*(.*)", text)[0]
                print(f'title: {title}')  # 제목

                if re.findall("(\d*)월\s*\d*일", text):
                    when_date_month = re.findall("(\d*)월\s*\d*일", text)[0]
                if re.findall("\d*월\s*(\d*)일", text):
                    when_date_day = re.findall("\d*월\s*(\d*)일", text)[0]
                print(f'month: {when_date_month}')  # 상영날짜
                print(f'day: {when_date_day}')

                if re.findall("(\d*):\s*\d*~", text):
                    when_time_hour = re.findall("(\d*):\s*\d*~", text)[0]
                if re.findall("\d*:\s*(\d*)~", text):
                    when_time_minuite = re.findall("\d*:\s*(\d*)~", text)[0]
                print(f'when_time_hour: {when_time_hour}')  # 상영시간
                print(f'when_time_minuite: {when_time_minuite}')

                # 런타임 계산을 위해서 끝나는시간 뽑음

                if re.findall("~(\d*):\s*\d*", text):
                    fin_time_hour = re.findall("~(\d*):\s*\d*", text)[0]
                if re.findall("~\d*:\s*(\d*)", text):
                    fin_time_minuite = re.findall("~\d*:\s*(\d*)", text)[0]
                print(f'fin_time_hour: {fin_time_hour}')  # 상영시간
                print(f'fin_time_minuite: {fin_time_minuite}')

                runtime = ((int(fin_time_hour) - int(when_time_hour)) * 60 + (
                            int(fin_time_minuite) - int(when_time_minuite)))
                print(f'runtime: {runtime}')  # 런타임

                if re.findall("상영장소\s*:\s*(.*)\s*", text):
                    place = re.findall("상영장소\s*:\s*(.*)\s*", text)[0]
                print(f'place: {place}')

                print('@@@@@@@@@@@@@@@@@@@@@@@@')

                d = datetime.date(int(year), int(when_date_month), int(when_date_day))
                t = datetime.time(int(when_time_hour), int(when_time_minuite), 0)
                dt = datetime.datetime.combine(d, t)

                library = Library.objects.get(library_code=area_code)
                print(library)

                # 상영기준이 오늘 보다 이전인것은 포함 안시키겠다.
                if dt >= before_months_first_day and dt <= after_months_last_day and dt >= now_date:
                    movie, movie_created_bool = Movie.objects.get_or_create(
                        library=library,
                        title=title,
                        when=dt,
                        place=place,
                        runtime=runtime,
                        # thumbnail_url=pic_url  #  ---> 12.31/ get_or_create시 계속 중복 생성해서 여기선 업데이트 x
                    )


#             구의제3동도서관에서는 '문화가 있는 날'을 맞아 무료영화 상영을 통해 관내 주민의 문화생활 및 여가활용에 이바지 하고자합니다.

#             ◈ 일시 : 10월 31일(수) 16:30~18:35

#             ◈ 영화명 : 우리는 동물원을 샀다

#             ◈ 상영등급 : 전체 관람가

#             ◈ 상영장소 : 도서관 소강의실


#     table_rows = soup.select('table.table700 > tbody > tr')



def jungnanggu_movie_crawler(libGroup):

    # 전체 페이지에서 타이틀 쪼개지는 경우 있어서. 디테일 들어가서 각각 정보 크롤링 해주겠슴.
    url = "http://www.jungnanglib.seoul.kr/jnlib/index.php?g_page=event&m_page=event04"
    request = requests.get(url)
    response = request.text
    soup = BeautifulSoup(response, 'lxml')
    movie_a_tags = soup.select("div.data_wrapper")
    url_nums = []  # 각 디테일 가는 번호 여기 저장.
    for movie_a_tag in movie_a_tags:

        a_tag = movie_a_tag.select_one("h3 > a").get('href')
        #     print(a_tag)
        #     ./index.php?g_page=event&m_page=event04&libCho=MA&libCho=MA&act=movie_view&mvCode=228
        if re.findall('Code=(\d*)', a_tag):
            url_nums.append(re.findall('Code=(\d*)', a_tag)[0])

    # 뽑아낸 url_num으로 각 detail page크롤링
    root_url = "http://www.jungnanglib.seoul.kr/jnlib/index.php?g_page=event&m_page=event04&libCho=MA&libCho=MA&act=movie_view&mvCode="

    for url_num in url_nums:

        title = ""  # 제목

        when = ""  # 일시
        when_date_year = 0
        when_date_month = 0
        when_date_day = 0
        when_time_hour = 0
        when_time_minuite = 0

        runtime = 0  # 런타임
        place = ""  # 장소

        detail_url = root_url + url_num
        request = requests.get(detail_url)
        response = request.text
        soup = BeautifulSoup(response, 'lxml')
        movie_box = soup.select_one("div.data_info")

        title = movie_box.select_one('h3').get_text(strip=True)
        print(f'title: {title}')

        lis = movie_box.select('li')
        for li in lis:
            item_name = li.select_one('span.item').get_text(strip=True)

            if item_name == "일시":
                when = li.select_one('span.value').get_text(strip=True)
                print(f'when: {when}')  # 2019년 04월 27일  15시 00분 (토) 상영

                when_date_year = re.findall('(\d\d\d\d)', when)[0]
                when_date_month = re.findall('(\d{1,2})\s*월', when)[0]
                when_date_day = re.findall('(\d{1,2})\s*일', when)[0]

                # 18시 이런식으로만 표현될땐 ~
                if re.findall('(\d+)\s*시', when):
                    when_time_hour = re.findall('(\d+)시', when)[0]
                # 18시 30분 이런식으로 표현시
                elif re.findall('\d+\s*시\s*(\d+)\s*분', when):
                    when_time_hour = re.findall('(\d+)\s*시\s*\d+\s*분', when)[0]
                    when_time_minuite = re.findall('\d+\s*시\s*(\d+)\s*분', when)[0]

                print(f'when_date_year: {when_date_year}')
                print(f'when_date_month: {when_date_month}')
                print(f'when_date_day: {when_date_day}')
                print(f'when_time_hour: {when_time_hour}')
                print(f'when_time_minuite: {when_time_minuite}')

            elif item_name == "장소":
                place = li.select_one('span.value').get_text(strip=True)
                print(f'place: {place}')

            elif item_name == "시간":
                runtime_pre = li.select_one('span.value').get_text(strip=True)
                runtime = re.findall('(\d+)', runtime_pre)[0]
                print(f'runtime: {runtime}')

        d = datetime.date(int(when_date_year), int(when_date_month), int(when_date_day))
        t = datetime.time(int(when_time_hour), int(when_time_minuite), 0)
        dt = datetime.datetime.combine(d, t)

        library = Library.objects.get(library_code=libGroup)
        # print(library)

        # 이전월의 첫날 <=  상영일 <= 다음달의 마지막일 때만 저장.

        if dt >= before_months_first_day and dt <= after_months_last_day and dt >= now_date:
            movie, movie_created_bool = Movie.objects.get_or_create(
                library=library,
                title=title,
                when=dt,
                place=place,
                runtime=runtime,
            )

        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')



def get_extra_info(movie,title):

    global dict_log

    def get_soup(url):
        ssl._create_default_https_context = ssl._create_unverified_context
        res = req.urlopen(url)
        soup = BeautifulSoup(res, 'lxml')
        return soup

    # 한글을 query 로 변환
    title_encoded = parse.quote(title)

    # 검색 url접속후 detail 페이지로 가기위한 url을 먼저 얻겠다.
    url = "https://movie.naver.com/movie/search/result.nhn?query=" + title_encoded + "&section=all&ie=utf8"
    soup = get_soup(url)

    # 만약 아무것도 검색 결과 없다면 None 입력되고 아래 if문 못들어감.
    # detail_url_pre = soup.select_one('ul.search_list_1 > li > dl > dt > a') 이전 맨앞에꺼 뽑던 코드.(일단 주석처리함 )
    detail_url_pre = soup.select('ul.search_list_1 > li > dl > dd.point > em.cuser_cnt')

    # 이번 크롤링 회차에 저장되는 영화 검색 되던말든 일단 이름 저장.
    dict_log["updated_movie"][movie.library.library_district.district_name]["num"] += 1
    dict_log["updated_movie"][movie.library.library_district.district_name]["list"].append(movie.title)

    if detail_url_pre:

        # 모델 객체 저장할 값들 초기화
        pic_url =""
        rating = 0
        genre = ""
        director =""
        age =""
        story =""

        # 이하는 검색 결과 중 가장 많이본 영화 테그 착기 위함.
        max_num = 0
        max_num_rated_movies_line1 = detail_url_pre[0]  # 일단 맨앞 line저장
        for line1 in detail_url_pre:
            #         print(line1) # 여기기준  이웃 , 부모 테그 타고가서 링크 얻자.
            text_pre = line1.get_text()
            number_of_rated_people = re.findall("(\d+)", text_pre)[0]
            #         print(number_of_rated_people)
            if max_num <= int(number_of_rated_people):
                max_num = int(number_of_rated_people)
                max_num_rated_movies_line1 = line1

        parent_tag = max_num_rated_movies_line1.parent
        dt_tag_as_previous_tag = parent_tag.find_previous_sibling("dt")
        a_tag = dt_tag_as_previous_tag.select_one('a')

        # detail로 가는 url
        detail_url = 'https://movie.naver.com' + a_tag.get('href')

        soup = get_soup(detail_url)

        # 포스터 이미지
        pic_url_pre = soup.select_one('div.poster > a > img')
        if pic_url_pre:
            pic_url = pic_url_pre.get('src')
            print(f'pic_url: {pic_url}')

        # 포토가 있는 경우에는 포토 의 맨앞에거 가져다 쓰고싶다.
        pic_viewer_url_pre = soup.select_one('div.viewer_img >  img')
        if pic_viewer_url_pre:
            pic_url = pic_viewer_url_pre.get('src')
            print(f'pic_url: {pic_url}')

        rating_pre = soup.select_one('div.mv_info > div.main_score > div.score.score_left > div.star_score > a')
        if rating_pre:
            rating = rating_pre.get_text()
            print(f'rating: {rating}')


        genre_pre_pre = soup.select_one('div.mv_info > dl.info_spec > dt.step1')
        if genre_pre_pre:
            genre_pre = genre_pre_pre.find_next_siblings('dd')[0].select('p > span > a')[0] # 여기서 인덱스 에러 날수도 있다...
            if genre_pre:
                genre =  genre_pre.get_text()
                print(f'genre: {genre}')


        director_pre_pre = soup.select_one('div.mv_info > dl.info_spec > dt.step2')
        if director_pre_pre:
            director_pre = director_pre_pre.find_next_siblings('dd')[0]
            if director_pre:
                director = director_pre.get_text()
                print(f'director: {director}')


        age_pre_pre = soup.select_one('div.mv_info > dl.info_spec > dt.step4')
        if age_pre_pre:
            age_pre = age_pre_pre.find_next_siblings('dd')[0].select_one('a')
            if age_pre:
                age = age_pre.get_text()
                print(f'age: {age}')

        story_pre = soup.select_one('div.video')
        if story_pre:
            story = story_pre.get_text()
            print(f'story: {story}')

        # # 썸네일이 이미 없는 경우에만 업데이트를 하자 ------> 일단 안지우겠슴.
        # if movie.thumbnail_url == "":
        #     movie.thumbnail_url = pic_url

        # 썸네일 네이버 검색 이미지 -> 뷰어이미지 첫번째거로 통일 시키겠다.
        # 무조건 업데이트 하겠슴.(검색 안되는데 섬네일 있는경우는 여기 아예 안들언옴) ---> 12.31/ get_or_create시 계속 중복 생성해서 걍 무조건 여기서 업데이트 하겠슴.
        movie.thumbnail_url = pic_url                                         # 검색 안되는것 추후 구글검색 첫이미지로 업데이트 시키겠다.

        # 수지윙의 세계의 경우 네이버 영화 에서 검색은 되지만 섬네일 없다.
        # 이런경우에는 구글에서 이미지 검색해서 썸네일 업데이트 해주자.
        if not pic_url:
            upadete_google_image(movie,movie.title)

        movie.rating = float(rating)
        movie.genre = genre
        movie.director = director
        movie.age = age
        movie.story = story
        movie.save()

    # 네이버 영화에서 검색결과 없다면.
    else:
        upadete_google_image(movie,movie.title)  # 구글 검색해서 이미지라도 넣어주겠슴.
        dict_log["no_extra_info_movie"][movie.library.library_district.district_name]["num"]+=1
        dict_log["no_extra_info_movie"][movie.library.library_district.district_name]["list"].append(movie.title)


def upadete_google_image(movie,title):

    search_term = title
    search_url = "https://www.google.com/search?q={}&site=webhp&tbm=isch".format(search_term)
    d = requests.get(search_url).text
    soup = BeautifulSoup(d, 'html.parser')

    img_tags = soup.find_all('img')

    imgs_urls = []
    for img in img_tags:
        if img['src'].startswith("http"):
            imgs_urls.append(img['src'])

    movie.thumbnail_url = imgs_urls[0]
    movie.save()

def main_movie_crawler():

    global dict_log

    dict_log = {
        "updated_movie": {
            "동대문구": {"num": 0, "list": []},
            "성동구": {"num": 0, "list": []},
            "광진구": {"num": 0, "list": []},
            "중랑구": {"num": 0, "list": []},
        },
        "no_extra_info_movie": {
            "동대문구": {"num": 0, "list": []},
            "성동구": {"num": 0, "list": []},
            "광진구": {"num": 0, "list": []},
            "중랑구": {"num": 0, "list": []},
        },
        "deleted_movie": {
            "동대문구": {"num": 0, "list": []},
            "성동구": {"num": 0, "list": []},
            "광진구": {"num": 0, "list": []},
            "중랑구": {"num": 0, "list": []},
        },
        "total_movie": {
            "동대문구": {"before": 0, "now": 0, "after": 0},
            "성동구": {"before": 0, "now": 0, "after": 0},
            "광진구": {"before": 0, "now": 0, "after": 0},
            "중랑구": {"before": 0, "now": 0, "after": 0},
        },
    }

    # 오늘 날짜 먼저 가져옴
    now = datetime.datetime.now()
    year = now.year
    day = now.day
    month = now.month
    #
    ##### 동대문구 크롤러#####

    dongdaemungu_area_code_list = ['MA', 'MF', 'MB', 'MC', 'MJ']
    # 정보화,답십리, 장안, 용두, 휘셩 (이문 제외)
    #     dongdaemungu_area_code_list = ['MA']

    for libGroup in dongdaemungu_area_code_list:
        dongdaemungu_movie_crawler(year,libGroup)
        print(
            f'{libGroup} #####################################################################################################################################')

#     ### 성동구 크롤러 #####
#
#     seongdonggu_area_code_list = ['SD','YD','SS','KH','CG']
#     # 성동구립,용답, 장안, 성수, 금호,청계
# #     seongdonggu_area_code_list = ['SD']
#
#     for area_code in seongdonggu_area_code_list:
#         seongdonggu_movie_crawler(area_code,year)
#         print(f'{area_code}#############################################################################################################################')
#
#


#     ##### 광진구 크롤러 #####
    gwangjingu_area_code_list = ['gjinfo','jgsports','gu3dong']
#     정보 , 중곡문화체육센터, 구의제3동
    for area_code in gwangjingu_area_code_list:
        gwangjingu_movie_crawler(area_code,year,month)
        print(f'{area_code}#############################################################################################################################')


    ###### 중랑구 크롤러 #####
    jungnanggu_area_code = "JMA"  # 한곳이라 걍 변수로만함.
    jungnanggu_movie_crawler(jungnanggu_area_code)
    print(f'{jungnanggu_area_code}#############################################################################################################################')




    # 현제시간 - 5분
    now_date_before_5_min = timezone.now() - timezone.timedelta(minutes=5)

    # 상영시간 naive한 datetime으로 변환


    # 위에서 크롤링한 movie들의 extra 정보들을 update하는 함수 호출한다.
    for movie in Movie.objects.all():

        # 초벌 크롤링시 저장된 시간이 현제시간 -5분 보다 큰것(이후인것) 들만 업데이트 함수 적용시키겠다.
        if movie.created_at  > now_date_before_5_min:
            title = movie.title
            get_extra_info(movie, title)

        # 삭제될 영화 타이틀 로그에 저장
        if not movie.when >= before_months_first_day_aware and movie.when <= after_months_last_day_aware:
            dict_log["deleted_movie"][movie.library.library_district.district_name]["num"] += 1
            dict_log["deleted_movie"][movie.library.library_district.district_name]["list"].append(movie.title)
            movie.delete()

        # 토탈 영화 갯수 구별로 달끊어서 로그 저장.
        # 이전월의첫날 <= 상영일 <= 다음월 마지막달 인 영화 count
        elif (movie.when >= before_months_first_day_aware) and (movie.when < now_months_first_day_aware):
            dict_log["total_movie"][movie.library.library_district.district_name]["before"] += 1

        elif (movie.when >= now_months_first_day_aware) and (movie.when < after_months_first_day_aware):
            dict_log["total_movie"][movie.library.library_district.district_name]["now"] += 1

        elif (movie.when >= after_months_first_day_aware) and (movie.when <= after_months_last_day_aware):
            dict_log["total_movie"][movie.library.library_district.district_name]["after"] += 1

    return dict_log

