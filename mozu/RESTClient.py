#!/usr/bin/env python
# coding: utf-8

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
        print "Auth Ticket: {0}".format(_auth["accessToken)"])
        return _auth["accessToken"] #, _auth_response.status_code

class MozuBflyImage:
    pass

class MozuAlchemyClient:
    pass

class MozuRestClient:
    """docstring for MozuRestClient"""

    def __init__(self, **kwargs):
        import os.path as path
        import requests, json

        # Auth / Connect / HTTP Status - Globalized
        global http_status_code
        http_status_code = 0
        self.http_status_code = http_status_code
        #self.accessToken, self.http_status_code = get_mozu_client_authtoken()
        self.accessToken = get_mozu_client_authtoken()
        global mz_imageid
        mz_imageid = kwargs.get('mz_imageid', '')
        self.mz_imageid = mz_imageid

        ### Mozu Defaults - Tenant --> FQN
        self.listFQN = 'files@mozu'
        self.documentTypeFQN = 'image@mozu'
        self.tenant_name = '11146'

        ### build Mozu API Url String
        self.tenant_url = "https://t{0}.staging-sb.mozu.com/".format(self.tenant_name)
        self.document_data_api    = self.tenant_url + "/api/content/documentlists/" + self.listFQN + "/documents"
        global document_content_api
        self.document_content_api = '' # self.tenant_url + "/api/content/documentlists/" + self.listFQN + "/documents/" + self.mz_imageid + "/content"
        self.document_resource  = self.tenant_url + "/api/content/documentlists/" + self.listFQN + "/documents/" + self.mz_imageid + "/content"

        ## FileContent
        self.src_filepath = kwargs.get('src_filepath', '')
        # self.new_mz_imageid = ''
        self.bf_imageid   = path.basename(self.src_filepath) #[:-1]
        self.ext = self.bf_imageid.split('.')[-1]
        self.mimetype = "image/{}".format(self.ext.lower().replace('jpg','jpeg'))

        ## Tags - Keywords - Metadata
        _tags_list =  kwargs.get('tags','')
        self.properties = {u'tags': _tags_list}

        # Headers / Data-Payload and Filters
        self.qstring_filter = kwargs.get('qstring_filter', '')
        self.headers = {'Content-type': 'application/json', 'x-vol-app-claims' : self.accessToken, 'x-vol-tenant' : self.tenant_name, 'x-vol-master-catalog' : '1' } #, 'x-vol-dataview-mode': 'Pending', # ??'x-vol-site' : '1', }
        self.document_payload = {'listFQN' : self.listFQN, 'documentTypeFQN' : self.documentTypeFQN, 'name' : self.bf_imageid, 'extension' : self.ext, 'properties': self.properties}
        self.document_response = ''
        #super(MozuRestClient, self).__init__(**kwargs)


    def __repr__(self):
        print "MozuID: {0}\tBflyID: {1}".format(self.mz_imageid, self.bf_imageid)
        return "MZID: %s - BFID: %s - Status: %i" % (self.mz_imageid, self.bf_imageid ,self.http_status_code)


    ## POST - Document
    def create_new_mz_image(self):
        import requests, json
        self.headers["Content-type"] = 'application/json'
        _document_response = requests.post(self.document_data_api, data=json.dumps(self.document_payload), headers=self.headers, verify=False )
        print "DocumentPostResponse: {0}".format(_document_response.status_code)
        self.http_status_code = _document_response.status_code
        if self.http_status_code < 400:
            try:
                self.mz_imageid = _document_response.json()['id']
                return _document_response.json()['id']
            except KeyError:
                return _document_response


    ## PUT - Content stream - Send file
    def send_content(self):
        import requests, json
        self.headers["Content-type"] = self.mimetype
        stream = open(self.src_filepath, 'rb').read()
        _document_content_api = self.tenant_url + "/api/content/documentlists/" + self.listFQN + "/documents/" + self.mz_imageid + "/content"
        self.document_content_api = _document_content_api
        print _document_content_api, self.document_content_api
        content_response = requests.put(self.document_resource, data=stream, headers=self.headers, verify=False)
        self.http_status_code = content_response.status_code
        print "ContentPutResponse: {0}".format(content_response.status_code)
        return content_response

    ## UPDATE - PUT Document
    def update_mz_image(self):
        import requests, json
        self.headers["Content-type"] = 'application/json'
        if self.src_filepath:
            _document_response = requests.put(self.document_resource, data=json.dumps(self.document_payload), headers=self.headers, verify=False )
        else:
            _document_response = requests.put(self.document_data_api, data=json.dumps(self.document_payload), headers=self.headers, verify=False )
            print _document_response
            if self.properties.items()['tags'].values():
                _document_response = requests.put(self.document_resource, data=json.dumps(self.document_payload), headers=self.headers, verify=False )

        self.http_status_code = _document_response.status_code
        try:
            return _document_response.json()['id']
        except KeyError:
            return _document_response

    ## GET - Document
    def get_mz_image(self):
        import requests, json
        self.headers["Content-type"] = 'application/json'
        _document_response = requests.get(self.document_resource, data=json.dumps(self.document_payload), headers=self.headers, verify=False )
        self.http_status_code = _document_response.status_code
        print "DocumentGetResponse: {0}".format(_document_response.status_code)
        try:
            return _document_response.json()
        except KeyError:
            return _document_response

    ## DELETE - Document
    def delete_mz_image(self):
        import requests, json
        self.headers["Content-type"] = 'application/json'
        _document_response = requests.delete(self.document_resource, data=json.dumps(self.document_payload), headers=self.headers, verify=False )
        self.http_status_code = _document_response.status_code
        print "DocumentDeleteResponse: {0} -- {1} -- {2}".format(_document_response.status_code, _document_response.url, self.document_data_api)
        try:
            return _document_response
        except KeyError:
            return _document_response.headers()

        #files = {'media': open(src_filepath, 'rb')}

def main():
    pass


if __name__ == '__main__':
    main()