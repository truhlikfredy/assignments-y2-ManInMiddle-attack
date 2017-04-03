import httplib
# conn = httplib.HTTPConnection("www.python.org")
# conn.request("GET", "/index.html")
# r1 = conn.getresponse()
# print r1.status, r1.reason


c = httplib.HTTPConnection("www.wit.ie")
c.request("GET","/")
response = c.getresponse()
print response.status, response.reason

# import requests
# 
# r = requests.get('http://www.wit.ie')
# print r.status_code