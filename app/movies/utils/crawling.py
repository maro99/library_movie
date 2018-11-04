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
import urllib.request as req

import datetime
from urllib import parse


# 영화 제목
# 일시
# 장소

# http://www.l4d.or.kr/library/index.php?g_page=culture&m_page=culture04&cate=&part=0&libCho=TOL&libGroup=MA&year=2018&month=9

#     ##### 동대문구 크롤러##### (월별)
def dongdaemungu_movie_crawler(year,libGroup):
    params = {
        'libGroup': libGroup,
    }
    url = "http://www.l4d.or.kr/library/index.php?g_page=culture&m_page=culture04&" + parse.urlencode(params)

    request = requests.get(url)
    response = request.text
    soup = BeautifulSoup(response, 'lxml')

    # 영화별 정보 담은 박스
    data_boxes = soup.select('div.data_wrapper')

    for data_box in data_boxes:

        pic_url = ""  # 사진
        title = ""  # 제목
        when = ""  # 일시
        when_date_year = 0
        when_date_month = 0
        when_date_day = 0
        when_time_hour = 0
        when_time_minuite = 0
        runtime = 0  # 런타임
        place = ""  # 장소

        # 사진 뽑기
        pic_url = data_box.select_one('div.pic > a > img').get('src')
        # 사진 url을 뽑아보니 두가지 경우가 있다.
        # http로 시작 하는 경우, 상대결로로서 l4d주소 있다 가정하고 뒷주소만 있는경우

        # 뒷 주소만 있는경우 ../경로표시 빼고 l4d 주소 더해준다.
        if not re.findall('http://', pic_url):
            pic_url = 'http://www.l4d.or.kr/' + re.findall('\..(.*)', pic_url)[0]

        # @ 사진
        print(f'pic_url: {pic_url}')

        # 제목 뽑기
        title = data_box.select_one('h3.recom_title > a').get_text(strip=True)
        # @ 제목
        print(f'title: {title}')

        # 나머지 정보들 뽑기.

        #         print(data_box.prettify())

        #         <li>
        #           <span class="fb">
        #            일시
        #           </span>
        #           : 2018.09.02 13:00 (일)
        #          </li>
        #
        #          이런식으로 리스트들이 들어있는데
        #          li를 자식인 span.fb의 text인 일시 를 기준으로 찾고 싶다.
        #          즉 기준이되는 찾은 테그의 부모의 택스트를 가져오고 싶은것.

        # 여기서 선택 된 것은 tag리스트이고
        # 이중 text가 일시 인것을 먼저 찾아보겠다.

        span_tags = data_box.select('ul > li > span.fb')
        #         print(span_tags)

        for span_tag in span_tags:
            span_tag_text = span_tag.get_text(strip=True)

            if span_tag_text == "일시":
                when = span_tag.parent.get_text(strip=True)  # 일시: 2018.10.07 16:00 (일)
                when_date_year = re.findall('\s(\d\d\d\d).', when)[0]
                when_date_month = re.findall('\d\d\d\d.(\d{1,2}).', when)[0]
                when_date_day = re.findall('\d\d\d\d.\d*.(\d{1,2})\s', when)[0]
                when_time_hour = re.findall('\s(\d\d):', when)[0]
                when_time_minuite = re.findall('\s\d\d:(\d\d)', when)[0]
                print(f'when_date_year: {when_date_year}')
                print(f'when_date_month: {when_date_month}')
                print(f'when_date_day: {when_date_day}')
                print(f'when_time_hour: {when_time_hour}')
                print(f'when_time_minuite: {when_time_minuite}')

            elif span_tag_text == "장소":
                place_pre = span_tag.parent.get_text(strip=True)  # 장소: 지하2층 시청각실
                place = re.findall('장소:\s*(.*)', place_pre)[0]
                print(f'place: {place}')

            elif span_tag_text == "시간":
                runtime_pre = span_tag.parent.get_text(strip=True)  # 시간: 92분
                runtime = re.findall('시간:\s*(\d*)', runtime_pre)[0]
                print(f'runtime: {runtime}')

        # pic_url = ""  # 사진
        # title = ""  # 제목
        # when = ""  # 일시
        # when_date_year = ""
        # when_date_month = ""
        # when_date_day = ""
        # when_time_hour = ""
        # when_time_minuite = ""
        # runtime = ""  # 런타임
        # place = ""  # 장소


        d = datetime.date(int(when_date_year),int(when_date_month),int(when_date_day))
        t = datetime.time(int(when_time_hour),int(when_time_minuite),0)
        dt = datetime.datetime.combine(d, t)

        library = Library.objects.get(library_code=libGroup)
        print(library)

        movie,movie_created_bool = Movie.objects.get_or_create(
            library = library,
            title = title,
            when = dt,
            place = place,
            runtime = runtime,
            thumbnail_url = pic_url
        )


        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')


#    ##### 성동구 크롤러 ##### (페이지별)

def seongdonggu_movie_crawler(area_code, year):
    # 페이지 1~3를 탐색해서 해당 월에 상영하는 작품만 가져오자.
    for page in range(1, 3):

        params = {
            'page': page
        }

        url = "https://www.sdlib.or.kr/" + area_code + "/U07080.asp?viewtype=list&" + parse.urlencode(params)
        #     url = "https://www.sdlib.or.kr/SD/U07080.asp?viewtype=list&page=1&libno="

        ssl._create_default_https_context = ssl._create_unverified_context
        res = req.urlopen(url)
        soup = BeautifulSoup(res, 'lxml')

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

            movie, movie_created_bool = Movie.objects.get_or_create(
                library=library,
                title=title,
                when=dt,
                place=place,
                runtime=runtime,
                thumbnail_url=pic_url,
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

            movie, movie_created_bool = Movie.objects.get_or_create(
                library=library,
                title=title,
                when=dt,
                place=place,
                runtime=runtime,
                thumbnail_url=pic_url
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

                movie, movie_created_bool = Movie.objects.get_or_create(
                    library=library,
                    title=title,
                    when=dt,
                    place=place,
                    runtime=runtime,
                    thumbnail_url=pic_url
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

                movie, movie_created_bool = Movie.objects.get_or_create(
                    library=library,
                    title=title,
                    when=dt,
                    place=place,
                    runtime=runtime,
                    thumbnail_url=pic_url
                )


#             구의제3동도서관에서는 '문화가 있는 날'을 맞아 무료영화 상영을 통해 관내 주민의 문화생활 및 여가활용에 이바지 하고자합니다.

#             ◈ 일시 : 10월 31일(수) 16:30~18:35

#             ◈ 영화명 : 우리는 동물원을 샀다

#             ◈ 상영등급 : 전체 관람가

#             ◈ 상영장소 : 도서관 소강의실


#     table_rows = soup.select('table.table700 > tbody > tr')


def get_extra_info(movie,title):

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
    detail_url_pre = soup.select_one('ul.search_list_1 > li > dl > dt > a')

    if detail_url_pre:
        pic_url =""
        rating = 0
        genre = ""
        director =""
        age =""
        story =""

        # detail로 가는 url
        detail_url = 'https://movie.naver.com' + detail_url_pre.get('href')

        soup = get_soup(detail_url)

        pic_url_pre = soup.select_one('div.poster > a > img')
        if pic_url_pre:
            pic_url = pic_url_pre.get('src')
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

        # 썸네일이 이미 없는 경우에만 업데이트를 하자
        if movie.thumbnail_url == "":
            movie.thumbnail_url = pic_url

        movie.rating = float(rating)
        movie.genre = genre
        movie.director = director
        movie.age = age
        movie.story = story
        movie.save()



def main_movie_crawler():
    # 오늘 날짜 먼저 가져옴
    now = datetime.datetime.now()
    year = now.year
    day = now.day
    month = now.month

    ##### 동대문구 크롤러#####

    dongdaemungu_area_code_list = ['MA', 'MF', 'MB', 'MC', 'MJ']
    # 정보화,답십리, 장안, 용두, 휘셩 (이문 제외)
    #     dongdaemungu_area_code_list = ['MA']

    for libGroup in dongdaemungu_area_code_list:
        dongdaemungu_movie_crawler(year,libGroup)
        print(
            f'{libGroup} #####################################################################################################################################')

    #### 성동구 크롤러 #####

    seongdonggu_area_code_list = ['SD','YD','SS','KH','CG']
    # 성동구립,용답, 장안, 성수, 금호,청계
#     seongdonggu_area_code_list = ['SD']

    for area_code in seongdonggu_area_code_list:
        seongdonggu_movie_crawler(area_code,year)
        print(f'{area_code}#############################################################################################################################')


    ##### 광진구 크롤러 #####
    gwangjingu_area_code_list = ['gjinfo','jgsports','gu3dong']
#     정보 , 중곡문화체육센터, 구의제3동
    for area_code in gwangjingu_area_code_list:
        gwangjingu_movie_crawler(area_code,year,month)
        print(f'{area_code}#############################################################################################################################')



    # 위에서 크롤링한 movie들의 extra 정보들을 update하는 함수 호출한다.

    for movie in Movie.objects.all():
        title = movie.title
        get_extra_info(movie, title)