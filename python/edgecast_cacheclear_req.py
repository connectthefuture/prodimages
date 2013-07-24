


#if token != "" && account != "" && mediaPath != "" && mediaType != "":


## Setup variables
token = "9af6d09a-1250-4766-85bd-29cebf1c984f"
account = "4936"
mediaPath = argv[1]
mediaType = "8"


purgeURL = "https://api.edgecast.com/v2/mcc/customers/" + account + "/edge/purge"

## Create send data
request_params = (
'MediaPath' = mediaPath,
'MediaType' = mediaType,
)
data = json_encode(request_params)

## Send the request to Edgecast
ch = curl_init()
curl_setopt(ch, CURLOPT_URL, purgeURL)
curl_setopt(ch, CURLOPT_PORT , 443)
curl_setopt(ch, CURLOPT_SSL_VERIFYPEER, 0)
curl_setopt(ch, CURLOPT_HEADER, 0)
curl_setopt(ch, CURLINFO_HEADER_OUT, 1)
curl_setopt(ch, CURLOPT_RETURNTRANSFER, true)
curl_setopt(ch, CURLOPT_FORBID_REUSE, 1)
curl_setopt(ch, CURLOPT_FRESH_CONNECT, 1)
curl_setopt(ch, CURLOPT_CUSTOMREQUEST, "PUT")
curl_setopt(ch, CURLOPT_POSTFIELDS,data)
curl_setopt(ch, CURLOPT_HTTPHEADER, array(
'Authorization: tok:' + token,
'Content-Type: application/json',
'Accept: application/json',
'Content-length: ' + str(len(data))
)
