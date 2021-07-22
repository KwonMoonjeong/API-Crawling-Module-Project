import urllib.request
import datetime
import json
import pandas as pd
from pandas import json_normalize
import numpy as np


def GetTrustDataChangePandas(resultJsonData, changeDataName):

    dataOfResult = json_normalize(resultJsonData['data']) # "data"의 값들을 Pandas 데이터프레임으로 추출
    dataOfResult = dataOfResult[['orgnm', 'orgZipaddr', 'orgTlno']]    # 기관명, 주소, 전화번호 컬럼 추출
    dataOfResult = dataOfResult.rename(columns={'orgnm' : 'hName',      # 컬럼명 변경
                                                'orgZipaddr' : 'hAddress',
                                                 'orgTlno' : 'hNum'}, inplace=False)

    dataOfResult['hLon'], dataOfResult['hLat'] = zip(*dataOfResult['hAddress'].apply(GetGeoLocationData))
    # 좌표 구해서 2개의 컬럼에 넣어주기
