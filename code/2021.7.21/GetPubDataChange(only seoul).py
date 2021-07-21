# 서울 의료기관 데이터만 가져오기
# 1-B조 유승현, 이슬 2021.07.21
def GetPubDataChange(resultJsonData, changeDataName):
    
 for iCount in range(0, resultJsonData['currentCount']):
     k = resultJsonData['data'][iCount]['address']  
     if  k.startswith("서울특별시")==True:
 

        hName = resultJsonData['data'][iCount]['centerName']
        hAddress = resultJsonData['data'][iCount]['address']
        hNum = resultJsonData['data'][iCount]['phoneNumber']
        hLat = resultJsonData['data'][iCount]['lat']
        hLon = resultJsonData['data'][iCount]['lng']    

        changeDataName.append({ 'hName': hName,
                            'hAddress': hAddress,
                            'hNum': hNum,
                            'hLat': hLat,
                            'hLon' : hLon })
     else: 
         None
