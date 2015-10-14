#!/usr/bin/env python
# coding: utf-8

__base_protocol__               = "https"
__base_url__                    = "staging-sb.mozu.com"
__listFQN__                     = 'files@mozu'
__documentTypeFQN__             = 'image@mozu'
__tenant_name__                 = '11146'
__tenant_url__                  = "{0}://t{1}.{2}".format(__base_protocol__, __tenant_name__,__base_url__ )
### build Mozu API Url String
__document_data_api__   = __tenant_url__ + "/api/content/documentlists/" + __listFQN__ + "/documents"


def get_mozu_client_authtoken():
    #  "http://requestb.in/q66719q6" #
    import os.path as path
    import requests, json
    _auth_url = "https://home.staging.mozu.com/api/platform/applications/authtickets"
    _auth_headers = {'Content-type': 'application/json', 'Accept-Encoding': 'gzip, deflate'}
    _auth_request = {'applicationId' : 'bluefly.product_images.1.0.0.release', 'sharedSecret' : '53de2fb67cb04a95af323693caa48ddb'}
    _auth_response = requests.post(_auth_url, data=json.dumps(_auth_request), headers=_auth_headers, verify=False)
    # TODO: 5) add Validation(regex) to prevent unwanted updates
    print "Auth Response: {0}".format(_auth_response.status_code)
    _auth_response.raise_for_status()
    _auth = _auth_response.json()
    print "Auth Ticket: {0}".format(_auth["accessToken"])
    return _auth["accessToken"] #, _auth_response.status_code



def main():
    auth = get_mozu_client_authtoken()
    return auth


if __name__ == '__main__':
    main()
