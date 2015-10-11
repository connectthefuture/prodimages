#!/usr/bin/env python
# -*- coding: utf-8 -*-

#### SET AUTH VARS ####
app_key = 'ikcr68gddbxed1t'
app_secret = 'i4wjfxe0umdvx7c'
token_str = 'aFNqVSoDKPEAAAAAAAAMcj7D7el49caS8gBocryRW99VpF-5K6_GRJi6pQZ5Ii2K'

### Optional ###
username = 'john.bragato@bluefly.com'  
password = 'secret'
# access_type can be 'app_folder' or 'dropbox', depending on
# how you registered your app.
## folder name image_sync_api
## app-name image-sync-api
access_type = 'app_folder'  

#### END VARS ####
import dropbox
import webbrowser
from dropbox import client, rest, session
#import keychain
import pickle
i#mport # console

def get_request_token():
    # console.clear()
    print 'Getting request token...'    
    sess = session.DropboxSession(app_key, app_secret, access_type)
    request_token = sess.obtain_request_token()
    url = sess.build_authorize_url(request_token)
    # console.clear()
    webbrowser.open(url, modal=True)
    return request_token

def get_access_token(token_str=None):
    if token_str:
        pass
    else:
        token_str = globals()['token_str']  ## keychain.get_password('dropbox', app_key)
    if token_str:
        key, secret = pickle.loads(token_str)
        return session.OAuthToken(key, secret)
    request_token = get_request_token()
    sess = session.DropboxSession(app_key, app_secret, access_type)
    access_token = sess.obtain_access_token(request_token)
    token_str = pickle.dumps((access_token.key, access_token.secret))
    keychain.set_password('dropbox', app_key, token_str)
    return access_token

def get_client():
    access_token = get_access_token()
    sess = session.DropboxSession(app_key, app_secret, access_type)
    sess.set_token(access_token.key, access_token.secret)
    dropbox_client = client.DropboxClient(sess)
    return dropbox_client

def main():
    # Demo if started run as a script...
    # Just print the account info to verify that the authentication worked:
    print 'Getting account info...'
    dropbox_client = get_client()
    account_info = dropbox_client.account_info()
    print 'linked account:', account_info

if __name__ == '__main__':
    main()
