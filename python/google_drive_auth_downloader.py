#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import sys
#sys.argv[1:] = ''
# def create_googleDriveapi_service2(serviceName=None, version=None, client_id=None,client_secret=None,redirect_uri=None, scope=None):
#     import httplib2
#     from oauth2client.file import Storage
#     from oauth2client.client import OAuth2WebServerFlow
#     from oauth2client import tools
#     import os, datetime, argparse, apiclient
#     from apiclient import http, errors
#     # if serviceName == 'drive':
#     #     print serviceName
#     #     client_id = '390426411557-fsk0n5k1g5fnj1gs1te2f19kq5vfftgk.apps.googleusercontent.com'
#     # ##########################Vars
#     # elif serviceName == 'calendar':
#     #     print serviceName
#     #     client_id = '924881045523-kc7leju7role0too3k4itlo864eprl1u.apps.googleusercontent.com'
    
#     client_id = client_id
#     client_secret= client_secret  #'rqZxYuy0Cht37rJ0GSZ05YoY'
#     scope =  scope
#     user_agent =  'Python2.7'
#     BROWSERdeveloperKey='AIzaSyBHozNPRDnVkdPo_JlP_4TLbNrJIsd3bQ4'
#     SERVERdeveloperKey='AIzaSyDe68JsIJK5O5Cqd-tAVGqaSeHqcFCNPh8'
#     ##
#     # if not serviceName:
#     #     serviceName = 'calendar'
#     # if not version:
#     #     version = 'v3'
#     ###########
#     ###########
#     # The client_id and client_secret are copied from the API Access tab on
#     # the Google APIs Console
#     FLOW = OAuth2WebServerFlow(
#         client_id=client_id,
#         client_secret=client_secret,
#         scope=scope,
#         redirect_uri=redirect_uri,
#         user_agent=user_agent,)
#     #        approval_prompt='force')

#     # If the Credentials don't exist or are invalid, run through the native client
#     # flow. The Storage object will ensure that if successful the good
#     # Credentials will get written back to a file.
#     py_dir = os.path.dirname(os.path.realpath(__file__))
#     #py_dir = os.path.dirname(os.path.realpath(os.curdir))
#     print py_dir
#     os.chdir(py_dir)
    
#     #storage_file = os.path.join(os.path.dirname(py_dir), 'calendar.dat')
#     storage_file = os.path.join(py_dir, serviceName + '.dat')
#     STORAGE = Storage(storage_file)

#     # To disable the local server feature, replace with '' in the following line:
#     args = '' #'--noauth_local_webserver'
#     parser = argparse.ArgumentParser(parents=[tools.argparser])
#     FLAGS = parser.parse_args()
#     ##
#     #
#     credentials = STORAGE.get()
#     if credentials is None or credentials.invalid == True:
#         authorize_url = FLOW.step1_get_authorize_url()
#         print 'Go to the following link in your browser: ' + authorize_url
#         code = raw_input('Enter verification code: ').strip()
#         credentials = FLOW.step2_exchange(code)
#         STORAGE.put(credentials)
#         print credentials, STORAGE, storage_file
#         #credentials = tools.run_flow(FLOW, STORAGE, FLAGS)
#     ##
#     # Create an httplib2.Http object to handle our HTTP requests and authorize it
#     # with our good Credentials.
#     http = httplib2.Http()
#     http = credentials.authorize(http)

#     from apiclient.discovery import build
#     #client = apiclient.APIClient()
#     # Build a service object for interacting with the API.
#     service = build(serviceName=serviceName, version=version, http=http)
#     print STORAGE._filename
#     return service


# def instantiate_google_drive_service2():
#     #import apiclient, sys
#     #from googleapi_service import create_googleapi_service
#     serviceName = 'drive'
#     version = 'v2'
#     client_secret = 'dccI63nfXqddT5BZcjcs67lj'
#     client_id = '355881409068-167vm2c1oqjkmdmb2kulaugu63ehgcim.apps.googleusercontent.com'
#     scope = 'https://www.googleapis.com/auth/drive'
#     # drive_file = drive_file_instance
#     redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
#     service = create_googleDriveapi_service(serviceName=serviceName, version=version, client_secret=client_secret, client_id=client_id, redirect_uri=redirect_uri, scope=scope)
#     return service

download_file_content(service=None, drive_file=None)

def download_google_drive_file(service=None, image_url=None, destpath=None):
    """Download a Drive file's content to the local filesystem.
    Args:
    service: Drive API Service instance.
    fileId: ID of the Drive file that will downloaded.
    destpath: io.Base or file object, the stream that the Drive file's
        contents will be written to.
    """
    from apiclient import http, errors
    if not service:
        from googleapi_service import instantiate_google_drive_service
        service       = instantiate_google_drive_service()
    else:
        pass
    
    from googleapi_drive_content import download_file_content
    
    request       = service.files().get_media(fileId=image_url)
    media_request = http.MediaIoBaseDownload(destpath, request)
    
    file_content  = download_file_content(service=service, drive_file=image_url)
    if file_content:
        return file_content

    while True:
        try:
            download_progress, done = media_request.next_chunk()
        except errors.HttpError, error:
            print 'An error occurred: %s' % error
            return
        if download_progress:
            print 'Download Progress: %d%%' % int(download_progress.progress() * 100)
        if done:
            print 'Download Complete'
            return destpath


if __name__ == '__main__':
    import sys
    try:
        image_url = sys.argv[1]
        destpath  = sys.argv[2]
        res = download_google_drive_file(image_url=image_url, destpath=destpath)
    except IndexError:
        print 'Failed, please supply both the image_url and destpath args as sys.argv[1] and [2], respectively'

