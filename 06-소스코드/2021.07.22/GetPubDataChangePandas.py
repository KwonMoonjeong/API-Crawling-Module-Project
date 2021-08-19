# 공공병원 데이터정제(DataFrame 활용)
# 1조(이슬) 2021.07.22

import json
import pandas as pd


def GetPubDataChange(pubData):
    dataResult = json_normalize(pubData['data']) # "data"의 값들을 Pandas 데이터프레임으로 추출
    dataResult = dataResult[['centerName', 'address', 'phoneNumber', 'lat', 'lng']]    # 기관명, 주소, 전화번호 컬럼 추출
    dataResult = dataResult.rename(columns={'centerName' : 'hName',      # 컬럼명 변경
                                                'address' : 'hAddress',
                                                'phoneNumber' : 'hNum',
                                                'lat' : 'hLat',
                                                'lng' : 'hLon'}, inplace=False)
