# 테스트용 (pandas 적용 후)
# 2021.07.22 황성호

from operator import iconcat
import urllib.request
import datetime
import json
import time
import folium
from folium.map import Popup
import pandas as pd
from pandas import json_normalize
from _operator import itemgetter
from multiprocessing import Pool

client_id = "xa25ja6nca"
client_secret = "1a3NIZFJLWWpgOnc1tgDJMFYTTKQLzVsXTH7T4X2"


def Get_Request_GoUrl(url): # 크롤러를 담당하는 부분
    req = urllib.request.Request(url) #검색 URL 경로 지정    

    try:
        response = urllib.request.urlopen(req) # URL을 통해 데이터 요청해서 결과 받음
        if response.getcode() == 200: # URL 요청 성공
            print("[%s] Go_Url 요청 성공 : " % datetime.datetime.now())    
            return response.read().decode('utf-8')
    except Exception as ex:
        print(ex)
        print("[%s] Go_Url 요청 실패 : %s " % datetime.datetime.now(), url)
        return None


def GetGoVSearchResult(baseUrl,par, pageValue, perPageValue):   
    paraData = "?page=" + str(pageValue)
    paraData += "&perPage=" + str(perPageValue)
    keyValue = "&serviceKey=%2BptXuibm2mCBLhAZqH%2F88WSuHtU%2BmhKVJUWGVelVYJKc1NENMurzQaKEMPN%2Bd99LWr97LDZcj1XoIkcr6UlUjg%3D%3D"

    # 공공 의료 기관 
    if (par == "centers"):
        url = baseUrl+par + paraData + keyValue
        resultData = Get_Request_GoUrl(url)
        resultJsonData = json.loads(resultData)
        changeDataName = GetPubDataChange(resultJsonData)

    # 위탁 의료 기관
    elif (par == "list"):
        con = []
        # con : cond[orgZipaddr::LIKE=서울특별시]
        con.append(r"&cond%5BorgZipaddr%3A%3ALIKE%5D=%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C")
        # con : cond[orgZipaddr::LIKE=경기도]
        # con.append(r"&cond%5BorgZipaddr%3A%3ALIKE%5D=%EA%B2%BD%EA%B8%B0%EB%8F%84")
        for conData in con:
            url = baseUrl+par + paraData + conData + keyValue
            resultData = Get_Request_GoUrl(url)
            resultJsonData = json.loads(resultData)

            changeDataName = GetTrustDataChange(resultJsonData)

    if changeDataName.empty:
        return None
    else:
        return changeDataName

# 네이버 API를 이용한 데이터 요청
def Get_Request_NaverUrl(addr):  # addr : 서울특별시  url :  https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"/query
    baseUrl = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"
    paraData = "?query=%s" % (urllib.parse.quote(addr))

    url = baseUrl + paraData

    req = urllib.request.Request(url) 
    req.add_header("X-NCP-APIGW-API-KEY-ID", client_id) 
    req.add_header("X-NCP-APIGW-API-KEY", client_secret) 

    try:
        response = urllib.request.urlopen(req) 
        if response.getcode() == 200: # URL 요청 성공   
            return response.read().decode('utf-8')
    except Exception as ex:
        print(ex)
        print("[%s] Naver_Url 요청 실패  : %s " % datetime.datetime.now(), url)
        return None
# 네이버 API를 이용해, 주소 값으로 위도,경도 가져오기
def GetGeoLoactionData(url):
    addrlist = []
    
    resultData = Get_Request_NaverUrl(url)

    tempData = []

    if(resultData == None): 
        return "Data가 없습니다."
    else:
        tempData = json.loads(resultData) # 데이터를 정형으로 변경 

     # xdata : 경도 ydata : 위도
    if 'addresses' in tempData.keys():
        xdata = tempData['addresses'][0]['x']
        ydata = tempData['addresses'][0]['y']
    
    addrlist.append(
            {'addresses':url,
            'xdata' : tempData['addresses'][0]['x'],
            'ydata' : tempData['addresses'][0]['y']
    })

    return addrlist

# 공공 의료 기관 데이터 정제
def GetPubDataChange(pubData):
    dataOfResult = json_normalize(pubData['data']) # "data"의 값들을 Pandas 데이터프레임으로 추출
    dataOfResult = dataOfResult[['centerName', 'address', 'phoneNumber', 'lat', 'lng']]    # 기관명, 주소, 전화번호 컬럼 추출
    dataOfResult = dataOfResult.rename(columns={'centerName' : 'hName',      # 컬럼명 변경
                                                'address' : 'hAddress',
                                                 'phoneNumber' : 'hNum',
                                                 'lat' : 'hLat',
                                                 'lng' : 'hLon'}, inplace=False)
    return dataOfResult

'''
# 공공 의료 기관 데이터 정제
def GetPubDataChange(resultJsonData,changeDataName):

    df = pd.DataFrame(resultJsonData['data'])

    for iCount in range(0, resultJsonData['currentCount']):
        hAddress = resultJsonData['data'][iCount]['address']
        if(hAddress.startswith("서울특별시")==True): #or (hAddress.startswith("경기도")==True)):
            hName = resultJsonData['data'][iCount]['centerName']
            hNum = resultJsonData['data'][iCount]['phoneNumber']
            hLat = resultJsonData['data'][iCount]['lat']     # 위도
            hLon = resultJsonData['data'][iCount]['lng']    # 경도

            changeDataName.append({'hName': hName,
                                'hAddress': hAddress,
                                'hNum': hNum,
                                'hLat': hLat,
                                'hLon' : hLon })
'''
# 위탁 의료 기관 데이터 정제
def GetTrustDataChange(trustData):

    dataOfResult = json_normalize(trustData['data'])
    dataOfResult = dataOfResult[['orgnm', 'orgZipaddr', 'orgTlno']] 
    dataOfResult = dataOfResult.rename(columns={'orgnm' : 'hName',      # 컬럼명 변경
                                                'orgZipaddr' : 'hAddress',
                                                 'orgTlno' : 'hNum'}, inplace=False)
    
    dataOfResult.sort_values(by=['hAddress'],axis=0)
    
    print("[%s] dataOfResult sorted 성공 : " % datetime.datetime.now())
    addrs = []
    dataset = []
    #for iCount in range(0,trustData['currentCount']):
    #    addrs.append(trustData['data'][iCount]['orgZipaddr'])
    
    # multi processing을 위한 urllist 모음

    urllist = []
    #for count in range(0,trustData['currentCount']):
    #    baseUrl = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"
    #    paraData = "?query=%s" % urllib.parse.quote(dataOfResult['hAddress'][count])
        

    # 위도 경도 값을 가져오기 위한 multi processing 시작 
    results = Get_Locate_Multi(dataOfResult['hAddress'])
  
    # 위탁 의료 기관 데이터 정제(기관명, 주소, 전화번호)
    # trustDataset = TrustDataToDic(trustData)
    # 위탁 의료 기관 키('hAddress') 기준으로 sorting
    # sorttrustDataset = sorted(trustDataset,key=lambda k:k['hAddress'])
    
    
    # errorlist : 위탁 의료 기관 주소 데이터의 오류를 담음
    errorlist = []
    # 위탁 의료 기관 데이터 정제(주소, 위도, 경도)
    dataSet,errorlist = MultiResultToDic(results,trustData['currentCount'])
    # 위탁 의료 기관 키('hAddress') 기준으로 sorting
    trustDataFrame = pd.DataFrame(dataSet)
    dataOfResult = pd.merge(dataOfResult,trustDataFrame, on='hAddress',how="left")

    #print(dataOfResult)
    #jCount = 0
    #errorCountIndex = 0
    # 위탁 의료 기관 데이터 정제(기관명, 주소, 전화번호, 위도, 경도)
    #for iCount in range(0,trustData['currentCount']):
        
    #    if(not errorlist or (iCount != errorlist[errorCountIndex])):
    #        changeDataName.append({
    #        'hName':sorttrustDataset[iCount]['hName'],
    #        'hAddress':sorttrustDataset[iCount]['hAddress'],
    #        'hNum':sorttrustDataset[iCount]['hNum'],
    #        'hLat':sortDataSet[jCount]['hLat'],
    #        'hLon':sortDataSet[jCount]['hLon']
    #        })
    #    else: # 주소 오류 처리
    #        jCount = jCount - 1
    #        if(errorCountIndex != (errorlist.__len__()-1)):
    #            errorCountIndex = errorCountIndex + 1
    #    jCount = jCount + 1
    return dataOfResult
        
# 검색할 url의 받아오는 데이터 갯수 구하는 함수
def CheckTotalCount(baseUrl,par):
    keyValue = "&serviceKey=%2BptXuibm2mCBLhAZqH%2F88WSuHtU%2BmhKVJUWGVelVYJKc1NENMurzQaKEMPN%2Bd99LWr97LDZcj1XoIkcr6UlUjg%3D%3D"
    url = baseUrl + par + "?page=1&perPage=1"+keyValue

    resultData = Get_Request_GoUrl(url)
    resultJsonData = json.loads(resultData)

    return resultJsonData['totalCount']

# 위탁 의료 기관 데이터 정제(기관명, 주소, 전화번호)
def TrustDataToDic(trustData):

    dataOfResult = json_normalize(trustData['data'])
    dataOfResult = dataOfResult[['orgnm', 'orgZipaddr', 'orgTlno']] 
    dataOfResult = dataOfResult.rename(columns={   # 컬럼명 변경
                                                'orgZipaddr' : 'hAddress',
                                                 'ydata' : 'hLat',
                                                 'xdata' : 'hLon',}, inplace=False)
    trustDataSet = []
    for iCount in range(0,trustData['currentCount']):
        hName = trustData['data'][iCount]['orgnm']
        hAddress = trustData['data'][iCount]['orgZipaddr']
        hNum = trustData['data'][iCount]['orgTlno']
        trustDataSet.append({
        'hName':hName,
        'hAddress':hAddress,
        'hNum':hNum,
        })
    return trustDataSet

# multi processing한 결과 값 데이터 정제(주소, 위도, 경도)
def MultiResultToDic(results,index):
    dataset = []
    errorlist = []
    for count in range(0,index):
        if(results[count]._success):
            dataset.append({
                'hAddress':results[count]._value[0]['addresses'],
                'hLat':results[count]._value[0]['ydata'],
                'hLon':results[count]._value[0]['xdata']
                })
        else:
            errorlist.append(count)

    return dataset,errorlist

def Get_Locate_Multi(urllist):
    pool = Pool(8)
    results = [pool.apply_async(GetGeoLoactionData,(url,))for url in urllist]
    pool.close()
    pool.join()
    print("[%s] pool 요청 성공 : " % datetime.datetime.now())
    return results

def Map_Marker(jsonSearchResult,xdata,ydata):

    focus = folium.Map(location=[ydata,xdata], zoom_start=15)
    folium.Marker([ydata,xdata],popup="내 위치",icon=folium.Icon(color='gray')).add_to(focus)
    jsonlen = len(jsonSearchResult)
    for iCount in range(0,jsonlen-1):
        tip = jsonSearchResult[iCount]['hName']
        tag = "주소 : %s , 전화번호 : %s " %(jsonSearchResult[iCount]['hAddress'],jsonSearchResult[iCount]['hNum'])
        popup = folium.Popup(tag, max_width=300,min_width=200) 
        folium.Marker([jsonSearchResult[iCount]['hLat'],
                    jsonSearchResult[iCount]['hLon']], 
                    popup=popup, tooltip=tip).add_to(focus)

    jsonNext = jsonSearchResult[jsonlen-1]
    for iCount in range(0,len(jsonNext)):
        tip = jsonNext[iCount]['hName']
        tag = "주소 : %s , 전화번호 : %s " %(jsonNext[iCount]['hAddress'],jsonNext[iCount]['hNum'])
        popup = folium.Popup(tag, max_width=300,min_width=300)
        icon = folium.Icon(color='red')
        folium.Marker([jsonNext[iCount]['hLat'],
                    jsonNext[iCount]['hLon']], 
                    popup=popup, tooltip=tip,icon=icon).add_to(focus)
    focus.save(r'c:\temp\hsmap.html')

def Main():
    start_time = time.time()
    pubUrl = "https://api.odcloud.kr/api/15077586/v1/"
    pubUrl_par = "centers"
    pageData = 1
    perPageData = CheckTotalCount(pubUrl,pubUrl_par)
    
    
    goData= GetGoVSearchResult(pubUrl, pubUrl_par,pageData, perPageData)

    trustUrl = "https://api.odcloud.kr/api/apnmOrg/v1/"
    trustUrl_par = "list"
    perPageData = CheckTotalCount(trustUrl,trustUrl_par)
    # perPageData = 10
    trustData = GetGoVSearchResult(trustUrl,trustUrl_par ,pageData, perPageData)
    jsonSearchResult = pd.concat([goData,trustData],axis=0)
    # print(jsonSearchResult)
    
    #baseUrl = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"
    #paraData = "?query=%s" % urllib.parse.quote('서울특별시 중구 필동로1길 30')
    #url = baseUrl + paraData
    addr = '서울특별시 중구 필동로1길 30'
    dataset = GetGeoLoactionData(addr)

    # Map_Marker(jsonSearchResult,dataset[0]['xdata'],dataset[0]['ydata'])

    print("-------%s seconds -------" % (time.time() - start_time))
    

    
    temp = 0 

if __name__ == '__main__':
    Main()   
