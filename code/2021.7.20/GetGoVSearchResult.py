# GetGoVSearchResult()
# 이슬 2021.07.20

import json
import urllib.request

def Get_Request_GoUrl(url):
    pass


def GetGoVSearchResult(baseUrl, pageValue, perPageValue):   
    paraData = "page=" + str(pageValue)
    paraData += "&perPage=" + str(perPageValue)
    keyValue = "&serviceKey=%2BptXuibm2mCBLhAZqH%2F88WSuHtU%2BmhKVJUWGVelVYJKc1NENMurzQaKEMPN%2Bd99LWr97LDZcj1XoIkcr6UlUjg%3D%3D"

    url = baseurl + paraData + keyValue

    resultData = Get_Request_GoUrl(url)

    if(resultData == None):
        return None
    else:
        return json.loads(resultData)
    
    
def Main():
    baseUrl = pubUrl
    baseUrl = trustUrl
    jsonSearchResult = GetGoVSearchResult(pubUrl, pageData, perPageData)
    jsonSearchResult.append() = GetGoVSearchResult(trustUrl, pageData, perPageData)

    with open('%s_GoVData_%s.json' % ('예방접종센터', '데이터'), 'w', encoding='utf-8') as filedata:
        rJson = json.dumps(jsonSearchResult,
                            indent = 4, 
                            sort_keys = True, 
                            ensure_ascii = False)
        filedata.write(rJson)

    print('파일이름 : %s_GoVData_%s.json 저장완료' % ('예방접종센터', '데이터'))

    
if __name__ == '__main__':
    Main()   
