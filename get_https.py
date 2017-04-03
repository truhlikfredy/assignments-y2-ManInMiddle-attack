#!/usr/bin/env python

import httplib
c = httplib.HTTPSConnection("moodle.wit.ie")
c.request("GET", "/login/index.php")
response = c.getresponse()
print response.status, response.reason
data = response.read()
print data
