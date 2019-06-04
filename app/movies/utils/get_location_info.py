from ..models.locations import *

def get_info():

# crawling_then_send_result_email 에서 호출중 .

    district_library_info_dict = {
        "동대문구": [
            {
                'name': "동대문구정보화도서관",
                'code': 'MA',
                'address': '서울특별시 동대문구 청량리동 206-19',
                'lat': '37.590052',
                'lng': '127.047285',
            },
            {
                'name': "동대문구답십리도서관",
                'code': 'MF',
                'address': '서울특별시 동대문구 답십리동 서울시립대로4길',
                'lat': '37.573174',
                'lng': '127.050502',
            },
            {
                'name': "장안어린이도서관",
                'code': 'MB',
                'address': '서울특별시 동대문구 장안동 342-23',
                'lat': '37.571186',
                'lng': '127.073236',
            },
            {
                'name': "용두어린이도서관",
                'code': 'MC',
                'address': '서울특별시 동대문구 용두동 무학로 133',
                'lat': '37.576061',
                'lng': '127.030280',
            },
            {
                'name': "휘경어린이도서관",
                'code': 'MJ',
                'address': '서울특별시 동대문구 휘경동 282-4',
                'lat': '37.588647',
                'lng': '127.060600',
            },
        ],

        "성동구": [
            {
                'name': "성동구립도서관",
                'code': 'SD',
                'address': '서울특별시 성동구 행당1동 고산자로10길 9',
                'lat': '37.559190',
                'lng': '127.034921',
            },
            {
                'name': "용답도서관",
                'code': 'YD',
                'address': '서울특별시 성동구 용답동 용답중앙3길 10',
                'lat': '37.566697',
                'lng': '127.051305',
            },
            {
                'name': "성수도서관",
                'code': 'SS',
                'address': '서울특별시 성동구 성수1가1동 뚝섬로1길 43',
                'lat': '37.545410',
                'lng': '127.046955',
            },
            {
                'name': "금호도서관",
                'code': 'KH',
                'address': '서울특별시 성동구 금호1가동 난계로 20',
                'lat': '37.554073',
                'lng': '127.024897',

            },
            {
                'name': "청계도서관",
                'code': 'CG',
                'address': '서울특별시 성동구 상왕십리동 마장로 141',
                'lat': '37.567893',
                'lng': '127.025453',
            },
        ],
        "광진구": [
            {
                'name': "광진정보도서관",
                'code': 'gjinfo',
                'address': '서울특별시 광진구 광장동 아차산로78길 90',
                'lat': '37.550615',
                'lng': '127.110398',
            },
            {
                'name': "중곡문화체육센터도서관",
                'code': 'jgsports',
                'address': '서울특별시 광진구 중곡동 168-8',
                'lat': '37.567748',
                'lng': '127.084711',
            },
            {
                'name': "구의제3동도서관",
                'code': 'gu3dong',
                'address': '서울특별시 광진구 구의3동 강변역로 17',
                'lat': '37.538108',
                'lng': '127.091892',
            },
        ],
        "중랑구": [
            {
                'name': "중랑구립정보도서관",
                'code': 'JMA',
                'address': '서울특별시 중랑구 신내로15길 197',
                'lat': '37.615254',
                'lng': '127.086901',
            },
        ],
        "성북구": [
            {
                'name': "종암동새날도서관",
                'code': 'snlib',
                'address': '서울특별시 성북구 종암로 98-8',
                'lat': '37.599045',
                'lng': '127.035207',
            },
        ],
        "송파구": [
            {
                'name': "송파글마루도서관",
                'code': 'SPJ',
                'address': '서울특별시 송파구 충민로 120',
                'lat': '37.480894',
                'lng': '127.130359',
            },
            {
                'name': "송파어린이도서관",
                'code': 'SPC',
                'address': '서울 송파구 올림픽로 105',
                'lat': '37.512170',
                'lng': '127.082413',
            },
            {
                'name': "거마도서관",
                'code': 'SPG',
                'address': '서울특별시 송파구 거마로2길 19',
                'lat': '37.493524',
                'lng': '127.146837',
            },
            {
                'name': "송파어린이영어작은도서관",
                'code': 'SPE',
                'address': '서울 송파구 오금로 1',
                'lat': '37.521866',
                'lng': '127.103285',
            },
            {
                'name': "소나무언덕1호작은도서관",
                'code': 'SP1',
                'address': '서울 송파구 올림픽로47길 9',
                'lat': '37.527229',
                'lng': '127.117745',
            },
            {
                'name': "소나무언덕2호작은도서관",
                'code': 'SP2',
                'address': '서울 송파구 석촌호수로 155',
                'lat': '37.507229',
                'lng': '127.094223',
            },
            {
                'name': "소나무언덕3호작은도서관",
                'code': 'SP3',
                'address': '서울특별시 송파구 성내천로 319',
                'lat': '37.492304',
                'lng': '127.156633',
            },
            {
                'name': "소나무언덕4호작은도서관",
                'code': 'SP4',
                'address': '서울 송파구 송이로 34',
                'lat': '37.502192',
                'lng': '127.116845',
            },
            {
                'name': "소나무언덕잠실본동작은도서관",
                'code': 'SPM',
                'address': '서울 송파구 탄천동로 211',
                'lat': '37.502947',
                'lng': '127.077464',
            },
        ],
        "영등포구": [
            {
                'name': "서울특별시교육청 영등포평생학습관",
                'code': 'ydpllc',
                'address': '서울특별시 영등포구 버드나루로15길 10 영등포평생학습관',
                'lat': '37.526422',
                'lng': '126.907414',
            },
            {
                'name': "문래정보문화도서관",
                'code': 'mllib',
                'address': '서울특별시 영등포구 문래로20길 49 카튼빌',
                'lat': '37.516796',
                'lng': '126.890921',
            },
            {
                'name': "대림정보문화도서관",
                'code': 'dllib',
                'address': '서울특별시 영등포구 도신로 27 대림정보문화도서관',
                'lat': '37.504376',
                'lng': '126.896058',
            },
            {
                'name': "선유정보문화도서관",
                'code': 'sylib',
                'address': '서울특별시 영등포구 선유로43가길 10-8 선유정보문화도서관',
                'lat': '37.533264',
                'lng': '126.892857',
            },
        ],
        "은평구": [
            {
                'name': "은평구립도서관",
                'code': 'eplib',
                'address': '서울특별시 은평구 통일로78가길 13-84',
                'lat': '37.619073',
                'lng': '126.928265',
            },
            {
                'name': "은평뉴타운도서관",
                'code': 'enlib',
                'address': '서울특별시 은평구 진관2로 111-51',
                'lat': '37.637225',
                'lng': '126.933067',
            },
            {
                'name': "은평구립증산정보도서관",
                'code': 'jsplib',
                'address': '서울특별시 영등포구 도신로 27 대림정보문화도서관',
                'lat': '37.582723',
                'lng': '126.907594',
            },
            {
                'name': "은평구립응암정보도서관",
                'code': 'ealib',
                'address': '서울특별시 은평구 가좌로7길 15',
                'lat': '37.585929',
                'lng': '126.919669',
            },
            {
                'name': "은평구립구산동도서관마을",
                'code': 'gsvlib',
                'address': '서울특별시 은평구 연서로13길 29-23',
                'lat': '37.609612',
                'lng': '126.913018',
            },
        ],
    }

    # 중랑구중앙과 동대문중앙 code겹쳐서 중랑구쪽 임으로 JMA라 코드 부여해 놓음

    for district_key, district_value in district_library_info_dict.items():

        # district 객체부터 만듬
        district, district_created_bool = District.objects.get_or_create(
            district_name = district_key
        )
        # print(district_key)

        for library_key in district_value:
            name = library_key['name']
            code = library_key['code']
            address = library_key['address']
            lat = library_key['lat']
            lng = library_key['lng']

            # print(name)
            # print(code)
            # print(address)
            # print(lat)
            # print(lng)
            # print(' ')
            # print(' ')

            library, library_created_bool = Library.objects.get_or_create(

                library_name = name,
                library_code = code,
                library_district = district,
                library_address = address,
                lat = lat,
                lng = lng
            )

