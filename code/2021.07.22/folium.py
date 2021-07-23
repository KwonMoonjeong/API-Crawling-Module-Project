
    addrData = [37.567817,127.004501] # base_map에 넣어줄 위도 경도
    base_map = folium.Map(location=addrData, zoom_start=15) #basemap 설정
    for i in range(len(changeDataName)):
        #print(changeDataName[i]["hAddress"])
        addrData = GetGeoLoactionData(changeDataName[i]["hAddress"]) # 주소값으로 위도 경도를 구함
    #  # 구글 지도
        tip = changeDataName[i]['hName']
        map_data = folium.Marker(addrData, popup=(changeDataName[i]["hAddress"] ,changeDataName[i]['hNum'])
        ,tooltip=tip).add_to(base_map) #basemap에 marker표시
        
    map_data.save(r'c:\temp\navermapii.html')
        
