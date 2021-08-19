# 공공 데이터 크롤링해서 가져오기
# 권문정 2021.07.20


import urllib.request
import datetime
import json

def Get_Request_GoUrl(url): # 크롤러를 담당하는 부분
    req = urllib.request.Request(url) #검색 URL 경로 지정    
    # https://api.odcloud.kr/api/15077586/v1/centers?page=1&perPage=10    
    # &serviceKey=spm%2FxLr97h3BZnQQDuIKw4ESJIOX%2F7z%2F8eCDjDXmcSsOQuws8vDlflhHCtm0fXLeptDUkt39rPoI945V%2FCbEPw%3D%3D
    try:
        response = urllib.request.urlopen(req) # URL을 통해 데이터 요청해서 결과 받음
        if response.getcode() == 200: # 200 코드 번호면 성공 400/500 은 문서에서 확인
            print("[%s] Url 요청 성공 : " % datetime.datetime.now())    
            return response.read().decode('utf-8')
    except Exception as ex:
        print(ex)
        print("[%s] 오류 : %s " % datetime.datetime.now(), url)
        return None
