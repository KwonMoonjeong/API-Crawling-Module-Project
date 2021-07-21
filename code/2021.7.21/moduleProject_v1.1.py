# 데이터 정제 V0.1
# 1조(권문정, 유승현, 이슬, 황성호) 2021.07.20

import urllib.request
import datetime
import json


client_id = "xa25ja6nca"
client_secret = "1a3NIZFJLWWpgOnc1tgDJMFYTTKQLzVsXTH7T4X2"


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

    
def GetGoVSearchResult(baseUrl, par, pageValue, perPageValue):   
    paraData = "?page=" + str(pageValue)
    paraData += "&perPage=" + str(perPageValue)
    keyValue = "&serviceKey=%2BptXuibm2mCBLhAZqH%2F88WSuHtU%2BmhKVJUWGVelVYJKc1NENMurzQaKEMPN%2Bd99LWr97LDZcj1XoIkcr6UlUjg%3D%3D"

    url = baseUrl+par + paraData + keyValue

    resultData = Get_Request_GoUrl(url)
    resultJsonData = json.loads(resultData)

    changeDataName = []

    if (par == "list"):
        GetTrustDataChange(resultJsonData, changeDataName)
    
    elif (par == "centers"):
        GetPubDataChange(resultJsonData, changeDataName)

    if(resultData == None):
        return None
    
    else:
        return changeDataName


def Get_Request_NaverUrl(url): # 데이터 요청하여 가져오기 - 크럴러 작업
    req = urllib.request.Request(url) # 검색 URL 경로 지정
    req.add_header("X-NCP-APIGW-API-KEY-ID", client_id) # 경로 접근하기 위한 아이디 - naver에서 발급
    req.add_header("X-NCP-APIGW-API-KEY", client_secret) # 경로 접근하기 위한 비밀번호 - naver에서 발급

    try:
        response = urllib.request.urlopen(req) # URL을 통해 데이터 요청해서 결과 받음
        if response.getcode() == 200: # 200 코드 번호면 성공 400/500 은 Naver 문서에서 확인
            #print("[%s] Url 요청 성공 : " % datetime.datetime.now())    
            return response.read().decode('utf-8')
    except Exception as ex:
        print(ex)
        print("[%s] 오류 : %s " % datetime.datetime.now(), url)
        return None
    
def GetGeoLoactionData(addr):
    baseUrl = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"
    paraData = "?query=%s" % urllib.parse.quote(addr)
    resultUrl = baseUrl + paraData

    resultData = Get_Request_NaverUrl(resultUrl)

    tempData = []

    if(resultData == None): # 결과가 있는지 없는지 확인
        return "Data가 없습니다."
    else:
        tempData = json.loads(resultData) # 데이터를 정형으로 변경함 
    
    # xdata : 경도 ydata : 위도
    if 'addresses' in tempData.keys():
        xdata = tempData['addresses'][0]['x']
        ydata = tempData['addresses'][0]['y']

    return xdata, ydata


def GetPubDataChange(resultJsonData, changeDataName):
    
    for iCount in range(0, resultJsonData['currentCount']):
        
        hName = resultJsonData['data'][iCount]['centerName']
        hAddress = resultJsonData['data'][iCount]['address']
        hNum = resultJsonData['data'][iCount]['phoneNumber']
        hLat = resultJsonData['data'][iCount]['lat']
        hLon = resultJsonData['data'][iCount]['lng']    

        changeDataName.append({ 'hName': hName,
                            'hAddress': hAddress,
                            'hNum': hNum,
                            'hLat': hLat,
                            'hLon' : hLon })


def GetTrustDataChange(resultJsonData, changeDataName):
    
    for iCount in range(0, resultJsonData['currentCount']):
        
        hName = resultJsonData['data'][iCount]['orgnm']
        hAddress = resultJsonData['data'][iCount]['orgZipaddr']
        hNum = resultJsonData['data'][iCount]['orgTlno']
        hLon, hLat = GetGeoLoactionData(hAddress)
        
        changeDataName.append({ 'hName': hName,
                            'hAddress': hAddress,
                            'hNum': hNum,
                            'hLat': hLat,
                            'hLon' : hLon })
    

def Main():
    pubUrl = "https://api.odcloud.kr/api/15077586/v1/"
    pubUrl_par = "centers"
    trustUrl = "https://api.odcloud.kr/api/apnmOrg/v1/"
    trusetUrl_par = "list"
    pageData = 1
    perPageData = 10
    
    changeDataName = GetGoVSearchResult(pubUrl, pubUrl_par, pageData, perPageData)
    changeDataName += GetGoVSearchResult(trustUrl, trusetUrl_par, pageData, perPageData)

    with open('%s_GoVData_%s.json' % ('예방접종센터', '데이터'), 'w', encoding='utf-8') as filedata:
        rJson = json.dumps(changeDataName,
                            indent = 4, 
                            sort_keys = True, 
                            ensure_ascii = False)
        filedata.write(rJson)

    print('파일이름 : %s_GoVData_%s.json 저장완료' % ('예방접종센터', '데이터'))
    

if __name__ == '__main__':
    Main()   
