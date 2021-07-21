# 공공 데이터 - 위탁의료기관 데이터 정제
# 권문정, 황성호 / 2021.07.21

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
    
    return changeDataName
