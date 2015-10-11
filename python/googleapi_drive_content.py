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
    from googleapi_service import create_googleapi_service

    serviceName = 'drive'
    version = 'v2'
    client_secret = 'dccI63nfXqddT5BZcjcs67lj'
    client_id = '355881409068-167vm2c1oqjkmdmb2kulaugu63ehgcim.apps.googleusercontent.com'
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

    download_file_content(service=service, drive_file=drive_file)
