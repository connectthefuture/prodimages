#!/usr/bin/env python
# -*- coding: utf-8 -*-

def download_file_content(service=None, drive_file=None):
    """Download a file's content.

    Args:
    service: Drive API service instance.
    drive_file: Drive File instance.

    Returns:
    File's content if successful, None otherwise.
    """
    import requests
    drive_file_mdata_url = drive_file
    download_url = requests.get(drive_file_mdata_url).url
    #download_url = download_url.split()[0]['downloadUrl']
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


def download_gdrive_file(service=None, image_url=None, destpath=None):
    """Download a Drive file's content to the local filesystem.

      Args:
    service: Drive API Service instance.
    image_url: ID of the Drive file that will downloaded.
    destpath: io.Base or file object, the stream that the Drive file's
    contents will be written to.
      """
    from os import chdir, path
    from apiclient import http, errors
        
    pdir = path.dirname(path.realpath('__file__'))
    ## TODO: Fix this conditional workaround to python dir for import
    if not service:
        chdir(pdir)
        try:
            chdir('python')
        except:
            pass
        from googleapi_service import instantiate_google_drive_service
        service = instantiate_google_drive_service()
    else:
        pass
    
    request = service.files().get_media(fileId=image_url)
    fdest = open(destpath, 'wb+')
    media_request = http.MediaIoBaseDownload(fdest, request)
    while True:
        try:
            download_progress, done = media_request.next_chunk()
        except errors.HttpError, error:
            print 'An error occurred: %s' % error
            return
        if download_progress:
            print 'Download Progress: %d%%' % int(download_progress.progress() * 100)
        if done:
            print 'Download Complete', destpath
            return destpath


def download_google_drive_file(service=None, image_url=None, destpath=None):
    """Download a Drive file's content to the local filesystem.
    Args:
    service: Drive API Service instance.
    fileId/image_url: ID of the Drive file that will downloaded.
    destpath: io.Base or file object, the stream that the Drive file's
        contents will be written to.
    """
    from apiclient import http, errors
    from os import chdir, path
    import requests
    pdir = path.dirname(path.realpath('__file__'))
    ## TODO: Fix this conditional workaround to python dir for import
    if not service:
        chdir(pdir)
        try:
            chdir('python')
        except:
            pass
        from googleapi_service import instantiate_google_drive_service
        service = instantiate_google_drive_service()
    else:
        pass

    #request = service.files().get_media(fileId=image_url)
    #media_request = http.MediaIoBaseDownload(destpath, request)

#    file_content = download_file_content(service=service, drive_file=image_url)
#    if file_content:
#        with open(destpath, 'wb+') as f:
#            f.write(file_content)
#            f.close()
#            print 'WROTE ', destpath
#        return destpath

    while True:
        try:
            #download_progress, done = media_request.next_chunk()
            resp, content = service._http.request(image_url)
        except errors.HttpError, error:
            print 'An error occurred: %s' % error
            return
        #if download_progress:
        #    print 'Download Progress: %d%%' % int(download_progress.progress() * 100) 
        #print resp.get('content-location')  
        if resp.status == 200:
            download_url = resp.get('content-location')  ##resp.get('downloadUrl')
            print download_url
            file_content = requests.get(download_url,allow_redirects=True,timeout=5)
        if file_content:
            print 'Download Complete'
            with open(destpath, 'wb+') as f:
                f.write(file_content.content)
                f.close()
            print content
            return destpath


if __name__ == '__main__':
    import sys
    try:
        #image_url = 'https://drive.google.com/open?id=0B6gg_FhatSi8cWF4RVFhMEtiRm8&authuser=0'
        image_url = sys.argv[1]
        #destpath  = '/Users/johnb/Desktop/pix/testfile.jpg' 
        destpath = sys.argv[2]
        res = download_file(image_url=image_url, destpath=destpath)
    except IndexError:
        print 'Failed, please supply both the image_url and destpath args as sys.argv[1] and [2], respectively'
    
