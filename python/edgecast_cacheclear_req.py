import pycurl


#if token != "" && account != "" && mediaPath != "" && mediaType != "":


## Setup variables
token = "9af6d09a-1250-4766-85bd-29cebf1c984f"
account = "4936"
mediaPath = sys.argv[1]
mediaType = "8"


purgeURL = "https://api.edgecast.com/v2/mcc/customers/{0}/edge/purge".format(account)

## Create send data
request_params = (
'MediaPath' = mediaPath,
'MediaType' = mediaType
)
data = json_encode(request_params)
head_authtoken = "Authorization: tok:{0}".format(token)
head_content_len= "Content-length: {0})".format(str(len(data)))
head_accept = 'Accept: application/json'
head_contenttype = 'Content-Type: application/json'

## Send the request to Edgecast
c = pycurl.Curl()
c.setopt(c.URL, purgeURL)
c.setopt(c.PORT , 443)
c.setopt(c.SSL_VERIFYPEER, 0)
c.setopt(c.HEADER, 0)
curl_setopt(ch, CURLINFO_HEADER_OUT, 1)
c.setopt(c.RETURNTRANSFER, true)
c.setopt(c.FORBID_REUSE, 1)
c.setopt(c.FRESH_CONNECT, 1)
c.setopt(c.CUSTOMREQUEST, "PUT")
c.setopt(c.POSTFIELDS,data)
c.setopt(c.HTTPHEADER, [
head_authtoken,
head_contenttype,
head_accept,
head_content_len
])
try:
    c.perform()

except pycurl.error, error:
    errno, errstr = error
    print 'An error occurred: ', errstr




c = pycurl.Curl()
c.setopt(c.URL, 'http://myappserver.com/ses1')
c.setopt(c.CONNECTTIMEOUT, 5)
c.setopt(c.TIMEOUT, 8)
c.setopt(c.COOKIEFILE, '')
c.setopt(c.FAILONERROR, True)
c.setopt(c.HTTPHEADER, ['Accept: text/html', 'Accept-Charset: UTF-8'])
try:
    c.perform()

    c.setopt(c.URL, 'http://myappserver.com/ses2')
    c.setopt(c.POSTFIELDS, 'foo=bar&bar=foo')
    c.perform()







