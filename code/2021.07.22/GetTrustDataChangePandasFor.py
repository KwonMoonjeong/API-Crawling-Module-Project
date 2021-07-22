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
