#!/usr/bin/env python
# -*- coding: utf-8 -*-

import httplib2
import pprint
from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials
from apiclient.http import MediaFileUpload
from apiclient import errors

def instantiate_google_drive_serviceAccount_bfly():
    # drive_file = drive_file_instance
    import httplib2
    import pprint
    from apiclient.discovery import build
    from oauth2client.client import SignedJwtAssertionCredentials
    from apiclient.http import MediaFileUpload
    serviceName = 'drive'
    version = 'v2'
    client_email = '153570890903-3tl6bkluun2r32smkpgtqdultfrctvg6@developer.gserviceaccount.com'
    client_id = '153570890903-3tl6bkluun2r32smkpgtqdultfrctvg6.apps.googleusercontent.com'
    scope = 'https://www.googleapis.com/auth/drive'

    f = file('/root/drive-photo-bfly-privatekey.p12', 'rb')
    key = f.read()
    f.close()
    credentials = SignedJwtAssertionCredentials(client_email, key, scope=scope)
    http = httplib2.Http()
    http = credentials.authorize(http)
    drive_service = build(serviceName, version, http=http)
    return drive_service


def download_file_drive(file_id=None, destpath=None):
    from os import chdir, path
    import apiclient
    drive_service = instantiate_google_drive_serviceAccount_bfly()
    request = drive_service.files().get_media(fileId=file_id)
    fdest = open(destpath, 'w')
    media_request = apiclient.http.MediaIoBaseDownload(fdest, request)
    while True:
        try:
            download_progress, done = media_request.next_chunk()
        except apiclient.errors.HttpError, error:
            print 'An error occurred: %s' % error
            return media_request
        if download_progress:
            print 'Download Progress: %d%%' % int(download_progress.progress() * 100)
        if done:
            print 'Download Complete', destpath
            return destpath


def upload_file_drive(srcfile):
    drive_service = instantiate_google_drive_serviceAccount_bfly()
    media_body = MediaFileUpload(srcfile, mimetype='image/jpeg', resumable=True)
    body = {
        'title': '{}'.format(srcfile.split('/')[-1]),
        'description': 'Image',
        'mimeType': 'image/jpeg'
    }

    drive_file = drive_service.files().insert(body=body, media_body=media_body).execute()
    pprint.pprint(drive_file)


def create_drive_folder(pardir_fileid):
    drive_service = instantiate_google_drive_serviceAccount_bfly()
    folder_body = {
        "title": pardir_fileid,
        "description": "Images",
        "parents": [{"id": pardir_fileid}],
        "mimeType": "application/vnd.google-apps.folder"
    }


def save_movefile_drive_folder(file_id, pardir_fileid):
    drive_service = instantiate_google_drive_serviceAccount_bfly()
    body = {
          'title': '{}'.format(srcfile.split('/')[-1]),
            'description': 'Image',
            'mimeType': 'image/jpeg',
            "parents": [{
            "kind": "drive#fileLink",
            "id": pardir_fileid
          }]
        }


def print_application_data_folder_metadata(file_id = 'appfolder'):
    service = instantiate_google_drive_serviceAccount_bfly()
    try:
        file = service.files().get(fileId=file_id).execute()
        print 'Id: %s' % file['id']
        print 'Title: %s' % file['title']
    except errors.HttpError, error:
        print 'An error occurred: %s' % error



def insert_file_in_application_data_folder(service, description, mime_type, filename):
    pardir_fileid =  'appfolder'
    media_body = MediaFileUpload(filename, mimetype=mime_type, resumable=True)
    body = {
        'title': '{}'.format(srcfile.split('/')[-1]),
        "description": "Images",
        "parents": [{"id": pardir_fileid}],
        'mimeType': mime_type,
        'parents': [{'id': pardir_fileid}]
    }

    try:
        file = service.files().insert(
            body=body,
            media_body=media_body).execute()
        return file
    except errors.HttpError, error:
        print 'An error occured: %s' % error
        return None


def list_files_current_dir(service):
    req= service.files().list()
    res = req.execute()
    return res


def list_files_in_application_data_folder(service):
    result = []
    page_token = None
    while True:
        try:
            param = {}
            if page_token:
                param['pageToken'] = page_token
            else:
                param['q'] = "'appfolder' in parents"
            files = service.files().list(**param).execute()

            result.extend(files['items'])
            page_token = files.get('nextPageToken')
            if not page_token:
                break
        except errors.HttpError, error:
            print 'An error occurred: %s' % error
            break
    return result


def batch_callback(request_id, response, exception):
    from apiclient.http import BatchHttpRequest
    print "Response for request_id (%s):" % request_id
    print response

    # Potentially log or re-raise exceptions
    if exception:
        raise exception


def batch_upload(service, FILE_ID):
    batch_request = BatchHttpRequest(callback=batch_callback)
    batch_entry_1 = service.permissions().insert(fileId=FILE_ID, body={
      'value': 'johnb@relic7.uk.to',
      'type': 'user',
      'role': 'writer'
    })

    batch_request.add(batch_entry_1, request_id="batch1")

    batch_entry_2 = service.permissions().insert(fileId=FILE_ID, body={
      'value': 'johnb@relic7.uk.to',
      'type': 'group',
      'role': 'reader'
    })

    batch_request.add(batch_entry_2, request_id="batch2")

    batch_request.execute(http)



if __name__ == '__main__':
    import sys
    srcfile = sys.argv[1]
    upload_file_drive(srcfile)
