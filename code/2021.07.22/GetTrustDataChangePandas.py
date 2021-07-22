import urllib.request
import datetime
import json
from pandas import json_normalize

def GetTrustDataChange(resultJsonData, changeDataName):

    dataOfResult = json_normalize(resultJsonData['data']) # "data"의 값들을 Pandas 데이터프레임으로 추출
    dataOfResult = dataOfResult[['orgnm', 'orgZipaddr', 'orgTlno']]    # 기관명, 주소, 전화번호 컬럼 추출
    dataOfResult = dataOfResult.rename(columns={'orgnm' : 'hName',      # 컬럼명 변경
                                                'orgZipaddr' : 'hAddress',
                                                 'orgTlno' : 'hNum'}, inplace=False)

    dataOfResult['hLon', 'hLat'] = dataOfResult['hAddress'].apply(GetGeoLocationData)
