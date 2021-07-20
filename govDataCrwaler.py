import urllib.request
import datetime
import json

def Get_Request_Url(pubUrl, trustUrl): # 크롤러를 담당하는 부분
    
    pubReq = urllib.request.Request(pubUrl) #검색 URL 경로 지정  
    try:
        pubResponse = urllib.request.urlopen(pubReq) # URL을 통해 데이터 요청해서 결과 받음
        if pubResponse.getcode() == 200: # 200 코드 번호면 성공 400/500 은 문서에서 확인
            print("[%s] Url 요청 성공 : " % datetime.datetime.now())    
            return pubResponse.read().decode('utf-8')
    except Exception as ex:
        print(ex)
        print("[%s] 오류 : %s " % datetime.datetime.now(), pubUrl)
        return None
    
    trustReq = urllib.request.Request(trustUrl)
    try:
        trustResponse = urllib.request.urlopen(trustReq) # URL을 통해 데이터 요청해서 결과 받음
        if trustResponse.getcode() == 200: # 200 코드 번호면 성공 400/500 은 문서에서 확인
            print("[%s] Url 요청 성공 : " % datetime.datetime.now())    
            return trustResponse.read().decode('utf-8')
    except Exception as ex:
        print(ex)
        print("[%s] 오류 : %s " % datetime.datetime.now(), trustUrl)
        return None