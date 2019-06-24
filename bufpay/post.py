import http.client, urllib

httpClient = None
try:
    params = urllib.parse.urlencode({'name': 'Maximus', 'addr': "GZ"})
    headers = {"Content-type": "application/x-www-form-urlencoded"
                    , "Accept": "text/plain"}

    httpClient = http.client.HTTPConnection("localhost", 8080, timeout=30)
    httpClient.request("POST", "/test0.html", params, headers)

    response = httpClient.getresponse()
    print (response.status)
    print (response.reason)
    print (response.read())
    print (response.getheaders()) #获取头信息
except Exception as e:
    print (e)
finally:
    if httpClient:
        httpClient.close()
# ---------------------
# 作者：maximuszhou
# 来源：CSDN
# 原文：https://blog.csdn.net/MaximusZhou/article/details/39557483
# 版权声明：本文为博主原创文章，转载请附上博文链接！
