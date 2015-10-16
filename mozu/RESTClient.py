#!/usr/bin/env python
# coding: utf-8

# Import initial static vars and Auth func
__base_protocol__               = "https"
__base_url__                    = "staging-sb.mozu.com"
__listFQN__                     = 'files@mozu'
__documentTypeFQN__             = 'image@mozu'
__tenant_name__                 = '11146'
__tenant_url__                  = "{0}://t{1}.{2}".format(__base_protocol__, __tenant_name__,__base_url__ )
### build Mozu API Url String
__document_data_api__   = __tenant_url__ + "/api/content/documentlists/" + __listFQN__ + "/documents"


from base_config import authenticate


class MozuBflyDocument:
    pass

class MozuAlchemyClient:
    pass


class MozuRestClient:
    """Class to interact with Mozus REST API interface -- MozuRestClient"""

    # Class http_status_code
    http_status_code = 777
    __endpoints         = {}
    __listFQN           = __listFQN__
    __documentTypeFQN   = __documentTypeFQN__
    __tenant_name       = __tenant_name__
    ### build Mozu API Url String
    __tenant_url        = __tenant_url__
    __document_data_api = __document_data_api__


    def __init__(self, **kwargs):
        MozuRestClient.__endpoints["endpoint_resource_doclist"] = MozuRestClient.__document_data_api
        self.qstring_filter = kwargs.get('qstring_filter', '')
        self.mz_imageid = kwargs.get('mz_imageid', '')
        if type(self.mz_imageid) == str:
            self.document_resource  = MozuRestClient.__tenant_url + "/api/content/documentlists/" + MozuRestClient.__listFQN + "/documents/" + self.mz_imageid + "/content"
            self.document_metadata_resource  = MozuRestClient.__tenant_url + "/api/content/documentlists/" + MozuRestClient.__listFQN + "/documents/" + self.mz_imageid
            MozuRestClient.__endpoints["endpoint_resource_doc_content"] = self.document_resource
            MozuRestClient.__endpoints["endpoint_resource_doc_metadata"] = self.document_metadata_resource

        # Auth / Connect
        self.accessToken = authenticate()

        # Headers / Data-Payload and Filters
        self.headers = {'Content-type': 'application/json', 'x-vol-app-claims' : self.accessToken, 'x-vol-tenant' : MozuRestClient.__tenant_name, 'x-vol-master-catalog' : '1' } #, 'x-vol-dataview-mode': 'Pending', # ??'x-vol-site' : '1', }
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
        # Build Data Payload
        self.document_payload = {'listFQN' : MozuRestClient.__listFQN, 'documentTypeFQN' : MozuRestClient.__documentTypeFQN, 'name' : self.bf_imageid, 'extension' : self.ext, 'properties': self.properties}
        self.document_response = ''
        print 'Document Payload Set, Response Initialized'

        print kwargs, "End Init -- kwargs"
        #super(MozuRestClient, self).__init__(**kwargs)


    def __str__(self):
        print "MozuID: {0}\tBflyID: {1}".format(self.mz_imageid, self.bf_imageid)
        return "MZID: %s - BFID: %s - Status: %i" % (self.mz_imageid, self.bf_imageid , MozuRestClient.http_status_code)

    def __repr__(self):
        dictrepr = dict.__repr__(self)
        return '{0}({1})'.format(type(self).__name__, dictrepr)

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

    def __contains__(self, key, value):
        return self.__getitem__(dict(self)).__contains__(key)
        #return dict.__getitem__(self).__contains__(value)

    # def update(self, *args, **kwargs):
    #     print 'update', args, kwargs
    #     for k, v in dict(*args, **kwargs).iteritems():
    #         self[k] = v

    ## POST - Document - Create New
    def create_new_mz_image(self):
        import requests, json
        self.headers["Content-type"] = 'application/json'
        _document_data_response = requests.post(MozuRestClient.__document_data_api, data=json.dumps(self.document_payload), headers=self.headers, verify=False )
        print "DocumentPostResponse: {0}".format(_document_data_response.status_code)
        MozuRestClient.http_status_code = _document_data_response.status_code
        if MozuRestClient.http_status_code < 400:
            try:
                self.mz_imageid = _document_data_response.json()['id']
                self.document_resource = MozuRestClient.__document_data_api + "/" + self.mz_imageid + "/content"
                return {self.mz_imageid: self.document_resource}
            except KeyError:
                return (_document_data_response, None,)
        else:
            return {"Failed-POST", MozuRestClient.http_status_code}

    ## PUT - UpdateContent or Load to New Doc obj- Content stream - Send file
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
        self.document_resource = MozuRestClient.__document_data_api + "/" + _mz_imageid
        _content_response = requests.put(self.document_resource + "/content", data=stream, headers=self.headers, verify=False)
        MozuRestClient.http_status_code = _content_response.status_code
        print "ContentPutResponse: {0}".format(_content_response.status_code)
        return _content_response

    ## UPDATE - multi PUT Document DATA AND/OR CONTENT -- uses self.send_content()
    def update_mz_image(self,**kwargs):
        import requests, json
        self.headers["Content-type"] = 'application/json'
        _mz_imageid = kwargs.get('mz_imageid', self.mz_imageid)
        if kwargs.get("properties", dict(self.properties.items()['tags']).values()):
            self.document_payload['properties'] = kwargs.get("properties", self.properties.items()['tags'].values())
        self.document_resource = MozuRestClient.__document_data_api + "/" + _mz_imageid
        _document_data_response = requests.put(self.document_resource, data=json.dumps(self.document_payload), headers=self.headers, verify=False )
        #_document_data_response = requests.patch(self.document_resource, data=json.dumps(self.document_payload), headers=self.headers, verify=False )
        if kwargs.get("src_filepath"):
            _document_content_response = self.send_content(kwargs.get("src_filepath"), **kwargs) #requests.put(self.document_resource, data=json.dumps(self.document_payload), headers=self.headers, verify=False )
            print _document_content_response.headers
        MozuRestClient.http_status_code = _document_content_response.status_code
        try:
            return _document_data_response.json()['id']
        except KeyError:
            return _document_data_response

    ## GET - Single Document Obj by documentId .ie mz_imageid
    ## -- The Document properties that define the content used by the content management system (CMS).
    def get_mz_image_document(self, **kwargs):
        import requests, json
        self.headers["Content-type"] = 'application/json'
        _mz_imageid = kwargs.get('mz_imageid', self.mz_imageid)
        self.document_resource = MozuRestClient.__document_data_api + "/" + _mz_imageid
        # Get Content
        _document_content_response = requests.get(self.document_resource + "/content", data=json.dumps(self.document_payload), headers=self.headers, verify=False )
        MozuRestClient.http_status_code = _document_content_response.status_code
        print "DocumentGetResponse: {0}".format(_document_content_response.status_code)
        try:
            return _document_content_response.json()
        except KeyError:
            return _document_content_response.headers

    ## DELETE - Document Content - Then DELETE the Document Data Object with mzid
    def delete_mz_image(self,**kwargs):
        import requests, json
        self.headers["Content-type"] = 'application/json'
        _mz_imageid = kwargs.get('mz_imageid', self.mz_imageid)
        self.document_resource = MozuRestClient.__document_data_api + "/" + _mz_imageid
        print "Initial MZID URL: {}".format(self.document_resource)
        # Delete Content
        _document_content_response = requests.delete(self.document_resource + "/content", data=json.dumps(self.document_payload), headers=self.headers, verify=False)
        # Delete Document ID - Data TODO: Figure out how to determine the success or failure of Content delete
        _document_data_response = requests.delete(self.document_resource, data=json.dumps(self.document_payload), headers=self.headers, verify=False)
        MozuRestClient.http_status_code = _document_data_response.status_code
        print "DocumentDeleteResponse \n--DataCode: {0} \n--ContentCode: {1} \n\tLocal_MozuID: {2}\n\t-->URL: {3}".format(_document_data_response.status_code, _document_content_response.status_code, _mz_imageid, self.document_resource)
        try:
            return _document_data_response
        except KeyError:
            return _document_data_response.headers()

        #files = {'media': open(src_filepath, 'rb')}

    ###
    # Combined Methods using above base Methods
    ###

    ##  List Files - GET - List of Document PROPERTIES on FileManager - ie. a Single documentList
    def get_mz_image_document_list(self, **kwargs):
        import requests, json
        self.headers["Content-type"] = 'application/json'
        document_list_uri = MozuRestClient.__document_data_api

        ### build query string filter  make this a method eventually
        _qstring_fields = []
        if kwargs.get("filter", ""):
            _qstring_fields.append("filter={{filter}}".format(**kwargs))
        ## "sortBy=productCode+asc"
        if kwargs.get("sort_by", "name+desc"):
            _qstring_fields.append("sortBy={{sort_by}}".format(**kwargs))
        if kwargs.get("response_fields"):
            _qstring_fields.append("responseFields={{response_fields}}".format(**kwargs))
        if kwargs.get("page_size", "50"):
            _qstring_fields.append("pageSize={{page_size}}".format(**kwargs))
            if kwargs.get("start_index"):
                _qstring_fields.append("startIndex={{start_index}}".format(**kwargs))
        if kwargs.get("include_inactive", "True"):
            _qstring_fields.append("includeInactive={{include_inactive}}".format(**kwargs))

        if _qstring_fields:
            from urllib import urlencode, quote_plus
            #_qstring = urlencode(_qstring_fields)
            _qstring = "&".join(_qstring_fields)
            _qstring = quote_plus(_qstring)
            document_list_uri = document_list_uri + "?" + _qstring

        print _qstring_fields, "QSTRING 227"

        _document_list_response = requests.get(document_list_uri, data=json.dumps(self.document_payload), headers=self.headers, verify=False)
        MozuRestClient.http_status_code = _document_list_response.status_code
        print "DocumentGetResponse: {0}".format(_document_list_response.json())
        print document_list_uri
        try:
            ## returns Properties of each Document .get('items')
            return _document_list_response.json()
        except KeyError:
            return _document_list_response.headers

    ## HEAD - Single Documents Content Headers
    def get_mz_image_document_content_headers(self, **kwargs):
        import requests, json
        self.headers["Content-type"] = 'application/json'
        _mz_imageid = kwargs.get('mz_imageid', self.mz_imageid)
        self.document_resource = MozuRestClient.__document_data_api + "/" + _mz_imageid
        # Get Content
        _document_content_response = requests.head(self.document_resource + "/content", data=json.dumps(self.document_payload), headers=self.headers, verify=False)
        MozuRestClient.http_status_code = _document_content_response.status_code
        print "DocumentGetResponse: {0}".format(_document_content_response.status_code)
        try:
            return _document_content_response.json()
        except KeyError:
            return _document_content_response.headers

    ## Download File - GET - Document Content and download to Local or Remote File
    def download_mz_image_content(self, outfile=None, **kwargs):
        import requests, json
        from os import path as path
        _mz_imageid = kwargs.get('mz_imageid', self.mz_imageid)
        self.document_resource = MozuRestClient.__document_data_api + "/" + _mz_imageid + "/content"
        if not self.bf_imageid:
            # Get bflyid from Oracle using mz_id
            from db import mozu_image_table_instance
            self.bf_imageid = mozu_image_table_instance.select( whereclause=(mozu_image_table_instance.c.mz_imageid == self.mz_imageid) )[0]['bf_imageid']
        self.headers["Content-type"] = 'application/json'
        resp = requests.get(self.document_resource, data=json.dumps(self.document_payload), headers=self.headers, verify=False)
        MozuRestClient.http_status_code = resp.status_code
        if MozuRestClient.http_status_code < 400 and MozuRestClient.http_status_code != 0:
            if not outfile:
                outfile = path.join('/tmp', self.bf_imageid)
            else: pass
            with open(outfile,'w') as f:
                f.write(resp.content)
        return resp.content.headers()


def main():
    pass


if __name__ == '__main__':
    main()
