import httplib2
import pprint
from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials
from apiclient.http import MediaFileUpload



def create_googleapi_service(serviceName=None, version=None, client_id=None,client_secret=None,redirect_uri=None, scope=None):
    import httplib2
    from oauth2client.file import Storage
    from oauth2client.client import OAuth2WebServerFlow
    from oauth2client import tools
    import os, datetime, argparse, apiclient
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; en-US; rv:33.0) Gecko/20100101 Firefox/33.0' ##'Python2.7'
    BROWSERdeveloperKey='AIzaSyBHozNPRDnVkdPo_JlP_4TLbNrJIsd3bQ4'
    SERVERdeveloperKey='AIzaSyDe68JsIJK5O5Cqd-tAVGqaSeHqcFCNPh8'
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

    from apiclient import discovery
    #client = apiclient.APIClient()
    # Build a service object for interacting with the API.
    service = discovery.build(serviceName=serviceName, version=version, http=http)
    return service


def instantiate_google_drive_service_bfly():
    serviceName = 'drive'
    version = 'v2'
    client_secret = 'np60_xlDLHYircCLaxjf9-Y-'
    client_id = '153570890903-c4au43k7jq36mv4vve174tmrkfa2orln.apps.googleusercontent.com'
    scope = 'https://www.googleapis.com/auth/drive'
    # drive_file = drive_file_instance
    redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
    service = create_googleapi_service(serviceName=serviceName, version=version, client_secret=client_secret, client_id=client_id, redirect_uri=redirect_uri, scope=scope)
    return service


def upload_file_drive(srcfile):
    drive_service = instantiate_google_drive_service()

    media_body = MediaFileUpload(srcfile, mimetype='image/jpeg', resumable=True)
    body = {
        'title': '{}'.format(srcfile.split('/')[-1]),
        'description': 'Image',
        'mimeType': 'image/jpeg'
    }

    drive_file = drive_service.files().insert(body=body, media_body=media_body).execute()
    pprint.pprint(drive_file)


if __name__ == '__main__':
    import sys
    srcfile = sys.argv[1]
    upload_file_drive(srcfile)

