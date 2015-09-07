#!/usr/bin/env python
# -*- coding: utf-8 -*-

def qstring2kvpairs(url_with_qstring):
    from urlparse import urlparse, parse_qs
    url = url_with_qstring.encode('UTF-8')
    urlparse(url).query
    qkvpairs = parse_qs(urlparse(url).query)
    return qkvpairs


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


def download_boxapi_drive_file(service=None, image_url=None, destpath=None):
    """Download a Box file's content to the local filesystem.
      Args:

    service: Drive API Service instance.
    image_url/fileId: ID of the Drive file that will downloaded.
    destpath: io.Base or file object, the stream that the Drive file's
    contents will be written to.
      """
    from os import chdir, path
    from apiclient import http, errors
    import StringIO
    pdir = path.abspath('/usr/local/batchRunScripts/python/jbmodules/image_processing/marketplace') #path.dirname(path.realpath('__file__'))
    ## TODO: Fix this conditional workaround to python dir for import
    if not service:
        chdir(pdir)
        try:
            chdir('python')
        except:
            pass
        from boxapi_service import instantiate_boxapi_service
        service = instantiate_boxapi_service()
    else:
        pass
    
    file_id = qstring2kvpairs(image_url)['id'][0]
    request = service.files().get_media(fileId=file_id)
    fdest = open(destpath, 'w')
    media_request = http.MediaIoBaseDownload(fdest, request)
    while True:
        try:
            download_progress, done = media_request.next_chunk()
        except errors.HttpError, error:
            print 'An error occurred: %s' % error
            return media_request
        if download_progress:
            print 'Download Progress: %d%%' % int(download_progress.progress() * 100)
        if done:
            print 'Download Complete', destpath
            return destpath


if __name__ == '__main__':
    import sys
    try:
        #image_url = 'https://drive.boxapi.com/open?id=0B6gg_FhatSi8cWF4RVFhMEtiRm8&authuser=0'
        image_url = sys.argv[1]
        #destpath  = '/Users/johnb/Desktop/pix/testfile.jpg' 
        destpath = sys.argv[2]
        #res = download_boxapi_drive_file(image_url=image_url, destpath=destpath)
        #print res._total_size, res._uri, res._fd, res._request, res._rand
    except IndexError:
        print 'Failed, please supply both the image_url and destpath args as sys.argv[1] and [2], respectively'
    
