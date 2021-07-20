# GetGoVSearchResult() // 공공병원, 위탁의료기관 데이터 받아오기
# 이슬 2021.07.20

import json
import urllib.request
import datetime

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


def GetGoVSearchResult(baseUrl, pageValue, perPageValue, jsonSearchResult):   
    paraData = "?page=" + str(pageValue)
    paraData += "&perPage=" + str(perPageValue)
    keyValue = "&serviceKey=%2BptXuibm2mCBLhAZqH%2F88WSuHtU%2BmhKVJUWGVelVYJKc1NENMurzQaKEMPN%2Bd99LWr97LDZcj1XoIkcr6UlUjg%3D%3D"

    url = baseUrl + paraData + keyValue

    resultData = Get_Request_GoUrl(url)

    if(resultData == None):
        return None
    else:
        #return json.loads(resultData)
        jsonSearchResult.append(json.loads(resultData))
    
    
def Main():
    pubUrl = "https://api.odcloud.kr/api/apnmOrg/v1/list?"
    trustUrl = "https://api.odcloud.kr/api/15077586/v1/centers?"
    pageData = 1
    perPageData = 10
    jsonSearchResult = []
    GetGoVSearchResult(pubUrl, pageData, perPageData,jsonSearchResult)
    GetGoVSearchResult(trustUrl, pageData, perPageData,jsonSearchResult)
    #jsonSearchResult.append() = GetGoVSearchResult(trustUrl, pageData, perPageData)

    with open('%s_GoVData_%s.json' % ('예방접종센터', '데이터'), 'w', encoding='utf-8') as filedata:
        rJson = json.dumps(jsonSearchResult,
                            indent = 4, 
                            sort_keys = True, 
                            ensure_ascii = False)
        filedata.write(rJson)

    print('파일이름 : %s_GoVData_%s.json 저장완료' % ('예방접종센터', '데이터'))

    
if __name__ == '__main__':
    Main()   
