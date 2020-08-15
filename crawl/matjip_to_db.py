import requests
import pprint
import time
from pymongo import MongoClient

# 맛집 데이터는 seoul_matjip 이라는 데이터베이스에 저장하겠습니다.
client = MongoClient('localhost', 27017)
db = client.seoul_matjip

# 서울시 구마다 맛집을 검색해보겠습니다.
seoul_gu = ["종로구", "중구", "용산구", "성동구", "광진구", "동대문구", "중랑구", "성북구", "강북구", "도봉구", "노원구", "은평구", "서대문구", "마포구", "양천구", "강서구", "구로구", "금천구", "영등포구", "동작구", "관악구", "서초구", "강남구", "송파구", "강동구"]

# 네이버 검색 API 신청을 통해 발급받은 아이디와 시크릿 키를 입력합니다.
client_id = "IJzTWoJvCckCa0e3JZOj"
client_secret = "L7tMIUCzFQ"

# 검색어를 전달하면 결과를 반환하는 함수
def get_naver_result(keyword):
    time.sleep(0.1)
    # url에 전달받은 검색어를 삽입합니다.
    api_url = f"https://openapi.naver.com/v1/search/local.json?query={keyword}&display=10&start=1&sort=random"
    # 아이디와 시크릿 키를 부가 정보로 같이 보냅니다.
    headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret}
    # 검색 결과를 data에 저장합니다.
    data = requests.get(api_url, headers=headers)
    # 받아온 JSON 결과를 딕셔너리로 변환합니다.
    data = data.json()
    return data['items']

# 저장할 전체 맛집 목록
docs = []
# 구별로 검색을 실행합니다.
for gu in seoul_gu:
    # '강남구 맛집', '종로구맛집' ...반복 인코딩
    keyword = f'{gu} 맛집'
    # 맛집 리스트를 받아온다.
    matjip_list = get_naver_result(keyword)

    # 구 별 맛집 구분선
    print("*"*80 + gu)

    for matjip in matjip_list:
        matjip['gu'] = gu
        # 맛집 인쇄
        pprint.pprint(matjip)
        # docs에 맛집을 추가합니다.
        docs.append(matjip)

# 맛집 정보 저장
db.matjip.insert_many(docs)