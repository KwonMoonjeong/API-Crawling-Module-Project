def GetPubDataChange(jsonSearchResult,changeDataName): 
    ii=0
    for  ii in range(jsonSearchResult[0]['currentCount']):
        hAddress = jsonSearchResult[0]['data'][ii]['address']
        hName =jsonSearchResult[0]['data'][ii]['centerName']
        hNum = jsonSearchResult[0]['data'][ii]['phoneNumber']
        hLat = jsonSearchResult[0]['data'][ii]["lat"]
        hLon =jsonSearchResult[0]['data'][ii]["lng"]
       
        changeDataName.append({" hAddress" : hAddress, 
                                "hName" : hName,
                                "hNum" : hNum,
                                "hLat" : hLat,
                                "hLon" : hLon})
        

    return changeDataName
