#!/usr/bin/env python
# -*- coding: utf-8 -*-

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


def instantiate_boxapi_service():
    #serviceName = 'drive'
    #version = 'v2'
    client_secret = 'g4R1o909fgf1PSsa5mLMDslpAwcbfIQl'
    client_id = 'bxccmj5xnkngs8mggxv5ev49zuh80xs9'
    scope = 'https://app.box.com/services/auth_download_client'
    # box_file = drive_file_instance
    redirect_uri = 'http://localhost' #'urn:ietf:wg:oauth:2.0:oob'
    service = create_boxapi_service(serviceName=serviceName, client_secret=client_secret, client_id=client_id, redirect_uri=redirect_uri, scope=scope)
    return service


## BoxAppGalleryUrl = 'https://app.box.com/services/auth_download_client'

def create_boxapi_client(oauth=None):
    from boxsdk import Client
    oauth = instantiate_boxapi_service()
    client = Client(oauth)
    return client


def qstring2kvpairs(url_with_qstring):
    from urlparse import urlparse, parse_qs
    url = url_with_qstring.encode('UTF-8')
    #urlparse(url).query
    qkvpairs = parse_qs(urlparse(url).query)
    return qkvpairs


def download_boxapi_auth_file(client=None, image_url=None, destpath=None):
    file_id = qstring2kvpairs(image_url)['id'][0]
    content = client.file(file_id=file_id).content()
    if not destpath:
        return content
    else:
        with open(destpath,'w') as f:
            f.write(content)
            f.close()
        return destpath


def store_tokens():
    from boxsdk import OAuth2
    oauth = OAuth2(
        client_secret='g4R1o909fgf1PSsa5mLMDslpAwcbfIQl',
        client_id = 'bxccmj5xnkngs8mggxv5ev49zuh80xs9',
        store_tokens=instantiate_boxapi_service,
    )
    auth_url, csrf_token = oauth.get_authorization_url('http://localhost')


if __name__ == '__main__':
    import sys
    try:
        serviceName = sys.argv[1]
        create_boxapi_service(serviceName=serviceName,
                             client_id=client_id, 
                             client_secret=client_secret, 
                             redirect_uri=redirect_uri, 
                             scope=scope)
    except:
        pass
