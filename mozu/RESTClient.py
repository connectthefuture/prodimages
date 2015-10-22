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
### valid keys for filtering args
__mozu_image_table_valid_keys__       = [ 'id', 'bf_imageid', 'mz_imageid', 'md5checksum', 'created_date', 'modified_date', 'updated_count' ]
__mozu_query_filter_valid_keys__      = [ 'sortBy', 'filter', 'responseFields', 'pageSize', 'startIndex', 'includeInactive' ]
__mozu_query_filter_valid_operators__ = [ 'sw', 'cont', 'in' ]
__mozu_document_filter_valid_keys__      = [ 'name', 'filter', 'responseFields', 'includeInactive' ]


from base_config import authenticate
from mozu_image_util_functions import log


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


    @log
    def __init__(self, **kwargs):
        MozuRestClient.__endpoints["endpoint_resource_doclist"] = MozuRestClient.__document_data_api
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
        ## TODO does the logic and order below with src_filepath and bf_imageid work or should bf_imageid be first?
        if kwargs.get('src_filepath'):
            self.bf_imageid = kwargs.get('src_filepath').split('/')[-1]
            self.ext = self.bf_imageid.split('.')[-1].lower()
        elif kwargs.get('bf_imageid'):
            self.bf_imageid = kwargs.get('bf_imageid')
            self.ext = self.bf_imageid.split('.')[-1].lower()

        else:
            self.bf_imageid, self.ext = '', ''


        ## Tags - Keywords - Metadata
        self.properties = {'tags': kwargs.get('tags','')}
        # Build Data Payload
        self.document_payload = {'listFQN' : MozuRestClient.__listFQN, 'documentTypeFQN' : MozuRestClient.__documentTypeFQN, 'name' : self.bf_imageid, 'extension' : self.ext, 'properties': self.properties}
        self.document_response = ''
        print 'Document Payload Set, Response Initialized'
        self.request_url_string = self.uri_querystring_formatter(**kwargs)

        print kwargs, "End Init -- kwargs"
        #super(MozuRestClient, self).__init__(**kwargs)


    @log
    def __str__(self):
        print "MozuID: {0}\tBflyID: {1}".format(self.mz_imageid, self.bf_imageid)
        return "MZID: %s - BFID: %s - Status: %i" % (self.mz_imageid, self.bf_imageid , MozuRestClient.http_status_code)

    #@log
    def __repr__(self):
        dictrepr = dict.__repr__(self.__dict__)
        return '{0}({1})'.format(type(self).__name__, dictrepr)

    @log
    def __setitem__(self, key, value):
        #dict.__setitem__(self, key, value)
        self.__dict__[key] = value
        #self[key] = value

    @log
    def __getitem__(self, key):
        #return dict.__getitem__(self, key)
        #return self[key]
        return self.__dict__[key]

    @log
    def __delitem__(self, key):
        del self.__getitem__(dict)[key]

    @log
    def __contains__(self, key, value):
        return self.__getitem__(dict(self)).__contains__(key)
        #return dict.__getitem__(self).__contains__(value)

    #@log
    #def update(self, *args, **kwargs):
    #     print 'update', args, kwargs
    #     for k, v in dict(*args, **kwargs).iteritems():
    #         self[k] = v


    @log
    def uri_querystring_formatter(self, **kwargs):
        from mozu_image_util_functions import include_keys
        from urllib import urlencode, unquote
        ## Default qstring params camel cased to adhere to mozu format
        if kwargs.get("name") or kwargs.get("bf_imageid"):
            kwargs['name'] =  kwargs.get("bf_imageid", kwargs.get("name"))
            kwargs["pageSize" ] = kwargs.get("page_size", "50")
            qstring_args = include_keys(kwargs, __mozu_document_filter_valid_keys__)
            _qstring = "?{}".format(urlencode(qstring_args))
        elif not kwargs.get("mz_imageid"):
            kwargs["sortBy"] =  kwargs.get("sort_by", "name+desc")
            kwargs["pageSize" ] = kwargs.get("page_size", "50")
            kwargs["startIndex" ] = kwargs.get("start_index", "0")
            qstring_args = include_keys(kwargs, __mozu_query_filter_valid_keys__)
            print qstring_args
            _qstring = "?{}".format(unquote(urlencode(qstring_args)))
        else:
            _qstring = ""

        request_url_string = MozuRestClient.__endpoints["endpoint_resource_doclist"] + _qstring
        return request_url_string


    ## POST - Document - Create New
    @log
    def create_new_mz_image(self):
        import requests, json
        self.headers["Content-type"] = 'application/json'
        _document_data_response = requests.post(MozuRestClient.__document_data_api, data=json.dumps(self.document_payload), headers=self.headers, verify=False )
        print "DocumentPostResponse: {0}".format(_document_data_response.status_code)
        MozuRestClient.http_status_code = _document_data_response.status_code
        if MozuRestClient.http_status_code == 201:
            try:
                self.mz_imageid = _document_data_response.json()['id']
                self.document_resource = MozuRestClient.__document_data_api + "/" + self.mz_imageid + "/content"
                return (self.mz_imageid, self.document_resource,)
            except KeyError:
                return (_document_data_response, None,)
        else:
            return ("Failed-POST with code", MozuRestClient.http_status_code)

    ## PUT - UpdateContent or Load to New Doc obj- Content stream - Send file
    @log
    def send_content(self,**kwargs):
        import requests
        from os import path
        ## FileContent
        src_filepath = kwargs.get('src_filepath', "")
        mz_imageid = kwargs.get('mz_imageid', self.mz_imageid)
        self.bf_imageid   = src_filepath.split('/')[-1]
        self.ext = self.bf_imageid.split('.')[-1]
        self.mimetype = "image/{}".format(self.ext.lower().replace('jpg','jpeg'))
        self.headers["Content-type"] = self.mimetype
        try:
            stream = open(path.abspath(src_filepath), 'rb').read()
            self.document_resource = MozuRestClient.__document_data_api + "/" + mz_imageid
            _content_response = requests.put(self.document_resource + "/content", data=stream, headers=self.headers, verify=False)
            MozuRestClient.http_status_code = _content_response.status_code
            print "ContentPutResponse: {0}".format(_content_response.status_code)
            return _content_response
        except IOError:
            print "OIO Error 171 Failed send_content"


    ## UPDATE - multi PUT Document DATA AND/OR CONTENT -- uses self.send_content()
    @log
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
            _document_content_response = self.send_content(**kwargs) #requests.put(self.document_resource, data=json.dumps(self.document_payload), headers=self.headers, verify=False )
            print _document_content_response.headers
        MozuRestClient.http_status_code = _document_content_response.status_code
        try:
            return _document_data_response.json()['id']
        except KeyError:
            return _document_data_response

    ## GET - Single Document Obj by documentId .ie mz_imageid
    ## -- The Document properties that define the content used by the content management system (CMS).
    @log
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
    @log
    def delete_mz_image(self,**kwargs):
        import requests, json
        self.headers["Content-type"] = 'application/json'
        _mz_imageid = kwargs.get('mz_imageid', self.mz_imageid)
        self.document_resource = MozuRestClient.__document_data_api + "/" + _mz_imageid
        # print "Initial MZID URL: {}".format(self.document_resource)
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
    ##  List Files - GET - List of Document Collection PROPERTIES on FileManager - ie. a Single documentList(ie. DocumentCollection)
    @log
    def get_mz_image_document_list(self, **kwargs):
        import requests, json
        from urllib import urlencode, unquote
        self.headers["Content-type"] = 'application/json'
        _qstring = self.uri_querystring_formatter(**kwargs)
        document_list_uri = MozuRestClient.__document_data_api + "?" + _qstring
        print  "QFields 227:\t", kwargs, "\nDoclisturi with QString:\t", document_list_uri
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
    @log
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
    @log
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
