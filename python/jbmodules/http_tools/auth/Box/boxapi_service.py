#!/usr/bin/env python
# -*- coding: utf-8 -*-

urls = ['https://capturemrg.box.com/s/4ocv51zmv5wsb181nvej01awio1wm2qk',
        'https://capturemrg.box.com/s/cyh1md18r4y6tv1j7isaqeu9quwe30qu',
        'https://capturemrg.box.com/s/z2894tj1fdtyw4aix36h3zfxdowf7g3k',
        'https://capturemrg.box.com/s/b7jgrvdrhx6g2z810nzgi3dpveb71b0g',
        'https://capturemrg.box.com/s/cyh1md18r4y6tv1j7isaqeu9quwe30qu'
        ]


def pickler(data, filename=None):
    import cPickle as pickle
    import os.path
    if not filename:
        filename = os.path.join(py_dir, 'boxapi.pkl')
    with open(filename, 'wb', 0) as f:
        # Pickle dictionary using protocol 0.
        pickle.dump(data, output)
        output.close()
    return os.path.join(os.path.abspath('.'), filename)


def depickler(filename,data=None):
    import cPickle as pickle
    with open(filename, 'rb') as f:
        data = pickle.load(f)
        f.close()
    return data


import bottle
import os
from threading import Thread, Event
import webbrowser
from wsgiref.simple_server import WSGIServer, WSGIRequestHandler, make_server
from boxsdk import OAuth2


def jdefault(obj):
    if isinstance(o, set):
        return list(obj)
    return obj.__dict__


def get_store_tokens(access_token=None, refresh_token=None):
    import os.path
    from os import chdir  
    import json 
    py_dir = os.path.dirname(os.path.realpath('/Users/johnb/virtualenvs/GitHub-prodimages/python'))
    chdir(py_dir)
    storage_file = os.path.join(py_dir, 'boxapi' + '.pkl')
    credentials = ''
    try:
        credentials = depickler(storage_file)
    except:
        pass 
    if credentials is None or credentials == False:
        data = { "access_token": access_token, 
                 "refresh_token": refresh_token }
        pickled = pickler(data, filename=storage_file)
        credentials = depickler(storage_file)
        return credentials
    else:
        return credentials


def authenticate(client_secret=None, client_id=None, redirect_uri=None, access_token=None):
    class StoppableWSGIServer(bottle.ServerAdapter):
        def __init__(self, *args, **kwargs):
            super(StoppableWSGIServer, self).__init__(*args, **kwargs)
            self._server = None

        def run(self, app):
            server_cls = self.options.get('server_class', WSGIServer)
            handler_cls = self.options.get('handler_class', WSGIRequestHandler)
            self._server = make_server(self.host, self.port, app, server_cls, handler_cls)
            self._server.serve_forever()

        def stop(self):
            self._server.shutdown()


    auth_code = {}
    auth_code_is_available = Event()
    local_oauth_redirect = bottle.Bottle()
    @local_oauth_redirect.get('/')
    def get_token():
        auth_code['auth_code'] = bottle.request.query.code
        auth_code['state'] = bottle.request.query.state
        auth_code_is_available.set()

    local_server = StoppableWSGIServer(host='localhost', port=51711)
    server_thread = Thread(target=lambda: local_oauth_redirect.run(server=local_server))
    server_thread.start()

    oauth = OAuth2(
        client_id=client_id,
        client_secret=client_secret,
        store_tokens=get_store_tokens
    )
    auth_url, csrf_token = oauth.get_authorization_url(redirect_uri)
    #try:
    #    access_token = store_tokens()
    #    store_tokens(access_token=None, refresh_token=None)
    #    return oauth, access_token
    #except:
    webbrowser.open(auth_url)
    auth_code_is_available.wait()
    local_server.stop()
    assert auth_code['state'] == csrf_token
    access_token, refresh_token = oauth.authenticate(auth_code['auth_code'])
    print('access_token: ' + access_token)
    print('refresh_token: ' + refresh_token)
    return oauth


def get_validated_oauth_accesstoken(client_secret=None, client_id=None, redirect_uri=None):
    from boxsdk import OAuth2
    oauth = authenticate(client_secret=client_secret, client_id=client_id)
    auth_url, csrf_token = oauth.get_authorization_url(redirect_uri)
    access_token, refresh_token = oauth.refresh(auth_url)
    print access_token, refresh_token 
    #refreshed_access_token = store_tokens(access_token, refresh_token)
    return oauth, access_token #, ref_refresh_token


## BoxAppGalleryUrl = 'https://app.box.com/services/auth_download_client'
def download_boxapi_auth_file(client=None, file_id=None, destpath=None):    
    content = client.file(file_id=file_id).content()
    if not destpath:
        return content
    else:
        with open(destpath,'w') as f:
            f.write(content)
            f.close()
        return destpath


def main(image_url, destpath):
    import requests
    from boxsdk import Client
    box_api_shared_root = "https://api.box.com/2.0/shared_items"
    client_secret = 'g4R1o909fgf1PSsa5mLMDslpAwcbfIQl'
    client_id = 'bxccmj5xnkngs8mggxv5ev49zuh80xs9'
    #scope = 'https://app.box.com/services/auth_download_client'
    redirect_uri = 'http://localhost:51711' #'urn:ietf:wg:oauth:2.0:oob'
    oauth, access_token  = get_validated_oauth_accesstoken(client_secret=None, client_id=None, redirect_uri=None)
    client = Client(oauth)
    headers = {
                'Authorization': "Bearer " + access_token,
                'BoxApi': "shared_link=" + image_url
            }
    res = requests.get(box_api_shared_root, headers=headers)
    file_id = res.get('file_id')
    download_boxapi_auth_file(client=client, file_id=file_id, destpath=destpath)


if __name__ == '__main__':
    import sys
    image_url = 'https://capturemrg.box.com/s/cyh1md18r4y6tv1j7isaqeu9quwe30qu'
    destpath  = '/Users/johnb/Desktop/misc_tests2'
    #image_url = sys.argv[1]
    #destpath  = sys.argv[2]
    main(image_url, destpath)
        


#    headers = {
#                'Host' : 'dl.boxcloud.com', 
#                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:37.0) Gecko/20100101 Firefox/37.0', 
#                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
#                'Accept-Language': 'en-US,en;q=0.5',
#                'Referer': image_url,
#                'Connection': 'keep-alive'
#                }
