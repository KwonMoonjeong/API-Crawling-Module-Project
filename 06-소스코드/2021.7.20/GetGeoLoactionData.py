# 주소 값으로 위도 경도 값 구하기
# 황성호 2021.07.20 

import urllib.request
import json

def Get_Request_NaverUrl(url):
    pass

# 주소 입력 후 해당 주소의 위도, 경도 값 리턴
def GetGeoLoactionData(addr):
    baseUrl = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"
    paraData = "?query=%s" % urllib.parse.quote(addr)
    resultUrl = baseUrl + paraData

    resultData = Get_Request_NaverUrl(resultUrl)

    tempData = []

    if(resultData == None): # 결과가 있는지 없는지 확인
        return "Data가 없습니다."
    else:
        tempData = json.loads(resultData) # 데이터를 정형으로 변경함 
    
    # xdata : 경도 ydata : 위도
    if 'addresses' in tempData.keys():
        xdata = tempData['addresses'][0]['x']
        ydata = tempData['addresses'][0]['y']

    return xdata,ydata


def Main():
    addr = ""
    xdata,ydata = GetGeoLoactionData(addr)
    
   
if __name__ == '__main__':
    Main()
