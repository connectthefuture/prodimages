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
    

def create_boxapi_service(serviceName=None, version=None, client_id=None, client_secret=None,redirect_uri=None, scope=None):
    import httplib2
    from oauth2client.file import Storage
    from oauth2client.client import OAuth2WebServerFlow
    from oauth2client import tools
    import os, datetime, argparse
    client_id = client_id
    client_secret= client_secret  #'rqZxYuy0Cht37rJ0GSZ05YoY'
    scope =  scope
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; en-US; rv:33.0) Gecko/20100101 Firefox/33.0' ##'Python2.7'
    BOXAPIdeveloperToken='585pe1tlJ7s3QsFaSZVW3sGzOIVUaNKq'
    # BOXAPIKey = 'bxccmj5xnkngs8mggxv5ev49zuh80xs9'
    #####################
    #####################
    # The client_id and client_secret are copied from the API Access tab on
    # the Google APIs Console
    FLOW = OAuth2WebServerFlow(
        client_id=client_id,
        client_secret=client_secret,
        scope=scope,
        redirect_uri=redirect_uri,
        user_agent=user_agent)

    # If the Credentials don't exist or are invalid, run through the native client
    # flow. The Storage object will ensure that if successful the good
    # Credentials will get written back to a file.
    py_dir = os.path.dirname(os.path.realpath(__file__))
    #py_dir = os.path.dirname(os.path.realpath(os.curdir))
    print py_dir, ' Pydir'
    os.chdir(py_dir)
    
    # storage_file = os.path.join(os.path.dirname(py_dir), 'calendar.dat')
    storage_file = os.path.join(py_dir, serviceName + '.dat')
    STORAGE = Storage(storage_file)

    # To disable the local server feature, replace with '' in the following line:
    # args = '' #'--noauth_local_webserver'
    # parser = argparse.ArgumentParser(parents=[tools.argparser])
    # FLAGS = parser.parse_args()
    ##
    #
    credentials = STORAGE.get()
    if credentials is None or credentials.invalid == True:
        authorize_url = FLOW.step1_get_authorize_url()
        print 'Go to the following link in your browser: ' + authorize_url
        code = raw_input('Enter verification code: ').strip()
        credentials = FLOW.step2_exchange(code)
        STORAGE.put(credentials)
        print credentials, STORAGE, storage_file
        #credentials = tools.run_flow(FLOW, STORAGE, FLAGS)
    ##
    # Create an httplib2.Http object to handle our HTTP requests and authorize it
    # with our good Credentials.
    http = httplib2.Http()
    http = credentials.authorize(http)

    import buildBoxService as build
    # Build a service object for interacting with the API.
    service = build(serviceName=serviceName, http=http)
    return service



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


## BoxAppGalleryUrl = 'https://app.box.com/services/auth_download_client'

def regex_boxapi_ret_fileid(url):
    import re
    regex_boxapi  = re.compile(r'^(https?)?(?:\://)?(.+)\.box\.com/(.+)?(\.?[jpngJPNG]{3,4})?(.*?)?\??(.*?)?$', re.U)
    matches = regex_boxapi.match(url)
    if matches:
        protocol = matches.groups()[0]
        appname  = matches.groups()[1]
        fileId   = {'file_id': matches.groups()[2].split('/')[-1]}
        return fileId
    else:
        pass

def qstring2kvpairs(url_with_qstring):
    from urlparse import urlparse, parse_qs
    url = url_with_qstring.encode('UTF-8')
    #urlparse(url).query
    qkvpairs = parse_qs(urlparse(url).query)
    return qkvpairs


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
    import sys
    try:
        serviceName = sys.argv[1]
        create_boxapi_service(serviceName=serviceName,
                             client_id=client_id, 
                             client_secret=client_secret, 
                             redirect_uri=redirect_uri, 
                             scope=scope)
    except IndexError:
        pass

