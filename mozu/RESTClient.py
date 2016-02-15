#!/usr/bin/env python
# coding: utf-8

from os import environ
from mozu_image_util_functions import log

## Import and set static connection environmental variables -- sql_alchemy_uri, mozu_tenant etc.
from base_config import authenticate, set_environment
set_environment()

# Import initial static vars and Auth func Can set using environ or static
__base_protocol__          =  environ['MOZU_PROTOCOL']
__base_url__               =  environ['MOZU_BASE_URL']
__listFQN__                =  environ['MOZU_LIST_FQN']
__documentTypeFQN__        =  environ['MOZU_DOCUMENT_TYPE_FQN']
__master_catalogid__       =  environ['MOZU_MASTER_CATALOG_ID']
__tenant_name__            =  environ['MOZU_TENANT_NAME']
### build Mozu API Url Strings from env vars
__tenant_url__             =  "{0}://t{1}.{2}".format(__base_protocol__, __tenant_name__,__base_url__ )
__document_data_api__      = __tenant_url__ + "/api/content/documentlists/" + __listFQN__ + "/documents"
__document_tree_api__      = __tenant_url__ + "/api/content/documentlists/" + __listFQN__ + "/documentTree"

### valid keys for filtering insert fields and other query fields or args`
__mozu_image_table_valid_keys__         = [ 'id', 'bf_imageid', 'mz_imageid', 'md5checksum', 'created_date', 'modified_date', 'updated_count' ]
__mozu_query_filter_valid_keys__        = [ 'sortBy', 'filter', 'responseFields', 'pageSize', 'startIndex', 'includeInactive' ]
__mozu_query_filter_valid_operators__   = [ 'sw', 'cont', 'in' ]
__mozu_document_filter_valid_keys__     = [ 'name', 'filter', 'responseFields', 'includeInactive' ]


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
    __master_catalogid      = __master_catalogid__
    ### build Mozu API Url String
    __tenant_url        = __tenant_url__
    __document_data_api = __document_data_api__
    __document_tree_api = __document_tree_api__


    @log
    def __init__(self, **kwargs):
        # MozuRestClient.__endpoints["endpoint_resource_doclist"] = MozuRestClient.__document_data_api
        # self.mz_imageid = kwargs.get('mz_imageid', '')
        # if type(self.mz_imageid) == str:
        #     self.document_resource  = MozuRestClient.__tenant_url + "/api/content/documentlists/" + MozuRestClient.__listFQN + "/documents/" + self.mz_imageid
        #     self.document_resource_content  = MozuRestClient.__tenant_url + "/api/content/documentlists/" + MozuRestClient.__listFQN + "/documents/" + self.mz_imageid + "/content"
        #     self.document_metadata_resource  = MozuRestClient.__tenant_url + "/api/content/documentlists/" + MozuRestClient.__listFQN + "/documents/" + self.mz_imageid
        #     MozuRestClient.__endpoints["endpoint_resource_doc_content"] = self.document_resource_content
        #     MozuRestClient.__endpoints["endpoint_resource_doc_metadata"] = self.document_metadata_resource
        # elif len(self.bf_imageid) >= 9:
        #     self.document_tree_resource_content = MozuRestClient.__tenant_url + "/api/content/documentlists/" + MozuRestClient.__listFQN + "/documentTree/" + self.bf_imageid + "/content"  ## ?folderPath={folderPath}&folderId={folderId}
        #     MozuRestClient.__endpoints["endpoint_resource_doc_tree_content"] = self.document_tree_resource_content
        # Auth / Connect
        self.accessToken = authenticate()

        # Headers / Data-Payload and Filters
        self.headers = {'Content-type': 'application/json', 'x-vol-app-claims': self.accessToken, 'x-vol-tenant': MozuRestClient.__tenant_name, 'x-vol-master-catalog': MozuRestClient.__master_catalogid } #, 'x-vol-dataview-mode': 'Pending', # ??'x-vol-site' : '1', }
        ## TODO does the logic and order below with src_filepath and bf_imageid work or should bf_imageid be first?
        if kwargs.get('src_filepath'):
            self.bf_imageid, self.ext = kwargs.get('src_filepath').split('/')[-1].split('.')
            self.ext = self.ext.lower() # self.bf_imageid.split('.')[-1].lower()
        elif kwargs.get('bf_imageid'):
            self.bf_imageid = kwargs.get('bf_imageid')
            self.ext = 'jpg' # self.bf_imageid.split('.')[-1].lower()
        else:
            self.bf_imageid, self.ext = '', ''

        ## Tags - Keywords - Metadata
        self.properties = {'tags': kwargs.get('tags','')}
        # Build Data Payload
        self.document_payload =  self.set_document_payload() #{'listFQN' : MozuRestClient.__listFQN, 'documentTypeFQN' : MozuRestClient.__documentTypeFQN, 'name' : self.bf_imageid, 'extension' : self.ext, 'properties': self.properties}
        self.document_response = ''
        print 'Document Payload Set, Response Initialized'
        self.request_url_string = self.set_query_string(**kwargs)
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
    # @property

    @log
    def set_document_payload(self, **kwargs):
        self.bf_imageid = kwargs.get('bf_imageid', self.bf_imageid)
        self.mz_imageid = kwargs.get('mz_imageid', self.mz_imageid)
        self.ext        = kwargs.get('ext', self.ext)
        self.properties = kwargs.get('mz_imageid', self.mz_imageid)
        _document_payload = {'listFQN' : MozuRestClient.__listFQN, 'documentTypeFQN' : MozuRestClient.__documentTypeFQN, 'name' : self.bf_imageid, 'extension' : self.ext, 'properties': self.properties}
        print("Setting Document Payload\n\t{}".format(_document_payload))
        return _document_payload
    #document_payload = property(set_document_payload)

    @log
    def set_endpoint_uri(self, **kwargs):
        self.bf_imageid = kwargs.get('bf_imageid', self.bf_imageid)
        self.mz_imageid = kwargs.get('mz_imageid', self.mz_imageid)
        MozuRestClient.__endpoints["endpoint_resource_doclist"] = MozuRestClient.__document_data_api
        MozuRestClient.__endpoints["endpoint_resource_doc_metadata"] = MozuRestClient.__endpoints["endpoint_resource_doclist"] + self.mz_imageid
        MozuRestClient.__endpoints["endpoint_resource_doc_content"] = MozuRestClient.__endpoints["endpoint_resource_doc_metadata"] + "/content"
        MozuRestClient.__endpoints["endpoint_resource_doc_tree_content"] =  MozuRestClient.__document_tree_api + self.bf_imageid + "/content"
        print("Setting Endpoints\n\t{}".format(MozuRestClient.__endpoints))
        return MozuRestClient.__endpoints
    #endpoint_uri = property(set_document_payload)

    @log
    def set_query_string(self,**kwargs):
        from mozu_image_util_functions import include_keys
        from urllib import urlencode, unquote
        ## Default qstring params camel cased to adhere to mozu format
        if kwargs.get("name"): # or kwargs.get("bf_imageid"):
            kwargs['name'] =  kwargs.get("name")
            kwargs["pageSize"] = kwargs.get("page_size", "150")
            qstring_args = include_keys(kwargs, __mozu_document_filter_valid_keys__)
            _qstring = "?{}".format(urlencode(qstring_args))
        elif not kwargs.get("mz_imageid"):
            kwargs["sortBy"] =  kwargs.get("sort_by", "name+desc")
            kwargs["pageSize"] = kwargs.get("page_size", "200")
            kwargs["startIndex" ] = kwargs.get("start_index", "0")
            qstring_args = include_keys(kwargs, __mozu_query_filter_valid_keys__)
            print qstring_args
            _qstring = "?{}".format(unquote(urlencode(qstring_args)))
        else:
            _qstring = ""
        return _qstring


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
                self.document_resource_content = self.set_endpoint_uri(**kwargs)["endpoint_resource_doc_content"]
                return (self.mz_imageid, self.document_resource_content,)
            except KeyError:
                return (_document_data_response, "Keyerror",)
        else:
            return (_document_data_response, "Keyerror",)  # "Failed-POST with code: {}".format(MozuRestClient.http_status_code), MozuRestClient.http_status_code,

    ## PUT - UpdateContent or Load to New Doc obj- Content stream - Send file
    @log
    def send_content(self,**kwargs):
        import requests
        from os import path
        ## FileContent
        if not self.mz_imageid:
            src_filepath = kwargs.get('src_filepath', '')
            mz_imageid = kwargs.get('mz_imageid', self.mz_imageid)
            self.bf_imageid = src_filepath.split('/')[-1].split('.')[0]
            _endpoint = self.set_endpoint_uri(**kwargs)["endpoint_resource_doc_tree_content"]
        else:
            src_filepath = kwargs.get('src_filepath', '')
            mz_imageid = kwargs.get('mz_imageid', self.mz_imageid)
            _endpoint = self.set_endpoint_uri(**kwargs)["endpoint_resource_doc_content"]
        if not self.ext:
            self.ext = 'jpg'
        self.mimetype = "image/{}".format(self.ext.lower().replace('jpg','jpeg'))
        self.headers["Content-type"] = self.mimetype
        set_document_payload(**kwargs)
        try:
            stream = open(path.abspath(src_filepath), 'rb').read()
            _content_response = requests.put(_endpoint, data=stream, headers=self.headers, verify=False)
            MozuRestClient.http_status_code = _content_response.status_code
            print "ContentPutResponse: {0}".format(_content_response.status_code)
            return _content_response
        except AttributeError:
            print "OIO Error 171 Failed send_content"

    def get_content(self, **kwargs):
        import requests
        from os import path
        ## FileContent
        if not self.mz_imageid:
            src_filepath = kwargs.get('src_filepath', '')
            mz_imageid = kwargs.get('mz_imageid', self.mz_imageid)
            self.bf_imageid = src_filepath.split('/')[-1].split('.')[0]
            _endpoint = self.set_endpoint_uri(**kwargs)["endpoint_resource_doc_tree_content"]
        else:
            src_filepath = kwargs.get('src_filepath', '')
            mz_imageid = kwargs.get('mz_imageid', self.mz_imageid)
            _endpoint = self.set_endpoint_uri(**kwargs)["endpoint_resource_doc_content"]
        if not self.ext:
            self.ext = 'jpg'
        self.mimetype = "image/{}".format(self.ext.lower().replace('jpg', 'jpeg'))
        self.headers["Content-type"] = self.mimetype
        set_document_payload(**kwargs)
        try:
            _content_response = requests.get(_endpoint, headers=self.headers, verify=False)
            MozuRestClient.http_status_code = _content_response.status_code
            print "ContentPutResponse: {0}".format(_content_response.status_code)
            return _content_response
        except AttributeError:
            print "OIO Error 171 Failed send_content"

    ## UPDATE - multi PUT Document DATA AND/OR CONTENT -- uses self.send_content()
    @log
    def update_mz_image(self,**kwargs):
        import requests, json
        self.headers["Content-type"] = 'application/json'
        _mz_imageid = kwargs.get('mz_imageid', self.mz_imageid)
        _bf_imageid = kwargs.get('bf_imageid', self.bf_imageid)
        if kwargs.get("properties", dict(self.properties.items()['tags']).values()):
            self.document_payload['properties'] = kwargs.get("properties", self.properties.items()['tags'].values())
        if kwargs.get("src_filepath") and not _bf_imageid:
            self.bf_imageid = kwargs['bf_imageid'] = kwargs.get("src_filepath").split('/')[-1].split('.')[0]
        _document_content_response = self.send_content(**kwargs) #requests.put(self.document_resource, data=json.dumps(self.document_payload), headers=self.headers, verify=False )
        print _document_content_response.headers
        MozuRestClient.http_status_code = _document_content_response.status_code
        try:
            return _document_content_response.json()['id']
        except KeyError:
            print 'REST Client Update mzimage Failed --> KeyError'
            return MozuRestClient.http_status_code

    ## GET - Single Document Obj by documentId .ie mz_imageid
    ## -- The Document properties that define the content used by the content management system (CMS).
    @log
    def get_mz_image_document(self, **kwargs):
        import requests, json
        self.headers["Content-type"] = 'application/json'
        _mz_imageid = kwargs.get('mz_imageid', self.mz_imageid)
        _endpoint = self.set_endpoint_uri(**kwargs)["endpoint_resource_doc_content"]
        # Get Content
        _document_content_response = requests.get(_endpoint, data=json.dumps(self.document_payload), headers=self.headers, verify=False )
        MozuRestClient.http_status_code = _document_content_response.status_code
        print "DocumentGetResponse: {0}".format(_document_content_response.status_code)
        try:
            return _document_content_response.json()
        except KeyError:
            return _document_content_response.headers

    ## DELETE - Document Content - Then DELETE the Document Data Object with mzid
    @log
    def delete_mz_image(self, **kwargs):
        import requests, json
        self.headers["Content-type"] = 'application/json'
        self.mz_imageid = kwargs.get('mz_imageid', self.mz_imageid)
        self.bf_imageid = kwargs.get('bf_imageid', self.bf_imageid)
        if self.mz_imageid:
            # Use regular documentList content endpoint
            #self.document_resource = MozuRestClient.__document_data_api + "/" + self.mz_imageid + "/content"
            _endpoint = self.set_endpoint_uri(**kwargs)["endpoint_resource_doc_content"]
        elif self.bf_imageid:
            # Use alternate documentListTree content endpoint
            #self.document_tree_resource_content = MozuRestClient.__tenant_url + "/api/content/documentlists/" + MozuRestClient.__listFQN + "/documentTree/" + self.bf_imageid + "/content"  ## ?folderPath={folderPath}&folderId={folderId}
            _endpoint = self.set_endpoint_uri(**kwargs)["endpoint_resource_doc_tree_content"]
        # Delete Content
        _document_content_response = requests.delete(_endpoint, data=json.dumps(self.document_payload), headers=self.headers, verify=False)
        # Delete Document ID - Data TODO: Figure out how to determine the success or failure of Content delete
        # _document_data_response = requests.delete(self.document_resource, data=json.dumps(self.document_payload), headers=self.headers, verify=False)
        MozuRestClient.http_status_code = _document_data_response.status_code
        print "DocumentDeleteResponse \n--DataCode: {0} \n--ContentCode: {1} \n\tLocal_MozuID: {2}\n\t-->URL: {3}".format(_document_data_response.status_code, _document_content_response.status_code, self.mz_imageid, self.document_resource)
        try:
            return _document_content_response
        except KeyError:
            return _document_content_response.headers()

    ### files = {'media': open(src_filepath, 'rb')}
    ###
    # Combined Methods using above base Methods
    ###
    ##  List Files - GET - List of Document Collection PROPERTIES on FileManager - ie. a Single documentList(ie. DocumentCollection)
    @log
    def get_mz_image_document_list(self, **kwargs):
        import requests, json
        # from urllib import urlencode, unquote
        self.headers["Content-type"] = 'application/json'
        _qstring = self.set_query_string(**kwargs)
        document_list_uri = MozuRestClient.__document_data_api + _qstring
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
        _endpoint = self.set_endpoint_uri(**kwargs)["endpoint_resource_doc_content"]
        # Get Content
        _document_content_response = requests.head(_endpoint, data=json.dumps(self.document_payload), headers=self.headers, verify=False)
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
        _endpoint = self.set_endpoint_uri(**kwargs)["endpoint_resource_doc_tree_content"]
        if not self.bf_imageid:
            # Get bflyid from Oracle using mz_id
            from db import mozu_image_table_instance
            self.bf_imageid = mozu_image_table_instance.select( whereclause=(mozu_image_table_instance.c.mz_imageid == self.mz_imageid) )[0]['bf_imageid']
        self.headers["Content-type"] = 'application/json'
        resp = requests.get(_endpoint, data=json.dumps(self.document_payload), headers=self.headers, verify=False)
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
