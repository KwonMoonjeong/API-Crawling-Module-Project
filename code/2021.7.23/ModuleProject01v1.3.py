# 최종 ModuleProject01v1.3 (데이터 프레임 적용)
# 1조(권문정, 유승현, 이슬, 황성호) 2021.07.23

import urllib.request
import datetime
import json
import time
import folium
import pandas as pd
from folium.map import Popup
from pandas import json_normalize
from multiprocessing import Pool

clientId = "mziw9a2pu6"
clientSecret = "w54VM8kbXW2mNKX4NbSjel7dIgUOfEUrpKcwt9O9"

def Get_Request_Go_Url(url): # 크롤러를 담당하는 부분
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

def Get_Go_Search_Result(baseUrl, par, pageValue, perPageValue):   
    paraData = "?page=" + str(pageValue)
    paraData += "&perPage=" + str(perPageValue)
    keyValue = "&serviceKey=%2BptXuibm2mCBLhAZqH%2F88WSuHtU%2BmhKVJUWGVelVYJKc1NENMurzQaKEMPN%2Bd99LWr97LDZcj1XoIkcr6UlUjg%3D%3D"

    # 공공 의료 기관 
    if par == "centers":
        url = baseUrl + par + paraData + keyValue
        resultData = Get_Request_Go_Url(url)
        resultJsonData = json.loads(resultData)
        resultChangeData = Get_Pubdata_Change(resultJsonData)

    # 위탁 의료 기관
    elif par == "list":
        con = []
        # con : cond[orgZipaddr::LIKE=서울특별시]
        con.append(r"&cond%5BorgZipaddr%3A%3ALIKE%5D=%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C")
        # con : cond[orgZipaddr::LIKE=경기도]
        # con.append(r"&cond%5BorgZipaddr%3A%3ALIKE%5D=%EA%B2%BD%EA%B8%B0%EB%8F%84")
        for conData in con:
            url = baseUrl + par + paraData + conData + keyValue
            resultData = Get_Request_Go_Url(url)
            resultJsonData = json.loads(resultData)
            resultChangeData = Get_Trustdata_Change(resultJsonData)

    if resultChangeData.empty:
        return None
    else:
        return resultChangeData

# 네이버 API를 이용한 데이터 요청
def Get_Request_Naver_Url(addr):  # addr : 서울특별시  url :  https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"/query
    baseUrl = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"
    paraData = "?query=%s" % (urllib.parse.quote(addr))

    url = baseUrl + paraData
    req = urllib.request.Request(url) 
    req.add_header("X-NCP-APIGW-API-KEY-ID", clientId) 
    req.add_header("X-NCP-APIGW-API-KEY", clientSecret) 

    try:
        response = urllib.request.urlopen(req) 
        if response.getcode() == 200: # URL 요청 성공   
            return response.read().decode('utf-8')
    except Exception as ex:
        print(ex)
        print("[%s] Naver_Url 요청 실패  : %s" % datetime.datetime.now(), url)
        return None

# 네이버 API를 이용해, 주소 값으로 위도,경도 가져오기
def Get_Geo_Loaction_Data(url):
    addrList = []
    tempData = []

    resultData = Get_Request_Naver_Url(url)
    if resultData == None: 
        return "Data가 없습니다."
    else:
        tempData = json.loads(resultData) # 데이터를 정형으로 변경 

     # hLon : 경도 hLat : 위도
    if 'addresses' in tempData.keys():
        hLon = tempData['addresses'][0]['x']
        hLat = tempData['addresses'][0]['y']
    
    addrList.append(
            {'addresses' : url,
            'hLon' : hLon,
            'hLat' : hLat})
    return addrList

# 공공 의료 기관 데이터 정제
def Get_Pubdata_Change(pubData):
    resultOfData = json_normalize(pubData['data']) # "data"의 값들을 Pandas 데이터프레임으로 추출
    resultOfData = resultOfData[['centerName', 'address', 'phoneNumber', 'lat', 'lng']]    # 기관명, 주소, 전화번호 컬럼 추출
    resultOfData = resultOfData.rename(columns = {'centerName' : 'hName',      # 컬럼명 변경
                                                  'address' : 'hAddress',
                                                  'phoneNumber' : 'hNum',
                                                  'lat' : 'hLat',
                                                  'lng' : 'hLon'}, inplace = False)

    #서울특별시 데이터만 저장 
    resultOfData = resultOfData[resultOfData['hAddress'].str.contains('서울특별시')]
    resultOfData = resultOfData.reset_index(drop = True, inplace = False)
    return resultOfData

# 위탁 의료 기관 데이터 정제
def Get_Trustdata_Change(trustData):

    resultOfData = json_normalize(trustData['data'])
    resultOfData = resultOfData[['orgnm', 'orgZipaddr', 'orgTlno']] 
    resultOfData = resultOfData.rename(columns = {'orgnm' : 'hName',      # 컬럼명 변경
                                                  'orgZipaddr' : 'hAddress',
                                                  'orgTlno' : 'hNum'}, inplace = False)
    
    resultOfData.sort_values(by = ['hAddress'], axis = 0)
    print("[%s] resultOfData sorted 성공 : " % datetime.datetime.now())

    # 위도 경도 값을 가져오기 위한 multi processing 시작 
    results = Get_Locate_Multi(resultOfData['hAddress'])
  
    # 위탁 의료 기관 데이터 정제(주소, 위도, 경도)
    dataSet = Multiresult_To_Dic(results, trustData['currentCount'])
    # 위탁 의료 기관 키('hAddress') 기준으로 sorting
    trustDataFrame = pd.DataFrame(dataSet)
    resultOfData = pd.merge(resultOfData, trustDataFrame, on = 'hAddress', how = "left")

    return resultOfData

# 검색할 url의 받아오는 데이터 갯수 구하는 함수
def Check_Total_Count(baseUrl, par):
    keyValue = "&serviceKey=%2BptXuibm2mCBLhAZqH%2F88WSuHtU%2BmhKVJUWGVelVYJKc1NENMurzQaKEMPN%2Bd99LWr97LDZcj1XoIkcr6UlUjg%3D%3D"
    url = baseUrl + par + "?page=1&perPage=1" + keyValue

    resultData = Get_Request_Go_Url(url)
    resultJsonData = json.loads(resultData)

    return resultJsonData['totalCount']

# multi processing한 결과 값 데이터 정제(주소, 위도, 경도)
def Multiresult_To_Dic(results, index):
    dataSet = []
    for count in range(0, index):
        if(results[count]._success):
            dataSet.append({
                'hAddress' : results[count]._value[0]['addresses'],
                'hLat' : results[count]._value[0]['hLat'],
                'hLon' : results[count]._value[0]['hLon']
                })

    return dataSet

def Get_Locate_Multi(urllist):
    pool = Pool(16)
    results = [pool.apply_async(Get_Geo_Loaction_Data, (url, )) for url in urllist]
    pool.close()
    pool.join()
    print("[%s] pool 요청 성공 : " % datetime.datetime.now())
    return results

def Map_Marker(getChangeData, hLon, hLat, pubTotal):

    focus = folium.Map(location = [hLat, hLon], zoom_start = 15)
    folium.Marker([hLat, hLon], popup = "내 위치", icon = folium.Icon(color = 'gray')).add_to(focus)
    datalen = len(getChangeData)
    for iCount in range(0, datalen):
        if(getChangeData.iloc[iCount]['hLat'] == 0 ):
            continue
        if(iCount >= pubTotal):
            icon = folium.Icon(color = 'red')
        else:
            icon = folium.Icon(color = 'blue')
        tip = getChangeData.iloc[iCount]['hName']
        tag = "주소 : %s, 전화번호 : %s " % (getChangeData.iloc[iCount]['hAddress'], getChangeData.iloc[iCount]['hNum'])
        popup = folium.Popup(tag, max_width = 300, min_width = 200) 
        folium.Marker([getChangeData.iloc[iCount]['hLat'],
                    getChangeData.iloc[iCount]['hLon']], 
                    popup = popup, tooltip = tip, icon = icon).add_to(focus)

    focus.save(r'c:\temp\hsmap.html')

def Main():
    start_time = time.time()
    pubUrl = "https://api.odcloud.kr/api/15077586/v1/"
    pubUrl_par = "centers"
    pageData = 1
    perPageData = Check_Total_Count(pubUrl, pubUrl_par)
    goData = Get_Go_Search_Result(pubUrl, pubUrl_par, pageData, perPageData)
    goDataTotal = len(goData)

    trustUrl = "https://api.odcloud.kr/api/apnmOrg/v1/"
    trustUrl_par = "list"
    perPageData = Check_Total_Count(trustUrl, trustUrl_par)
    trustData = Get_Go_Search_Result(trustUrl, trustUrl_par, pageData, perPageData)
    getChangeData = pd.concat([goData, trustData], axis = 0)
    getChangeData = getChangeData.fillna(0)

    addr = '서울특별시 중구 필동로1길 30'
    dataSet = Get_Geo_Loaction_Data(addr)
    # Map_Marker(getChangeData, dataset[0]['hLon'], dataset[0]['hLat'], goDataTotal)

    print("-------%s seconds -------" % (time.time() - start_time))

if __name__ == '__main__':
    Main()   
