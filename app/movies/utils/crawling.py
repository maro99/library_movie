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
import time

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
        "중랑구": {"num": 0, "list": []},
        "성북구": {"num": 0, "list": []},
        "송파구": {"num": 0, "list": []},
        "영등포구": {"num": 0, "list": []},
        "은평구": {"num": 0, "list": []},
        "양천구": {"num": 0, "list": []},
        "서대문구": {"num": 0, "list": []},
        "마포구": {"num": 0, "list": []},
        "동작구": {"num": 0, "list": []},
        "도봉구": {"num": 0, "list": []},
        "노원구": {"num": 0, "list": []},
        "용산구": {"num": 0, "list": []},
        "구로구": {"num": 0, "list": []},
        "강서구": {"num": 0, "list": []},
        "강동구": {"num": 0, "list": []},
        "강남구": {"num": 0, "list": []},
        "종로구": {"num": 0, "list": []},
    },
    "no_extra_info_movie" : {
        "동대문구": {"num": 0,"list": []},
        "성동구": {"num": 0,"list": []},
        "광진구": {"num": 0,"list": []},
        "중랑구": {"num": 0, "list": []},
        "성북구": {"num": 0, "list": []},
        "송파구": {"num": 0, "list": []},
        "영등포구": {"num": 0, "list": []},
        "은평구": {"num": 0, "list": []},
        "양천구": {"num": 0, "list": []},
        "서대문구": {"num": 0, "list": []},
        "마포구": {"num": 0, "list": []},
        "동작구": {"num": 0, "list": []},
        "도봉구": {"num": 0, "list": []},
        "노원구": {"num": 0, "list": []},
        "용산구": {"num": 0, "list": []},
        "구로구": {"num": 0, "list": []},
        "강서구": {"num": 0, "list": []},
        "강동구": {"num": 0, "list": []},
        "강남구": {"num": 0, "list": []},
        "종로구": {"num": 0, "list": []},
    },
    "total_movie": {
        "동대문구": {"before": 0, "now": 0, "after": 0},
        "성동구": {"before": 0, "now": 0, "after": 0},
        "광진구": {"before": 0, "now": 0, "after": 0},
        "중랑구": {"before": 0, "now": 0, "after": 0},
        "성북구": {"before": 0, "now": 0, "after": 0},
        "송파구": {"before": 0, "now": 0, "after": 0},
        "영등포구": {"before": 0, "now": 0, "after": 0},
        "은평구": {"before": 0, "now": 0, "after": 0},
        "양천구": {"before": 0, "now": 0, "after": 0},
        "서대문구": {"before": 0, "now": 0, "after": 0},
        "마포구": {"before": 0, "now": 0, "after": 0},
        "동작구": {"before": 0, "now": 0, "after": 0},
        "도봉구": {"before": 0, "now": 0, "after": 0},
        "노원구": {"before": 0, "now": 0, "after": 0},
        "용산구": {"before": 0, "now": 0, "after": 0},
        "구로구": {"before": 0, "now": 0, "after": 0},
        "강서구": {"before": 0, "now": 0, "after": 0},
        "강동구": {"before": 0, "now": 0, "after": 0},
        "강남구": {"before": 0, "now": 0, "after": 0},
        "종로구": {"before": 0, "now": 0, "after": 0},
    },
    # "deleted_movie": {
    #     "동대문구": {"num": 0, "list": []},
    #     "성동구": {"num": 0, "list": []},
    #     "광진구": {"num": 0, "list": []},
    #     "중랑구": {"num": 0, "list": []},
    #     "성북구": {"num": 0, "list": []},
    #     "송파구": {"num": 0, "list": []},
    #     "영등포구": {"num": 0, "list": []},
    #     "은평구": {"num": 0, "list": []},
    # },
}

def save_movie(when_time_hour, when_date_year, when_date_month, when_date_day, when_time_minuite, libGroup, title, place, runtime):
    # 시간이 0시 ~ 9시 인 경우 도서관 운영 안하는 시간 이므로 + 12를 해준다.
    when_time_hour = int(when_time_hour)
    if 0 < when_time_hour < 9:
        when_time_hour = when_time_hour + 12

    d = datetime.date(int(when_date_year), int(when_date_month), int(when_date_day))
    t = datetime.time(when_time_hour, int(when_time_minuite), 0)
    dt = datetime.datetime.combine(d, t)

    library = ""
    try:
        library = Library.objects.get(library_code=libGroup)
    except:
        pass

    # 도서관 코드 맞는 도서관 존재 할때만 이하 저장 실행.
    if library:

        # 이전월의 첫날 <=  상영일 <= 다음달의 마지막일 때만 저장.

        # 이전월의 첫날 <=  상영일 <= 다음달의 마지막일 때만 저장. (이거 해제 하겠씀.).
        # if dt >= before_months_first_day and dt <= after_months_last_day and dt >= now_date:

        # 현재 달보다 앞선것만 저장하자.
        if dt >= now_date:
            movie, movie_created_bool = Movie.objects.get_or_create(
                library=library,
                title=title,
                when=dt,
                place=place,
                runtime=runtime,
            )


# 영화 제목
# 일시
# 장소

# http://www.l4d.or.kr/library/index.php?g_page=culture&m_page=culture04&cate=&part=0&libCho=TOL&libGroup=MA&year=2018&month=9

#     ##### 동대문구 크롤러##### (월별)
def dongdaemungu_movie_crawler(year,libGroup):


    # 몇페이지 까지 있나 알아내기 위해 초반 패이징 텝 크롤링 해서 판단해야함 .

    params = {
        'manageCd': libGroup,
    }
    url = "https://www.l4d.or.kr/intro/menu/10111/program/30030/movieList.do?" + parse.urlencode(params)

    request = requests.get(url)
    response = request.text
    soup = BeautifulSoup(response, 'lxml')
    is_next_page = soup.select('p.paging > a ')

    if is_next_page:
        page_num_list = ['1', '2']
        print(f'more than 1 page {True}')
    else:
        page_num_list = ['1']
        print(f'more than 1 page {False}')




    # 각 페이지에 대해서 크롤링
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

            title_pre  = movie_li.select_one('dt.tit')

            if title_pre:
                title = title_pre.get_text(strip=True)
            else:
                # 해당 페이지에 영화 없는 것이기 때문에 for문 나가준다.
                break
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
                    # 18시 30분 이런식으로 표현시
                    elif re.findall('\d+\s*시\s*(\d+)\s*분', when):
                        when_time_hour = re.findall('(\d+)\s*시\s*\d+\s*분', when)[0]
                        when_time_minuite = re.findall('\d+\s*시\s*(\d+)\s*분', when)[0]
                    # 18시 이런식으로 표현될땐 ~
                    elif re.findall('(\d+)\s*시', when):
                        when_time_hour = re.findall('(\d+)시', when)[0]

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

            # 만약 한개의 영화 title이라도 크롤링 했을때만 영화 저장 단계 넘어간다. + 시간 크롤링 됬을때
            if title and when_time_hour:
                save_movie(when_time_hour, when_date_year, when_date_month, when_date_day, when_time_minuite, libGroup,
                           title, place, runtime)
                print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')



#    ##### 성동구 크롤러 ##### (페이지별) # 참고로 냄겨둠.(현제 원본 페이지 페쇄인듯)
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

            # 만약 한개의 영화 title이라도 크롤링 했을때만 영화 저장 단계 넘어간다.
            if title and when_time_hour:
                save_movie(when_time_hour, when_date_year, when_date_month, when_date_day, when_time_minuite, libGroup,
                           title, place, runtime)

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
                    runtime = re.findall('(\d\d*)', runtime_pre)
                    if runtime:
                        runtime = runtime[0]
                    print(f'runtime: {runtime}')  # 런타임

                elif index == 3:
                    #                     print(f'상영일자 : {dd.contents[1]}') #상영일자(날짜 + 시간 ) # 2018.10.27(토) 오후 2시 or 오후2시, 오전1시
                    when = dd.contents[1]
                    when_date = re.findall("(\S*)\(", when)
                    if when_date and len(when_date[0].split('.')) >=3:
                        when_date = when_date[0]  # 2018.10.27
                        when_date_year = when_date.split('.')[0]
                        when_date_month = when_date.split('.')[1]
                        when_date_day = when_date.split('.')[2]
                    print(f'when_date_year:{when_date_year}')
                    print(f'month : {when_date_month}')  # 상영 날짜
                    print(f'day : {when_date_day}')  #

                    when_time_pre = re.findall("\)\s*(.{4,6})시", when)

                    if when_time_pre:
                        when_time_pre = when_time_pre[0]

                    # print(f'상영 시간 : {when_time_pre}') # 상영 시간  # 오후 2시
                    if '오후' in when_time_pre:
                        when_time_hour = int(re.findall("오후(.*\d*)", when_time_pre)[0].strip()) + 12

                    elif '오전' in when_time_pre:
                        when_time_hour = int(re.findall("오전(.*\d*)", when_time_pre)[0].strip())

                    print(f'when_time_hour :{when_time_hour}')

                    print('@@@@@@@@@@@@@@@@@@')

            # 만약 한개의 영화 title이라도 크롤링 했을때만 영화 저장 단계 넘어간다. + 영화의 hour 크롤링 제대로 했을때
            if title and when_time_hour:
                save_movie(when_time_hour, when_date_year, when_date_month, when_date_day, when_time_minuite, area_code, #libGroup,
                           title, place, runtime)

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

                if title and when_time_hour:   # when_date_year
                    save_movie(when_time_hour, year, when_date_month, when_date_day, when_time_minuite,
                               area_code, # libGroup,
                               title, place, runtime)


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
                # 만약 한개의 영화 title이라도 크롤링 했을때만 영화 저장 단계 넘어간다. + 영화의 hour 크롤링 제대로 했을때

                if title and when_time_hour:  # when_date_year
                    save_movie(when_time_hour, year, when_date_month, when_date_day, when_time_minuite,
                               area_code,  # libGroup,
                               title, place, runtime)


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

                # 18시 30분 이런식으로 표현시
                if re.findall('\d+\s*시\s*(\d+)\s*분', when):
                    when_time_hour = re.findall('(\d+)\s*시\s*\d+\s*분', when)[0]
                    when_time_minuite = re.findall('\d+\s*시\s*(\d+)\s*분', when)[0]

                # 18시 이런식으로만 표현될땐 ~
                elif re.findall('(\d+)\s*시', when):
                    when_time_hour = re.findall('(\d+)시', when)[0]


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

        # 만약 한개의 영화 title이라도 크롤링 했을때만 영화 저장 단계 넘어간다. + 영화의 hour 크롤링 제대로 했을때
        if title and when_time_hour:
            save_movie(when_time_hour, when_date_year, when_date_month, when_date_day, when_time_minuite, libGroup,
                       title, place, runtime)

            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')


def seongbukgu_movie_crawler(libGroup):

    url = "https://www.sblib.seoul.kr/snlib/menu/10457/program/30124/movieList.do"

    request = requests.get(url)
    response = request.text
    soup = BeautifulSoup(response, 'lxml')

    movie_dls = soup.select('ul.movie-list dl')

    for movie_dl in movie_dls:

        title = ""  # 제목
        when = ""  # 일시
        when_date_year = 0
        when_date_month = 0
        when_date_day = 0
        when_time_hour = 0
        when_time_minuite = 0
        runtime = 0  # 런타임
        place = ""  # 장소

        title = movie_dl.select_one('dt').get_text(strip=True).replace("제 목", "")
        print(f'title: {title}')

        #     item_names_pre = movie_dl.select('dd > strong.tit')
        items_pre = movie_dl.select('dd')
        for item_pre in items_pre:
            item_name = item_pre.select_one('strong.tit').get_text(strip=True)

            if item_name == "시 간":
                runtime = item_pre.get_text(strip=True).replace("시 간", "")
                runtime = re.findall('(\d+)', runtime)[0]
                print(f'runtime: {runtime}')


            elif item_name == "상영날짜":
                when = item_pre.get_text(strip=True).replace("상영날짜", "")
                print(f'when: {when}')  # 2019.04.27.(토) 오후 4시

                when_date_year = re.findall('(\d\d\d\d).', when)[0]
                when_date_month = re.findall('\d\d\d\d.(\d{1,2}).', when)[0]
                when_date_day = re.findall('\d\d\d\d.\d{1,2}.(\d{1,2})', when)[0]

                # 18:00 이런식으로 표현시
                if re.findall('(\d{1,2}):', when):
                    when_time_hour = re.findall('(\d{1,2}):', when)[0]
                    when_time_minuite = re.findall('\d{1,2}:(\d{1,2})', when)[0]

                # 18시 30분 이런식으로 표현시
                elif re.findall('\d+\s*시\s*(\d+)\s*분', when):
                    when_time_hour = re.findall('(\d+)\s*시\s*\d+\s*분', when)[0]
                    when_time_minuite = re.findall('\d+\s*시\s*(\d+)\s*분', when)[0]

                # 18시 이런식으로 표현될땐 ~
                elif re.findall('(\d+)\s*시', when):
                    when_time_hour = re.findall('(\d+)시', when)[0]


                print(f'when_date_year: {when_date_year}')
                print(f'when_date_month: {when_date_month}')
                print(f'when_date_day: {when_date_day}')
                print(f'when_time_hour: {when_time_hour}')
                print(f'when_time_minuite: {when_time_minuite}')

            elif item_name == "상영장소":
                place = item_pre.get_text(strip=True).replace("상영장소", "")
                print(f'place: {place}')

        # 만약 한개의 영화 title이라도 크롤링 했을때만 영화 저장 단계 넘어간다. + 영화의 hour 크롤링 제대로 했을때
        if title and when_time_hour:
            save_movie(when_time_hour, when_date_year, when_date_month, when_date_day, when_time_minuite, libGroup,
                       title, place, runtime)

            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')


def songpagu_movie_crawler(libGroup):

    params = {
        'LIBCODE': libGroup,
    }
    url = "http://www.splib.or.kr/movie.do?" + parse.urlencode(params)

    request = requests.get(url)
    response = request.text
    soup = BeautifulSoup(response, 'lxml')

    movie_tables = soup.select('div.contents > table')

    for movie_table in movie_tables:
        title = ""  # 제목
        when = ""  # 일시
        when_date_year = 0
        when_date_month = 0
        when_date_day = 0
        when_time_hour = 0
        when_time_minuite = 0
        runtime = 0  # 런타임
        place = ""  # 장소

        items_pre = movie_table.select('tr')

        for item_pre in items_pre:
            item_name = item_pre.select_one('th').get_text(strip=True)

            if item_name == "제목":
                title = item_pre.select_one('td.tb').get_text(strip=True)
                print(f'title: {title}')

            elif item_name == "상영일시":
                when = item_pre.select_one('td').get_text(strip=True)
                print(f'when: {when}')  # 2019년 04월 07일 (일요일) 14시 00분

                when_date_year = re.findall('(\d\d\d\d)', when)[0]
                when_date_month = re.findall('(\d{1,2})\s*월', when)[0]
                when_date_day = re.findall('(\d{1,2})\s*일', when)[0]

                # 18:00 이런식으로 표현시
                if re.findall('(\d{1,2}):', when):
                    when_time_hour = re.findall('(\d{1,2}):', when)[0]
                    when_time_minuite = re.findall('\d{1,2}:(\d{1,2})', when)[0]
                # 18시 30분 이런식으로 표현시
                elif re.findall('\d+\s*시\s*(\d+)\s*분', when):
                    when_time_hour = re.findall('(\d+)\s*시\s*\d+\s*분', when)[0]
                    when_time_minuite = re.findall('\d+\s*시\s*(\d+)\s*분', when)[0]

                # 18시 이런식으로 표현될땐 ~
                elif re.findall('(\d+)\s*시', when):
                    when_time_hour = re.findall('(\d+)시', when)[0]

                print(f'when_date_year: {when_date_year}')
                print(f'when_date_month: {when_date_month}')
                print(f'when_date_day: {when_date_day}')
                print(f'when_time_hour: {when_time_hour}')
                print(f'when_time_minuite: {when_time_minuite}')


            elif item_name == "상영장소":
                place = item_pre.select_one('td').get_text(strip=True)
                print(f'place: {place}')

            elif item_name == "상영정보":
                runtime = item_pre.select_one('td').get_text(strip=True)

                if re.findall('(\d+)', runtime):
                    runtime = re.findall('(\d+)', runtime)[0]

                print(f'runtime: {runtime}')

        # 만약 한개의 영화 title이라도 크롤링 했을때만 영화 저장 단계 넘어간다. + 영화의 hour 크롤링 제대로 했을때
        if title and when_time_hour:
            save_movie(when_time_hour, when_date_year, when_date_month, when_date_day, when_time_minuite, libGroup,
                       title, place, runtime)

            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')



def yeongdeungpogu_movie_crawler(libGroup):

    if libGroup == "ydpllc":
        pass
    else:
        url = "http://www." + libGroup + ".or.kr/program/movieList.do"
        request = requests.get(url)
        response = request.text
        soup = BeautifulSoup(response, 'lxml')

        movie_tables = soup.select('div.contents > form > table')

        for movie_table in movie_tables:
            title = ""  # 제목
            when = ""  # 일시
            when_date_year = 0
            when_date_month = 0
            when_date_day = 0
            when_time_hour = 0
            when_time_minuite = 0
            runtime = 0  # 런타임
            place = ""  # 장소

            item_pres = movie_table.select('th')
            #         findNext('th').contents[0]

            for item_pre in item_pres:

                if item_pre.get_text() == "제목":
                    title_pre = item_pre.find_next_sibling()
                    if title_pre:
                        title = title_pre.get_text(strip=True)

                        if ']' in title:  # [우리말 자막]레고 배트맨 : 더 무비 이런경우 앞의 괄호부분없애줌.
                            title_before = title.split(']')
                            title = title_before[1]
                        elif '무료영화상영' and '"' in title:  # 무료영화상영 "아기배달부 스토크"  이경우 안쪽만 빼주자.
                            title_before_pre = re.findall('"(.*)"', title)
                            if title_before_pre:
                                title = title_before_pre[0]

                        print(f'title: {title}')
                    else:
                        break  # 제목 정보 없으면 다음영화 넘어감

                elif item_pre.get_text() == "상영일시":
                    when_pre = item_pre.find_next_sibling()
                    if when_pre:
                        when = when_pre.get_text(strip=True)
                        print(f'when: {when}')
                    else:
                        break  # 날짜 정보 없으면 다음영화 넘어감.

                    when_date_year_pre = re.findall('(\d\d\d\d)', when)
                    if when_date_year_pre:
                        when_date_year = when_date_year_pre[0]
                    when_date_month_pre = re.findall('\d\d\d\d\s*.\s*(\d{1,2})', when)
                    if when_date_month_pre:
                        when_date_month = when_date_month_pre[0]
                    when_date_day_pre = re.findall('\d\d\d\d\s*.\s*\d{1,2}\s*.\s*(\d{1,2})', when)
                    if when_date_day_pre:
                        when_date_day = when_date_day_pre[0]

                    # 18:00 이런식으로 표현시
                    if re.findall('(\d{1,2})\s*:', when):
                        when_time_hour_pre = re.findall('(\d{1,2})\s*:', when)
                        if when_time_hour_pre:
                            when_time_hour = when_time_hour_pre[0]
                        when_time_minuite_pre = re.findall('\d{1,2}\s*:\s*(\d{1,2})\s*', when)
                        if when_time_minuite_pre:
                            when_time_minuite = when_time_minuite_pre[0]
                    # 18시 30분 이런식으로 표현시
                    elif re.findall('\d+\s*시\s*(\d+)\s*분', when):
                        when_time_hour_pre = re.findall('(\d+)\s*시\s*\d+\s*분', when)
                        if when_time_hour_pre:
                            when_time_hour = when_time_hour_pre[0]
                        when_time_minuite_pre = re.findall('\d+\s*시\s*(\d+)\s*분', when)
                        if when_time_minuite_pre:
                            when_time_minuite = when_time_minuite_pre[0]

                    # 18시 이런식으로 표현될땐 ~
                    elif re.findall('(\d+)\s*시', when):
                        when_time_hour_pre = re.findall('(\d+)\s*시', when)
                        if when_time_hour_pre:
                            when_time_hour = when_time_hour_pre[0]

                    print(f'when_date_year: {when_date_year}')
                    print(f'when_date_month: {when_date_month}')
                    print(f'when_date_day: {when_date_day}')
                    print(f'when_time_hour: {when_time_hour}')
                    print(f'when_time_minuite: {when_time_minuite}')

                elif item_pre.get_text() == "상영장소":
                    place_pre = item_pre.find_next_sibling()
                    if place_pre:
                        place = place_pre.get_text(strip=True)
                        print(f'place: {place}')

                elif item_pre.get_text() == "상영정보":
                    if item_pre.find_next_sibling():
                        info_tuple = item_pre.find_next_sibling().get_text(strip=True)  # 98분 / 전체이용가
                        if re.findall('(\d+)', info_tuple):
                            runtime = re.findall('(\d+)', info_tuple)[0]
                            print(f'runtime: {runtime}')

            if title and when_time_hour:
                save_movie(when_time_hour, when_date_year, when_date_month, when_date_day, when_time_minuite, libGroup,
                           title, place, runtime)
            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')


def eunpyeonggu_movie_crawler(libGroup):
    url = "http://www." + libGroup + ".or.kr/culture/movie.asp"
    if libGroup == "gsvlib":
        url = url + "?mode=list&gubun=3"
    request = requests.get(url)
    response = request.text
    soup = BeautifulSoup(response, 'lxml')
    movie_tables = soup.select('div.tableF > ul.clear > li > dl.book_exp')  # 영화 없으면 아예 아래 포문 안들어가게 하겠슴.

    for movie_table in movie_tables:
        title = ""  # 제목
        when = ""  # 일시
        when_date_year = 0
        when_date_month = 0
        when_date_day = 0
        when_time_hour = 0
        when_time_minuite = 0
        runtime = 0  # 런타임
        place = ""  # 장소

        # 제목 따로 dt테그라 먼저 찾겠슴
        title_pre = movie_table.select_one('dt')
        if title_pre:
            title = title_pre.get_text(strip=True)
            if re.findall('\((.*)\)', title):  # 이월 (독립영화),(더빙),(자막) 등 빼주기위함.
                title_before_pre = re.findall('(.*)\(.*\)', title)
                if title_before_pre:
                    title = title_before_pre[0]
            print(f'title: {title}')
        else:
            print('영화제목없음')
            continue  # 타이틀 없으면 다음 영화로 넘어감.

        # 나머지정보들 묶여서 한번에 크롤링
        item_pres = movie_table.select('dd > p')
        for item_pre in item_pres:
            item_name_pre = item_pre.get_text()

            if "상영일시" in item_name_pre:

                when = item_name_pre
                print(f'when: {when}')

                when_date_year_pre = re.findall('(\d\d\d\d)', when)
                if when_date_year_pre:
                    when_date_year = when_date_year_pre[0]
                when_date_month_pre = re.findall('\d\d\d\d\s*-\s*(\d{1,2})', when)
                if when_date_month_pre:
                    when_date_month = when_date_month_pre[0]
                when_date_day_pre = re.findall('\d\d\d\d\s*-\s*\d{1,2}\s*-\s*(\d{1,2})', when)
                if when_date_day_pre:
                    when_date_day = when_date_day_pre[0]

                if libGroup in ["eplib", "enlib"]:  # 이 두 사이트는 공지사항에만 몇시인지 따로 명시해놓음
                    when_time_hour = "14"
                    when_time_minuite = "0"

                    # 18:00 이런식으로 표현시
                elif re.findall('(\d{1,2})\s*:', when):
                    when_time_hour_pre = re.findall('(\d{1,2})\s*:', when)
                    if when_time_hour_pre:
                        when_time_hour = when_time_hour_pre[0]
                    when_time_minuite_pre = re.findall('\d{1,2}\s*:\s*(\d{1,2})\s*', when)
                    if when_time_minuite_pre:
                        when_time_minuite = when_time_minuite_pre[0]
                # 18시 30분 이런식으로 표현시
                elif re.findall('\d+\s*시\s*(\d+)\s*분', when):
                    when_time_hour_pre = re.findall('(\d+)\s*시\s*\d+\s*분', when)
                    if when_time_hour_pre:
                        when_time_hour = when_time_hour_pre[0]
                    when_time_minuite_pre = re.findall('\d+\s*시\s*(\d+)\s*분', when)
                    if when_time_minuite_pre:
                        when_time_minuite = when_time_minuite_pre[0]

                # 18시 이런식으로 표현될땐 ~
                elif re.findall('(\d+)\s*시', when):
                    when_time_hour_pre = re.findall('(\d+)\s*시', when)
                    if when_time_hour_pre:
                        when_time_hour = when_time_hour_pre[0]

                print(f'when_date_year: {when_date_year}')
                print(f'when_date_month: {when_date_month}')
                print(f'when_date_day: {when_date_day}')
                print(f'when_time_hour: {when_time_hour}')
                print(f'when_time_minuite: {when_time_minuite}')


            elif "장소" in item_name_pre:
                place_pre = item_name_pre.split('장소')
                if place_pre:
                    place = place_pre[1]
                    print(f'place: {place}')

            # 상영시간에 상영 일시 적힌곳있어서... 상영일시에서 시간,분 0,0인것에한해서
            # 여기서 상영일시 시간, 분을 얻어보겠다. (런타임은 일괄적으로 안뽑겠다.
            # 여기서도 안뽑히면 0시 0분으로 갈수밖에 없음.  ->이경우 저장안됨.
            elif "상영시간" in item_name_pre:
                when_time_hour_pre = ""
                when_time_minute_pre = ""

                # 18:00 이런식으로 표현시
                if re.findall('(\d{1,2})\s*:', item_name_pre):
                    when_time_hour_pre = re.findall('(\d{1,2})\s*:', item_name_pre)
                    when_time_minuite_pre = re.findall('\d{1,2}\s*:\s*(\d{1,2})\s*', item_name_pre)
                # 18시 30분 이런식으로 표현시
                elif re.findall('\d+\s*시\s*(\d+)\s*분', item_name_pre):
                    when_time_hour_pre = re.findall('(\d+)\s*시\s*\d+\s*분', item_name_pre)
                    when_time_minuite_pre = re.findall('\d+\s*시\s*(\d+)\s*분', item_name_pre)

                # 18시 이런식으로 표현될땐 ~
                elif re.findall('(\d+)\s*시', item_name_pre):
                    when_time_hour_pre = re.findall('(\d+)\s*시', item_name_pre)

                # 위에 규칙대로 상영시간에서 hour뽑혔다면  -> 상영시간 (시간,분) 여기 적혀있는것. -> 이것으로최신화
                if when_time_hour_pre:
                    when_time_hour = when_time_hour_pre[0]
                    print(f'when_time_hour: {when_time_hour}  (상영시간에서 추출해서 이것으로변경)')
                if when_time_minute_pre:
                    when_time_minuite = when_time_minuite_pre[0]
                    print(f'when_time_minuite: {when_time_minuite} (상영시간에서 추출해서 이것으로변경)')  # 0에서 ->0 바귄것이면 안뜸.

        if title and when_time_hour:
            save_movie(when_time_hour, when_date_year, when_date_month, when_date_day, when_time_minuite, libGroup,
                       title, place, runtime)
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')


# 서울시 교육청 통합 크롤러 약 100개 이상 한번에 크롤
def seoul_massive_crawler(year,month):

    # 요청 거부시 10초후 제시도 하는 함수
    def get_url_data(url, max_tries=10):
        for n in range(max_tries):
            try:
                return requests.get(url)
            except requests.exceptions.RequestException:
                if n == max_tries - 1:
                    raise
                time.sleep(10)

    year = str(year)
    month = str(month)
    if len(month) ==1:
        month = '0' + month

    # 페이지 번호 뽑기위해 초벌 크롤
    url = "https://lib.sen.go.kr/lib/board/index.do?plan_date=" + year + "-" + month + "&menu_idx=12&manage_idx=1121&board_idx=0&rowCount=50&plan_year=" + year + "&plan_month=" + month + "&viewPage=1&search_type=title%2Bcontent"
    request = get_url_data(url)
    response = request.text
    soup = BeautifulSoup(response, 'lxml')

    # 페이지 부터 뽑고 그것을 포문 돌아 보겠슴.
    pages = []

    page_button_parent = soup.find("div", {"id": "board_paging"})
    if page_button_parent:
        page_button = page_button_parent.select("a.paginate_button")
        if page_button:
            for i in range(len(page_button)):
                pages.append(i + 1)

    print(pages)
    count = 0
    for page in pages:
        url = "https://lib.sen.go.kr/lib/board/index.do?plan_date=" + year + "-" + month + "&menu_idx=12&manage_idx=1121&board_idx=0&rowCount=50&plan_year=" + year + "&plan_month=" + month + "&viewPage=" + str(
            page) + "&search_type=title%2Bcontent"
        request = get_url_data(url)
        response = request.text
        soup = BeautifulSoup(response, 'lxml')

        movie_tables = soup.select('div.search-results > div.row')  # 영화 없으면 아예 아래 포문 안들어가게 하겠슴.

        for movie_table in movie_tables:
            count += 1

            title = ""  # 제목
            when = ""  # 일시
            when_date_year = 0
            when_date_month = 0
            when_date_day = 0
            when_time_hour = 0
            when_time_minuite = 0
            runtime = 0  # 런타임
            place = ""  # 장소

            libGroup = ""

            # 제목 따로 a테그라 먼저 찾겠슴
            title_pre = movie_table.select_one('div.box > div.item > div.bif > a.name')

            if title_pre:
                title = title_pre.get("title")

                if re.findall('\(.+\)\s*(.+)', title):  # (독립영화) 이월
                    title_before_pre = re.findall('\(.+\)\s*(.+)', title)
                    if title_before_pre:
                        title = title_before_pre[0]
                elif re.findall('(.+)\s*\(.+\)', title):  # 이월 (독립영화),(더빙),(자막) 등 빼주기위함.
                    title_before_pre = re.findall('(.+)\s*\(.+\)', title)
                    if title_before_pre:
                        title = title_before_pre[0]
                elif re.findall('\[.+\]\s*(.+)', title):  # [강서스크린] 웃는남자
                    title_before_pre = re.findall('\[.+\]\s*(.+)', title)
                    if title_before_pre:
                        title = title_before_pre[0]
                elif re.findall('(.+)\s*\[.+\]', title):  # 웃는남자 [강서스크린]
                    title_before_pre = re.findall('(.+)\s*\[.+\]', title)
                    if title_before_pre:
                        title = title_before_pre[0]
                elif re.findall('용산시네마여행_(.+)', title):  # 용산시네마여행_
                    title_before_pre = re.findall('용산시네마여행_(.+)', title)
                    if title_before_pre:
                        title = title_before_pre[0]
                elif re.findall('독립영화상영_(.+)', title):  # 독립영화상영_
                    title_before_pre = re.findall('독립영화상영_(.+)', title)
                    if title_before_pre:
                        title = title_before_pre[0]
                elif re.findall('힐링뮤직박스_(.+)', title):  # 힐링뮤직박스_
                    title_before_pre = re.findall('힐링뮤직박스_(.+)', title)
                    if title_before_pre:
                        title = title_before_pre[0]
                print(f'title: {title}')
            else:
                print('영화제목없음')
                continue  # 타이틀 없으면 다음 영화로 넘어감.

            # 나머지정보들 묶여서 한번에 크롤링
            item_pres = movie_table.select('div.box > div.item > div.bif > ul.con2 > li')

            found_libgroup = False  # 아래 코드 뽑을때 한번만 get하기 위함.
            for item_pre in item_pres:

                # 도서관 코드 뽑는것 추가.
                if not found_libgroup and item_pre.get('class'):
                    libGroup = item_pre.get('class')[0]
                    found_libgroup = True

                item_name_pre = item_pre.get_text()
                if "상영일시" in item_name_pre:

                    when = item_name_pre
                    #                     print(f'when: {when}')

                    when_date_year_pre = re.findall('(\d\d\d\d)', when)
                    if when_date_year_pre:
                        when_date_year = when_date_year_pre[0]
                    when_date_month_pre = re.findall('\d\d\d\d\s*-\s*(\d{1,2})', when)
                    if when_date_month_pre:
                        when_date_month = when_date_month_pre[0]
                    when_date_day_pre = re.findall('\d\d\d\d\s*-\s*\d{1,2}\s*-\s*(\d{1,2})', when)
                    if when_date_day_pre:
                        when_date_day = when_date_day_pre[0]

                    # 18:00 이런식으로 표현시
                    if re.findall('(\d{1,2})\s*:', when):
                        when_time_hour_pre = re.findall('(\d{1,2})\s*:', when)
                        if when_time_hour_pre:
                            when_time_hour = when_time_hour_pre[0]
                        when_time_minuite_pre = re.findall('\d{1,2}\s*:\s*(\d{1,2})\s*', when)
                        if when_time_minuite_pre:
                            when_time_minuite = when_time_minuite_pre[0]
                    # 18시 30분 이런식으로 표현시
                    elif re.findall('\d+\s*시\s*(\d+)\s*분', when):
                        when_time_hour_pre = re.findall('(\d+)\s*시\s*\d+\s*분', when)
                        if when_time_hour_pre:
                            when_time_hour = when_time_hour_pre[0]
                        when_time_minuite_pre = re.findall('\d+\s*시\s*(\d+)\s*분', when)
                        if when_time_minuite_pre:
                            when_time_minuite = when_time_minuite_pre[0]

                    # 18시 이런식으로 표현될땐 ~
                    elif re.findall('(\d+)\s*시', when):
                        when_time_hour_pre = re.findall('(\d+)\s*시', when)
                        if when_time_hour_pre:
                            when_time_hour = when_time_hour_pre[0]

                    print(f'when_date_year: {when_date_year}')
                    print(f'when_date_month: {when_date_month}')
                    print(f'when_date_day: {when_date_day}')
                    print(f'when_time_hour: {when_time_hour}')
                    print(f'when_time_minuite: {when_time_minuite}')


                elif "상영장소" in item_name_pre:
                    place_pre = item_name_pre.split(':')
                    if place_pre:
                        place = place_pre[1]
                        print(f'place: {place}')

                elif "상영시간" in item_name_pre:
                    runtime_pre = re.findall('(\d+)', item_name_pre)
                    if runtime_pre:
                        runtime = runtime_pre[0]
                        print(f'runtime: {runtime}')

            print(f'libGroup : {libGroup}')

            if title and when_time_hour:
                save_movie(when_time_hour, when_date_year, when_date_month, when_date_day, when_time_minuite, libGroup,
                           title, place, runtime)

            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')


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

        story_pre = soup.select_one('div.story_area > p.con_tx')
        if story_pre:
            story = story_pre.get_text()

            # 제작노트 같이 크롤링 된다면 잘라서 저장 하겠다.


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
            "성북구": {"num": 0, "list": []},
            "송파구": {"num": 0, "list": []},
            "영등포구": {"num": 0, "list": []},
            "은평구": {"num": 0, "list": []},
            "양천구": {"num": 0, "list": []},
            "서대문구": {"num": 0, "list": []},
            "마포구": {"num": 0, "list": []},
            "동작구": {"num": 0, "list": []},
            "도봉구": {"num": 0, "list": []},
            "노원구": {"num": 0, "list": []},
            "용산구": {"num": 0, "list": []},
            "구로구": {"num": 0, "list": []},
            "강서구": {"num": 0, "list": []},
            "강동구": {"num": 0, "list": []},
            "강남구": {"num": 0, "list": []},
            "종로구": {"num": 0, "list": []},
        },
        "no_extra_info_movie": {
            "동대문구": {"num": 0, "list": []},
            "성동구": {"num": 0, "list": []},
            "광진구": {"num": 0, "list": []},
            "중랑구": {"num": 0, "list": []},
            "성북구": {"num": 0, "list": []},
            "송파구": {"num": 0, "list": []},
            "영등포구": {"num": 0, "list": []},
            "은평구": {"num": 0, "list": []},
            "양천구": {"num": 0, "list": []},
            "서대문구": {"num": 0, "list": []},
            "마포구": {"num": 0, "list": []},
            "동작구": {"num": 0, "list": []},
            "도봉구": {"num": 0, "list": []},
            "노원구": {"num": 0, "list": []},
            "용산구": {"num": 0, "list": []},
            "구로구": {"num": 0, "list": []},
            "강서구": {"num": 0, "list": []},
            "강동구": {"num": 0, "list": []},
            "강남구": {"num": 0, "list": []},
            "종로구": {"num": 0, "list": []},
        },
        "total_movie": {
            "동대문구": {"before": 0, "now": 0, "after": 0},
            "성동구": {"before": 0, "now": 0, "after": 0},
            "광진구": {"before": 0, "now": 0, "after": 0},
            "중랑구": {"before": 0, "now": 0, "after": 0},
            "성북구": {"before": 0, "now": 0, "after": 0},
            "송파구": {"before": 0, "now": 0, "after": 0},
            "영등포구": {"before": 0, "now": 0, "after": 0},
            "은평구": {"before": 0, "now": 0, "after": 0},
            "양천구": {"before": 0, "now": 0, "after": 0},
            "서대문구": {"before": 0, "now": 0, "after": 0},
            "마포구": {"before": 0, "now": 0, "after": 0},
            "동작구": {"before": 0, "now": 0, "after": 0},
            "도봉구": {"before": 0, "now": 0, "after": 0},
            "노원구": {"before": 0, "now": 0, "after": 0},
            "용산구": {"before": 0, "now": 0, "after": 0},
            "구로구": {"before": 0, "now": 0, "after": 0},
            "강서구": {"before": 0, "now": 0, "after": 0},
            "강동구": {"before": 0, "now": 0, "after": 0},
            "강남구": {"before": 0, "now": 0, "after": 0},
            "종로구": {"before": 0, "now": 0, "after": 0},
        },
        # "deleted_movie": {
        #     "동대문구": {"num": 0, "list": []},
        #     "성동구": {"num": 0, "list": []},
        #     "광진구": {"num": 0, "list": []},
        #     "중랑구": {"num": 0, "list": []},
        #     "성북구": {"num": 0, "list": []},
        #     "송파구": {"num": 0, "list": []},
        #     "영등포구": {"num": 0, "list": []},
        #     "은평구": {"num": 0, "list": []},
        # },
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

    ###### 성북구 크롤러 #####
    seongbukgu_area_code = "snlib"  # 한곳이라 걍 변수로만함.
    seongbukgu_movie_crawler(seongbukgu_area_code)
    print(f'{seongbukgu_area_code}#############################################################################################################################')

    ###### 송파구 크롤러 #####
    songpagu_area_code_list = ['SPJ', 'SPC', 'SPG', 'SPE', 'SP1', 'SP2', 'SP3', 'SP4', 'SPM']

    for libGroup in songpagu_area_code_list:
        songpagu_movie_crawler(libGroup)
        print(f'{libGroup} #####################################################################################################################################')


    ###### 영등포구 크롤러 ######
    # yeongdeungpogu_area_code_list = ["ydpllc", "mllib","dllib","sylib"]
    yeongdeungpogu_area_code_list = ["mllib","dllib","sylib"]  # 19.6.6부로 "ydpllc",는 seoul_massive_crawler로 넘어감  서울특별시 교육청 산하는 한번에 크롤링

    for libGroup in yeongdeungpogu_area_code_list:
        yeongdeungpogu_movie_crawler(libGroup)
        print(f'{libGroup} #####################################################################################################################################')


    ###### 은평구 크롤러 ######
    eunpyeonggu_area_code_list = ["eplib", "enlib", "jsplib", "ealib", "gsvlib"]

    for libGroup in eunpyeonggu_area_code_list:
        eunpyeonggu_movie_crawler(libGroup)
        print(f'{libGroup} #####################################################################################################################################')

    ######서울특별시 교육청 통합 크롤러 ########
    print("######서울특별시 교육청 통합 크롤러 ######################################################################################################################")
    seoul_massive_crawler(year, month)



    # 현제시간 - 5분
    now_date_before_5_min = timezone.now() - timezone.timedelta(minutes=5)

    # 상영시간 naive한 datetime으로 변환


    # 위에서 크롤링한 movie들의 extra 정보들을 update하는 함수 호출한다.
    for movie in Movie.objects.all():

        # 초벌 크롤링시 저장된 시간이 현제시간 -5분 보다 큰것(이후인것) 들만 업데이트 함수 적용시키겠다(-> 기존에는 월 중에 새로 업데이트 되는것은 새로크롤링한것이니까 그것만 업데이트 하려고 이조건 넣었었다. -> 근데묹제가 옛날거도 로그에 쌓이는데 왜지?
        if movie.created_at  > now_date_before_5_min:
            title = movie.title
            get_extra_info(movie, title)

        # # 삭제될 영화 타이틀 로그에 저장 ( 이거 당분간 안쓸거라 빼줌.. 애러도 뭔가 있다. )
        # if not movie.when >= before_months_first_day_aware and movie.when <= after_months_last_day_aware:
        #     dict_log["deleted_movie"][movie.library.library_district.district_name]["num"] += 1
        #     dict_log["deleted_movie"][movie.library.library_district.district_name]["list"].append(movie.title)
        #     movie.delete()

        # 토탈 영화 갯수 구별로 달끊어서 로그 저장.
        # 이전월의첫날 <= 상영일 <= 다음월 마지막달 인 영화 count
        if (movie.when >= before_months_first_day_aware) and (movie.when < now_months_first_day_aware):
            dict_log["total_movie"][movie.library.library_district.district_name]["before"] += 1

        elif (movie.when >= now_months_first_day_aware) and (movie.when < after_months_first_day_aware):
            dict_log["total_movie"][movie.library.library_district.district_name]["now"] += 1

        elif (movie.when >= after_months_first_day_aware) and (movie.when <= after_months_last_day_aware):
            dict_log["total_movie"][movie.library.library_district.district_name]["after"] += 1

    return dict_log

