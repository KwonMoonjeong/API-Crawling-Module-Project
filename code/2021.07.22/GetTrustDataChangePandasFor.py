# 위탁의료기관 데이터 정제 (Pandas와 for문 동시 사용, 멀티 프로세스 사용 전)
# 1조(권문정) 2021.07.22

import urllib.request
import datetime
import json
import pandas as pd
from pandas import json_normalize
import numpy as np

def GetTrustDataChangePandasFor(resultJsonData, changeDataName):

    dataOfResult = json_normalize(resultJsonData['data']) # "data"의 값들을 Pandas 데이터프레임으로 추출
    dataOfResult = dataOfResult[['orgnm', 'orgZipaddr', 'orgTlno']]    # 기관명, 주소, 전화번호 컬럼 추출
    dataOfResult = dataOfResult.rename(columns={'orgnm' : 'hName',      # 컬럼명 변경
                                                'orgZipaddr' : 'hAddress',
                                                 'orgTlno' : 'hNum'}, inplace=False)

    dataOfResult['hLon'] = np      # 경도와 위도를 넣어줄 빈 컬럼 2개 생성
    dataOfResult['hLat'] = np

    for iCount in range(0, resultJsonData['currentCount']):     # 좌표 가져오기
        hLon, hLat = GetGeoLocationData(resultJsonData['data'][iCount]['orgZipaddr'])

        dataOfResult.loc[iCount,'hLon'] = hLon      # 경도와 위도 컬럼에 좌표 채우기
        dataOfResult.loc[iCount,'hLat'] = hLat
