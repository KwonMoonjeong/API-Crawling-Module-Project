# 이슬 2021.07.21

import urllib.request
import datetime
import json

def GetPubDataChange(resultJsonData, changeDataName):
    
    for iCount in range(0, resultJsonData[0]['currentCount']):
        
        hName = resultJsonData[0]['data'][iCount]['centerName']
        hAddress = resultJsonData[0]['data'][iCount]['address']
        hNum = resultJsonData[0]['data'][iCount]['phoneNumber']
        hLat = resultJsonData[0]['data'][iCount]['lat']     # 위도
        hLon = resultJsonData[0]['data'][iCount]['lng']    # 경도

        changeDataName.append({ 'hName': hName,
                            'hAddress': hAddress,
                            'hNum': hNum,
                            'hLat': hLat,
                            'hLon' : hLon })

    return changeDataName
