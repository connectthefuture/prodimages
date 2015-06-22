#!/usr/bin/env python
# -*- coding: utf-8 -*-

import httplib2
import pprint
from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials
from apiclient.http import MediaFileUpload


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


if __name__ == '__main__':
    import sys
    srcfile = sys.argv[1]
    upload_file_drive(srcfile)
