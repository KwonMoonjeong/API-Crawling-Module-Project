# 공공 데이터 - 공공 병원 데이터 정제
# 유승현, 이슬 / 2021.07.21

import urllib.request
import datetime
import json

def GetPubDataChange(resultJsonData, changeDataName):
    
    for iCount in range(0, resultJsonData[0]['currentCount']):
        
        hName = resultJsonData[0]['data'][iCount]['centerName']
        hAddress = resultJsonData[0]['data'][iCount]['address']
        hNum = resultJsonData[0]['data'][iCount]['phoneNumber']
        hLat = resultJsonData[0]['data'][iCount]['lat']
        hLon = resultJsonData[0]['data'][iCount]['lng']    

        changeDataName.append({ 'hName': hName,
                            'hAddress': hAddress,
                            'hNum': hNum,
                            'hLat': hLat,
                            'hLon' : hLon })

    return changeDataName
