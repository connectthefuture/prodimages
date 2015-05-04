#!/usr/bin/env python
# -*- coding: utf-8 -*-


urls = ['https://capturemrg.box.com/s/4ocv51zmv5wsb181nvej01awio1wm2qk',
        'https://capturemrg.box.com/s/cyh1md18r4y6tv1j7isaqeu9quwe30qu',
        'https://capturemrg.box.com/s/z2894tj1fdtyw4aix36h3zfxdowf7g3k',
        'https://capturemrg.box.com/s/b7jgrvdrhx6g2z810nzgi3dpveb71b0g',
        'https://capturemrg.box.com/s/cyh1md18r4y6tv1j7isaqeu9quwe30qu'
        ]


def store_tokens(access_token, refresh_token):
    from oauth2client.file import Storage
    import os  
    import json 
    py_dir = os.path.dirname(os.path.realpath('/Users/johnb/virtualenvs/GitHub-prodimages/python'))
    os.chdir(py_dir)
    storage_file = os.path.join(py_dir, 'boxapi' + '.dat')
    STORAGE = Storage(storage_file)
    credentials = STORAGE.get()
    if credentials is None or credentials.invalid == True:
        tokens = json.dumps({'access_token: ' + access_token + ', refresh_token: ' + refresh_token}, 
                            sort_keys=True, 
                            separators=(',', ': '))
        STORAGE.put(tokens)
        credentials = STORAGE.get()   
        return credentials
    else:
        return credentials


import bottle
import os
from threading import Thread, Event
import webbrowser
from wsgiref.simple_server import WSGIServer, WSGIRequestHandler, make_server
from boxsdk import OAuth2


def authenticate(client_secret=None, client_id=None, redirect_uri=None):
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

    local_server = StoppableWSGIServer(host='localhost', port=8080)
    server_thread = Thread(target=lambda: local_oauth_redirect.run(server=local_server))
    server_thread.start()

    oauth = OAuth2(
        client_id=client_id,
        client_secret=client_secret,
    )
    auth_url, csrf_token = oauth.get_authorization_url(redirect_uri)
    webbrowser.open(auth_url)
    auth_code_is_available.wait()
    local_server.stop()
    assert auth_code['state'] == csrf_token
    access_token, refresh_token = oauth.authenticate(auth_code['auth_code'])
    print('access_token: ' + access_token)
    print('refresh_token: ' + refresh_token)
    return oauth


def get_validated_oauth(client_secret=None, client_id=None, redirect_uri=None):
    from boxsdk import OAuth2
    from oauth2client.file import Storage
    import os
    oauth = authenticate(client_secret=client_secret, client_id=client_id)
    auth_url, csrf_token = oauth.get_authorization_url(redirect_uri)
    access_token, refresh_token = oauth.refresh(auth_url)
    
    # ref_access_token, ref_refresh_token = store_tokens(access_token, refresh_token)
    return oauth #access_token, ref_refresh_token


def instantiate_boxapi_client():
    from boxsdk import Client
    client_secret = 'g4R1o909fgf1PSsa5mLMDslpAwcbfIQl'
    client_id = 'bxccmj5xnkngs8mggxv5ev49zuh80xs9'
    #scope = 'https://app.box.com/services/auth_download_client'
    redirect_uri = 'http://localhost:8080' #'urn:ietf:wg:oauth:2.0:oob'
    oauth = get_validated_oauth(client_secret=client_secret, client_id=client_id,redirect_uri=redirect_uri)
    client = Client(oauth)
    return client


## BoxAppGalleryUrl = 'https://app.box.com/services/auth_download_client'

def regex_boxapi_ret_fileid(url):
    import re
    regex_boxapi  = re.compile(r'^(https?)?(?:\://)?(.+)\.box\.com/(.+)?(\.?[jpngJPNG]{3,4})?(.*?)?\??(.*?)?$', re.U)
    matches = regex_boxapi.match(url)
    if matches:
        protocol = matches.groups()[0]
        appname  = matches.groups()[1]
        fileId   = {'file_id': matches.groups()[2].split('/')[-1]}
        return fileId.values()[0]
    else:
        pass


def qstring2kvpairs(url_with_qstring):
    from urlparse import urlparse, parse_qs
    url = url_with_qstring.encode('UTF-8')
    #urlparse(url).query
    qkvpairs = parse_qs(urlparse(url).query)
    return qkvpairs


def download_boxapi_auth_file(client=None, file_id=None, image_url=None, destpath=None):
    if not file_id:
        try:
            file_id = qstring2kvpairs(image_url)['id'][0]
        except KeyError:
            file_id = regex_boxapi_ret_fileid(image_url)       
            pass    
    content = client.file(file_id=file_id).content()
    if not destpath:
        return content
    else:
        with open(destpath,'w') as f:
            f.write(content)
            f.close()
        return destpath



if __name__ == '__main__':
    import sys
    
    boxclient = 
    
