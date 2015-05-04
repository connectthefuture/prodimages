#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import bottle
import os
from threading import Thread, Event
import webbrowser
from wsgiref.simple_server import WSGIServer, WSGIRequestHandler, make_server

from boxsdk import OAuth2


CLIENT_ID = 'bxccmj5xnkngs8mggxv5ev49zuh80xs9'  # Insert Box client ID here
CLIENT_SECRET = 'g4R1o909fgf1PSsa5mLMDslpAwcbfIQl'  # Insert Box client secret here


def authenticate():
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
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
    )
    auth_url, csrf_token = oauth.get_authorization_url('http://localhost:8080')
    webbrowser.open(auth_url)

    auth_code_is_available.wait()
    local_server.stop()
    assert auth_code['state'] == csrf_token
    access_token, refresh_token = oauth.authenticate(auth_code['auth_code'])

    print('access_token: ' + access_token)
    print('refresh_token: ' + refresh_token)

    return oauth


def store_tokens(access_token, refresh_token):
    from oauth2client.file import Storage
    import os    
    py_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(py_dir)
    # storage_file = os.path.join(os.path.dirname(py_dir), 'calendar.dat')
    storage_file = os.path.join(py_dir, 'boxapi' + '.dat')
    STORAGE = Storage(storage_file)
    credentials = STORAGE.get()
    if credentials is None or credentials.invalid == True:
        STORAGE.put(access_token, refresh_token)
        credentials = STORAGE.get()   
    else:
        access_token, refresh_token = credentials
    return credentials


def authorize_client(**kwargs):
    from boxsdk import OAuth2
    oauth = OAuth2(
        client_secret=kwargs.get('client_secret'),
        client_id = kwargs.get('client_id'),
        store_tokens=store_tokens,
    )
    auth_url, csrf_token = oauth.get_authorization_url(kwargs.get('redirect_uri'))
    return auth_url, csrf_token


def instantiate_boxapi_client():
    from boxsdk import Client
    client_secret = 'g4R1o909fgf1PSsa5mLMDslpAwcbfIQl'
    client_id = 'bxccmj5xnkngs8mggxv5ev49zuh80xs9'
    #scope = 'https://app.box.com/services/auth_download_client'
    redirect_uri = 'http://localhost:8080' #'urn:ietf:wg:oauth:2.0:oob'
    oauth  = authorize_client(client_secret=client_secret, client_id=client_id,redirect_uri=redirect_uri)
    client = Client(oauth)
    return client


def download_boxapi_auth_file(client=None, image_url=None, destpath=None):
    try:
        file_id = qstring2kvpairs(image_url)['id'][0]
    except IndexError:
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
    authenticate()
    os._exit(0)
