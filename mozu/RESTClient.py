#!/usr/bin/env python
# coding: utf-8

# Import initial static vars and Auth func
from base_config import *

class MozuBflyDocument:
    pass

class MozuAlchemyClient:
    pass


class MozuRestClient:
    """docstring for MozuRestClient"""

    # global http_status_code
    http_status_code = 777

    def __init__(self, **kwargs):

        ### Mozu Defaults - Tenant --> FQN
        self.listFQN = 'files@mozu'
        self.documentTypeFQN = 'image@mozu'
        self.tenant_name = '11146'

        ### build Mozu API Url String
        self.tenant_url = "https://t{0}.staging-sb.mozu.com/".format(self.tenant_name)
        self.document_data_api    = self.tenant_url + "/api/content/documentlists/" + self.listFQN + "/documents"
        self.qstring_filter = kwargs.get('qstring_filter', '')
        self.mz_imageid = kwargs.get('mz_imageid', '')
        if type(self.mz_imageid) == str:
            self.document_resource  = self.tenant_url + "/api/content/documentlists/" + self.listFQN + "/documents/" + self.mz_imageid + "/content"

        # Auth / Connect
        self.accessToken = get_mozu_client_authtoken()

        # Headers / Data-Payload and Filters
        self.headers = {'Content-type': 'application/json', 'x-vol-app-claims' : self.accessToken, 'x-vol-tenant' : self.tenant_name, 'x-vol-master-catalog' : '1' } #, 'x-vol-dataview-mode': 'Pending', # ??'x-vol-site' : '1', }
        if kwargs.get('bf_imageid'):
            self.bf_imageid = kwargs.get('bf_imageid')
            self.ext = self.bf_imageid.split('.')[-1].lower()
        elif kwargs.get('src_filepath'):
            self.bf_imageid = kwargs.get('src_filepath').split('/')[-1]
            self.ext = self.bf_imageid.split('.')[-1].lower()
        else:
            self.bf_imageid, self.ext = '', ''


        ## Tags - Keywords - Metadata
        self.properties = {'tags': kwargs.get('tags','')}

        self.document_payload = {'listFQN' : self.listFQN, 'documentTypeFQN' : self.documentTypeFQN, 'name' : self.bf_imageid, 'extension' : self.ext, 'properties': self.properties}
        self.document_response = ''
        print 'Document Payload Set, Response Initialized'

        print kwargs, "End Init -- kwargs"
        #super(MozuRestClient, self).__init__(**kwargs)


    def __str__(self):
        print "MozuID: {0}\tBflyID: {1}".format(self.mz_imageid, self.bf_imageid)
        return "MZID: %s - BFID: %s - Status: %i" % (self.mz_imageid, self.bf_imageid , MozuRestClient.http_status_code)

    #def __repr__(self):
        #dictrepr = dict.__repr__(self)
        #return '%s(%s)' % (type(self).__name__, dictrepr)

    def __setitem__(self, key, value):
        #dict.__setitem__(self, key, value)
        self.__dict__[key] = value
        #self[key] = value

    def __getitem__(self, key):
        #return dict.__getitem__(self, key)
        #return self[key]
        return self.__dict__[key]

    def __delitem__(self, key):
        del self.__getitem__(dict)[key]

    def __contains__(self, key):
        return self.__getitem__(key).__contains__()

    def update(self, *args, **kwargs):
        print 'update', args, kwargs
        for k, v in dict(*args, **kwargs).iteritems():
            self[k] = v

    ## POST - Document
    def create_new_mz_image(self):
        import requests, json
        self.headers["Content-type"] = 'application/json'
        _document_response = requests.post(self.document_data_api, data=json.dumps(self.document_payload), headers=self.headers, verify=False )
        print "DocumentPostResponse: {0}".format(_document_response.status_code)
        MozuRestClient.http_status_code = _document_response.status_code
        if MozuRestClient.http_status_code < 400:
            try:
                self.mz_imageid = _document_response.json()['id']
                self.document_resource = self.document_data_api + self.mz_imageid + "/content"
                return (self.mz_imageid, self.document_resource,)
            except KeyError:
                return (_document_response, None,)
        else:
            return ("Failed-POST", MozuRestClient.http_status_code,)

    ## Update or New PUT - Content stream - Send file
    def send_content(self, src_filepath, **kwargs):
        import requests
        from os import path
        ## FileContent
        _mz_imageid = kwargs.get('mz_imageid', self.mz_imageid)
        self.bf_imageid   = src_filepath.split('/')[:-1]
        self.ext = self.bf_imageid.split('.')[-1]
        self.mimetype = "image/{}".format(self.ext.lower().replace('jpg','jpeg'))
        self.headers["Content-type"] = self.mimetype
        stream = open(path.abspath(src_filepath), 'rb').read()

        self.document_resource = self.document_data_api + _mz_imageid + "/content"
        _content_response = requests.put(self.document_resource, data=stream, headers=self.headers, verify=False)
        MozuRestClient.http_status_code = _content_response.status_code
        print "ContentPutResponse: {0}".format(_content_response.status_code)
        return _content_response

    ## UPDATE - PUT Document
    def update_mz_image(self, **kwargs):
        import requests, json
        self.headers["Content-type"] = 'application/json'
        _mz_imageid = kwargs.get('mz_imageid', self.mz_imageid)
        self.document_resource = self.document_data_api + _mz_imageid + "/content"
        if kwargs.get("src_filepath"):
            _document_response = requests.put(self.document_resource, data=json.dumps(self.document_payload), headers=self.headers, verify=False )
        else:
            _document_response = requests.put(self.document_data_api, data=json.dumps(self.document_payload), headers=self.headers, verify=False )
            print _document_response
            if kwargs.get("properties", dict(self.properties.items()['tags']).values()):
                self.document_payload['properties'] = kwargs.get("properties", self.properties.items()['tags'].values())
                _document_response = requests.put(self.document_resource, data=json.dumps(self.document_payload), headers=self.headers, verify=False )

        MozuRestClient.http_status_code = _document_response.status_code
        try:
            return _document_response.json()['id']
        except KeyError:
            return _document_response

    ## GET - List of Documents on FileManager
    def get_mz_image_document_list(self, **kwargs):
        import requests, json
        self.headers["Content-type"] = 'application/json'
        response_fields = kwargs.get("response_fields", "")
        if response_fields:
            self.qstring_filter = "?responseFields\={{response_fields}}".format(response_fields=response_fields)
        document_list_uri = "/".join(self.document_data_api.split('/')[:-1])
        _document_response = requests.get(document_list_uri, data=json.dumps(self.document_payload), headers=self.headers, verify=False )
        MozuRestClient.http_status_code = _document_response.status_code
        print "DocumentGetResponse: {0}".format(_document_response.status_code)
        try:
            return _document_response.json()
        except KeyError:
            return _document_response


    ## GET - Document
    def get_mz_image_document(self, **kwargs):
        import requests, json
        self.headers["Content-type"] = 'application/json'
        _mz_imageid = kwargs.get('mz_imageid', self.mz_imageid)
        self.document_resource = self.document_data_api + _mz_imageid + "/content"
        _document_response = requests.get(self.document_resource, data=json.dumps(self.document_payload), headers=self.headers, verify=False )
        MozuRestClient.http_status_code = _document_response.status_code
        print "DocumentGetResponse: {0}".format(_document_response.status_code)
        try:
            return _document_response.json()
        except KeyError:
            return _document_response


    ## GET - Document
    def download_mz_image_content(self, outfile=None, **kwargs):
        import requests, json
        from os import path as path
        _mz_imageid = kwargs.get('mz_imageid', self.mz_imageid)
        self.document_resource = self.document_data_api + _mz_imageid + "/content"
        if not self.bf_imageid:
            # Get bflyid from Oracle using mz_id
            from db import mozu_image_table_instance
            self.bf_imageid = mozu_image_table_instance.select( whereclause=(mozu_image_table_instance.c.mz_imageid == self.mz_imageid) )[0]['bf_imageid']

        self.headers["Content-type"] = 'application/json'
        self.document_resource = self.document_data_api + self.mz_imageid + "/content"
        resp = requests.get(self.document_resource, data=json.dumps(self.document_payload), headers=self.headers, verify=False )
        MozuRestClient.http_status_code = resp.status_code
        if MozuRestClient.http_status_code < 400 and MozuRestClient.http_status_code != 0:
            if not outfile:
                outfile = path.join('/tmp', self.bf_imageid)
            else: pass
            with open(outfile,'w') as f:
                f.write(resp.content)
        return resp.content.headers()


    ## DELETE - Document
    def delete_mz_image(self,**kwargs):
        import requests, json
        self.headers["Content-type"] = 'application/json'
        _mz_imageid = kwargs.get('mz_imageid', self.mz_imageid)
        self.document_resource = self.document_data_api + _mz_imageid + "/content"
        _document_response = requests.delete(self.document_resource, data=json.dumps(self.document_payload), headers=self.headers, verify=False )
        MozuRestClient.http_status_code = _document_response.status_code
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
