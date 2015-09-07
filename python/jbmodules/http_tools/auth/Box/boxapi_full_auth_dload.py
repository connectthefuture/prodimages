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
TOKENS_FILE = '/usr/local/batchRunScripts/python/jbmodules/image_processing/marketplace/tokens_priv.pkl'

def authenticate(refresh_token=None):

    CLIENT_ID = 'bxccmj5xnkngs8mggxv5ev49zuh80xs9'  # Insert Box client ID here
    CLIENT_SECRET = 'g4R1o909fgf1PSsa5mLMDslpAwcbfIQl'  # Insert Box client secret here

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
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
    )
    auth_url, csrf_token = oauth.get_authorization_url('http://localhost:51711')
    webbrowser.open(auth_url)

    auth_code_is_available.wait()
    local_server.stop()
    assert auth_code['state'] == csrf_token
    access_token, refresh_token = oauth.authenticate(auth_code['auth_code'])

    print('access_token: ' + access_token)
    print('refresh_token: ' + refresh_token)

    #return (access_token, refresh_token,)
    return oauth

####

def exchange_tokens(refresh_token=None):
    
    CLIENT_ID = 'bxccmj5xnkngs8mggxv5ev49zuh80xs9'  # Insert Box client ID here
    CLIENT_SECRET = 'g4R1o909fgf1PSsa5mLMDslpAwcbfIQl'  # Insert Box client secret here

    from os import chdir, path, curdir
    ## Check for stored tokens
    import cPickle as pickle
    initdir = path.abspath(curdir)
    #chdir(path.dirname(path.realpath(__file__)))    
    #TOKENS_FILE = 'tokens.pkl'

    if path.isfile(TOKENS_FILE):
        import requests, json
        #with open(TOKENS_FILE,'rb') as fr:
        #    oldaccess_token, valid_refresh_token = pickle.load(fr)
        with open(TOKENS_FILE,'rb') as fr:
            try:
                oldaccess_token, valid_refresh_token = pickle.load(fr)
            except:
                valid_refresh_token = None
                pass

            if valid_refresh_token is not None:
                pass
            else:
                return

            #else:
            #    oldaccess_token, valid_refresh_token = 'uyT2xUxxZxROzlRjW8T6ge9q7Ne0drdC', 'IVilutwMwaxD9xWWLIpNVffJSQx4GX36Ido8Y2guCFzU6pKrhyovRtooJU8milXn'
        
        box_api_token_root = "https://app.box.com/api/oauth2/token"
        data = {
             ##'Authorization': "Bearer " + access_token,
             ##'BoxApi': "shared_link=" + shared_link,
             'grant_type': 'refresh_token',
             'refresh_token': valid_refresh_token,
             'client_id': CLIENT_ID,
             'client_secret': CLIENT_SECRET
             }
        headers = {
                'Content-Type': 'application/json; charset=UTF-8'
        }
        res = requests.post(box_api_token_root, data=data, headers=headers)
        newcreds = json.loads(res.content)
        print(newcreds)
        try:
            access_token = newcreds['access_token']
            refresh_token = newcreds['refresh_token']
            
            ## Replace old cred dumping new creds to tokens.pkl
            ##---NOTE---## refresh token is valid for 60 days, 
            ##  ------  ## afterwhich the pickle file token_priv should be manually edited/synced
           
            with open(TOKENS_FILE,'wb') as fw:
                pickle.dump((access_token, refresh_token,),  fw)
                print('BoxSuccess')
                return access_token, refresh_token
        except KeyError:
            return
    ###################
    else:
        import __builtin__
        access_token, refresh_token = authenticate()
        pickle.dump((access_token, refresh_token,),  __builtin__.open(TOKENS_FILE,'wb'))
        #chdir(initdir)
        return access_token, refresh_token

###################### ONLY USING ABOVE IN PROD #################

def store_tokens(access_token, refresh_token):
    from oauth2client.file import Storage
    import os    
    py_dir = os.path.dirname(TOKENS_FILE)  #os.path.realpath(__file__))
    os.chdir(py_dir)
    # storage_file = os.path.join(os.path.dirname(py_dir), 'calendar.dat')
    storage_file = os.path.join(py_dir, 'boxapi' + '.dat')
    store = Storage(storage_file)
    credentials = store.get()
    if credentials is None or credentials.invalid == True:
        store.put((access_token, refresh_token,))
        credentials = store.get()
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
    redirect_uri = 'http://localhost:51711' #'urn:ietf:wg:oauth:2.0:oob'
    oauth  = authorize_client(client_secret=client_secret, client_id=client_id,redirect_uri=redirect_uri)
    client = Client(oauth)
    return client

#
# def download_boxapi_auth_file(client=None, image_url=None, destpath=None):
#     try:
#         file_id = qstring2kvpairs(image_url)['id'][0]
#     except IndexError:
#         file_id = regex_boxapi_ret_fileid(image_url)
#         pass
#
#     content = client.file(file_id=file_id).content()
#     if not destpath:
#         return content
#     else:
#         with open(destpath,'w') as f:
#             f.write(content)
#             f.close()
#         return destpath



if __name__ == '__main__':
    authenticate()
    os._exit(0)
