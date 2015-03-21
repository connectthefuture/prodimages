#!/usr/bin/env python
# -*- coding: utf-8 -*-

def download_google_drive_file(service=None, image_url=None, destpath=None):
    """Download a Drive file's content to the local filesystem.
    Args:
    service: Drive API Service instance.
    fileId/image_url: ID of the Drive file that will downloaded.
    destpath: io.Base or file object, the stream that the Drive file's
        contents will be written to.
    """
    from apiclient import http, errors
    if not service:
        from googleapi_service import instantiate_google_drive_service
        service = instantiate_google_drive_service()
    else:
        pass
    
    from googleapi_drive_content import download_file_content
    
    request       = service.files().get_media(fileId=image_url)
    media_request = http.MediaIoBaseDownload(destpath, request)
    
    file_content  = download_file_content(service=service, drive_file=image_url)
    if file_content:
        with open(destpath, 'wb+') as f:
            f.write(file_content)
            f.close()
            print 'WROTE ', destpath
        return destpath

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

