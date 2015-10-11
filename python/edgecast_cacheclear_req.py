import pycurl,json,sys,os

## Setup variables
token = "9af6d09a-1250-4766-85bd-29cebf1c984f"
account = "4936"
mediaPath = sys.argv[1]
#mediaPath = 'http://cdn.is.belleandclive.com/mgen/Bluefly/prodImage.ms?productCode=324860301&width=320&height=430&ver=3'
mediaType = "8"

purgeURL = "https://api.edgecast.com/v2/mcc/customers/{0}/edge/purge".format(account)

if token != "" and account != "" and mediaPath != "" and mediaType != "":
    ## Create send data
    data = json.dumps({
    'MediaPath' : mediaPath,
    'MediaType' : mediaType 
    })

    #data = json_encode(request_params)
    head_authtoken = "Authorization: tok:{0}".format(token)
    head_content_len= "Content-length: {0}".format(str(len(data)))
    head_accept = 'Accept: application/json'
    head_contenttype = 'Content-Type: application/json'
    #print head_content_len
    ## Send the request to Edgecast
    ### Send the request to Edgecast
    c = pycurl.Curl()
    c.setopt(pycurl.URL, purgeURL)
    c.setopt(pycurl.PORT , 443)
    c.setopt(pycurl.SSL_VERIFYPEER, 0)
    c.setopt(pycurl.HEADER, 0)
    #c.setopt(pycurl.INFOTYPE_HEADER_OUT, 1)
    #c.setopt(pycurl.RETURNTRANSFER, 1)
    c.setopt(pycurl.FORBID_REUSE, 1)
    c.setopt(pycurl.FRESH_CONNECT, 1)
    c.setopt(pycurl.CUSTOMREQUEST, "PUT")
    c.setopt(pycurl.POSTFIELDS,data)
    c.setopt(pycurl.HTTPHEADER, [head_authtoken, head_contenttype, head_accept, head_content_len])
    try:
        c.perform()
        c.close()
        print "Successfully Sent Purge Request for --> {0}".format(mediaPath)
    except pycurl.error, error:
        errno, errstr = error
        print 'An error occurred: ', errstr
