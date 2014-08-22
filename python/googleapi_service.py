#!/usr/bin/env python
# -*- coding: utf-8 -*-

def create_googleapi_service(serviceName=None, version=None):
    serviceName = ''
    version = ''
    import httplib2
    from oauth2client.file import Storage
    from oauth2client.client import OAuth2WebServerFlow
    from oauth2client import tools
    import os, datetime, argparse, apiclient


    ##########################Vars
    client_id='924881045523-kc7leju7role0too3k4itlo864eprl1u.apps.googleusercontent.com'
    client_secret='rqZxYuy0Cht37rJ0GSZ05YoY'
    user_agent='Python2.7'
    BROWSERdeveloperKey='AIzaSyBHozNPRDnVkdPo_JlP_4TLbNrJIsd3bQ4'
    SERVERdeveloperKey='AIzaSyDe68JsIJK5O5Cqd-tAVGqaSeHqcFCNPh8'

    ##
    # if not serviceName:
    #     serviceName = 'calendar'
    # if not version:
    #     version = 'v3'
    ###########
    ###########
    # The client_id and client_secret are copied from the API Access tab on
    # the Google APIs Console
    FLOW = OAuth2WebServerFlow(
        client_id=client_id,
        client_secret=client_secret,
        scope='https://www.googleapis.com/auth/' + serviceName,
        user_agent=user_agent)
    # If the Credentials don't exist or are invalid, run through the native client
    # flow. The Storage object will ensure that if successful the good
    # Credentials will get written back to a file.
    #py_dir = os.path.dirname(os.path.realpath(__file__))
    py_dir = os.path.dirname(os.path.realpath(os.curdir))
    os.chdir(py_dir)
    #storage_file = os.path.join(os.path.dirname(py_dir), 'calendar.dat')
    storage_file = os.path.join(os.path.dirname(py_dir), serviceName + '.dat')
    STORAGE = Storage(storage_file)
    ##
    #
    # To disable the local server feature, replace with '' in the following line:
    args = '--noauth_local_webserver'
    parser = argparse.ArgumentParser(parents=[tools.argparser])
    FLAGS = parser.parse_args()
    ##
    #
    credentials = STORAGE.get()
    if credentials is None or credentials.invalid == True:
        credentials = tools.run_flow(FLOW, STORAGE, FLAGS)
    ##
    # Create an httplib2.Http object to handle our HTTP requests and authorize it
    # with our good Credentials.
    http = httplib2.Http()
    http = credentials.authorize(http)

    from apiclient.discovery import build
    #client = apiclient.APIClient()
    # Build a service object for interacting with the API.
    service = build(serviceName=serviceName, version=version, http=http)

    return service

if __name__ == '__main__':
    print 
    create_googleapi_service(serviceName=serviceName,version=version)