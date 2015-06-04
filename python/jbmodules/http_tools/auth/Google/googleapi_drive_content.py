#!/usr/bin/env python
# -*- coding: utf-8 -*-

def create_googleapi_service(serviceName=None, version=None, client_id=None,client_secret=None,redirect_uri=None, scope=None):
    import httplib2
    from oauth2client.file import Storage
    from oauth2client.client import OAuth2WebServerFlow
    from oauth2client import tools
    import os, datetime, argparse, apiclient
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; en-US; rv:33.0) Gecko/20100101 Firefox/33.0' ##'Python2.7'

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
        #print credentials, STORAGE, storage_file
        #credentials = tools.run_flow(FLOW, STORAGE, FLAGS)
    ##
    # Create an httplib2.Http object to handle our HTTP requests and authorize it
    # with our good Credentials.
    http = httplib2.Http()
    http = credentials.authorize(http)

    from apiclient import discovery
    #client = apiclient.APIClient()
    # Build a service object for interacting with the API.
    service = discovery.build(serviceName=serviceName, version=version, http=http)
    return service


def download_file_content(service=None, drive_file=None):
    """Download a file's content.

    Args:
    service: Drive API service instance.
    drive_file: Drive File instance.

    Returns:
    File's content if successful, None otherwise.
    """
    download_url = drive_file.get('downloadUrl')
    if download_url:
        resp, content = service._http.request(download_url)
        if resp.status == 200:
            print 'Status: %s' % resp
            return content
        else:
            print 'An error occurred: %s' % resp
            return None
    else:
        # The file doesn't have any content stored on Drive.
        return None


if __name__ == '__main__':
    import apiclient, sys
    #from googleapi_service import create_googleapi_service

    serviceName = 'drive'
    version = 'v2'
    
    ### Uses Bluefly dev creds not personal google acct
    client_secret = 'np60_xlDLHYircCLaxjf9-Y-'
    client_id = '153570890903-c4au43k7jq36mv4vve174tmrkfa2orln.apps.googleusercontent.com'
    ###
    
    scope = 'https://www.googleapis.com/auth/drive'
    #redirect_uri = 'http://localhost:8080/'
    redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'


    service = create_googleapi_service(serviceName=serviceName,
                                        version=version,
                                        client_secret=client_secret,
                                        client_id=client_id,
                                        redirect_uri=redirect_uri,
                                        scope=scope)

    # drive_file = drive_file_instance
    #url = 'https://lh6.googleusercontent.com/OIewDxLKKSkrPbeyzzvnokg5QaQGryNrMwQFV9IoxYZKtop6ow_OQ45bX0lvq1e9SUveGICEK-I=w1154-h561'
    url = 'https://drive.google.com/file/d/0B4p-sxy24gtqb3dLQjZzZUJqSmc/edit?usp=sharing'
    
    folder_link = 'https://drive.google.com/a/bluefly.com/folderview?id=0B0Z4BGpAAp5KfkdSZWw5MGtDUEV5dFNPYXdXcHVhdVFGenplMTRXRVgwRnBvM0NFWllGdU0&usp=sharing'
    #download_file_content(service=service, drive_file='TESTdrive_file')
