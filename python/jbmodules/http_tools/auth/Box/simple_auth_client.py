#!/usr/bin/env python
# -*- coding: utf-8 -*-


def store_tokens(access_token, refresh_token):
    import os    
    py_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(py_dir)
    # storage_file = os.path.join(os.path.dirname(py_dir), 'calendar.dat')
    storage_file = os.path.join(py_dir, 'boxapi' + '.dat')
    STORAGE.put(access_token, refresh_token)
    return

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
    redirect_uri = 'http://localhost' #'urn:ietf:wg:oauth:2.0:oob'
    oauth  = authorize_client(client_secret=client_secret, client_id=client_id,redirect_uri=redirect_uri)
    client = Client(oauth)
    return client



def regex_boxapi_ret_fileid(url):
    import re
    regex_boxapi  = re.compile(r'^(https?)?(?:\://)?(.+)\.box\.com/(.+)?(\.?[jpngJPNG]{3,4})?(.*?)?\??(.*?)?$', re.U)
    matches = regex_boxapi.match(url)
    if matches:
        protocol = matches.groups()[0]
        appname  = matches.groups()[1]
        file_id   = {'file_id': matches.groups()[2].split('/')[-1]}
        return file_id
    else:
        pass


        
def download_boxapi_auth_file(client=None, image_url=None, destpath=None, **kwargs):
    if not kwargs.get('file_id'):
        try:
            file_id = qstring2kvpairs(image_url)['id'][0]
        except IndexError:
            file_id = regex_boxapi_ret_fileid(image_url)       
            pass
    else:
        file_id = kwargs.get('file_id').values()
    content = client.file(file_id=file_id).content()
    if not destpath:
        return content
    else:
        with open(destpath,'w') as f:
            f.write(content)
            f.close()
        return destpath
        
        

url = 'https://capturemrg.box.com/s/cy5fuoata8eiq5n53i5gvwphqfvb061x'

file_id = regex_boxapi_ret_fileid(url)

if file_id:
    print file_id
client = instantiate_boxapi_client()

print client.