from ..models.locations import *

def get_info():

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
    }

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

