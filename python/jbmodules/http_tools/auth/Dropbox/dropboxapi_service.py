#!/usr/bin/env python
#-*- coding: utf-8 -*-


def dropbox_client(access_token=None):
    # Include the Dropbox SDK
    import dropbox

    if not access_token:
        # Get your app key and secret from the Dropbox developer website
        ## app name = x-auth-downloader
        app_key = '5k7jk61r2pacz47'
        app_secret = 'ijf1l9aju0l63rm'

        flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

        # Have the user sign in and authorize this token
        authorize_url = flow.start()
        print '1. Go to: ' + authorize_url
        print '2. Click "Allow" (you might have to log in first)'
        print '3. Copy the authorization code.'
        code = raw_input("Enter the authorization code here: ").strip()

        # This will fail if the user enters an invalid authorization code
        access_token, user_id = flow.finish(code)

    client = dropbox.client.DropboxClient(access_token)
    print 'linked account: ', client.account_info()
    return client


def download_auth_file(client=None, access_token=None, image_url=None, destpath=None):
    if not client:
        access_token = 'Do3NA68T2qgAAAAAAACjyFme5rJ5hzhE2izh3JPA-d-Mmi7foHhrV_DH1jg3xVoL'
        client = dropbox_client(access_token=access_token)
    folder_metadata = client.metadata(image_url)
    print 'metadata: ', folder_metadata

    f, metadata = client.get_file_and_metadata(image_url)
    outfile = open(destpath, 'wb')
    outfile.write(f.read())
    outfile.close()
    print metadata
    return destpath


if __name__ == '__main__':
    download_auth_file()
