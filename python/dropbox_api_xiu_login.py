# YOU NEED TO INSERT YOUR APP KEY AND SECRET BELOW!
# Go to dropbox.com/developers/apps to create an app.

def get_login_client():
    import dropbox
    # Get your app key and secret from the Dropbox developer website
    #### SET AUTH VARS ####  
    app_key = 'uvdjq3jebc0i77w'
    app_secret = 'hwm2he4b4kff3ow'
    #app_key = 'cmdxy6bmoqd95h9'
    #app_secret = 'rmm7ecwe8xwrqsy'

    username = 'julia.liao@xiu.com'  
    password = '880703'
    token_str = 'q6WP3pOY0k8AAAAAAAAABdQ4y9ejnypzqCoGxujZfznGySNzvN_7s8lgdgEdIhHt'
    # access_type can be 'app_folder' or 'dropbox', depending on
    # how you registered your app.
    access_type = 'dropbox'

    #### END VARS ####
    flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
    authorize_url = flow.start()
    # print '1. Go to: ' + authorize_url
    # print '2. Click "Allow" (you might have to log in first)'
    # print '3. Copy the authorization code.'
    # code = raw_input("Enter the authorization code here: ").strip()
    # This will fail if the user enters an invalid authorization code
    if private_access_token:
        access_token = private_access_token
    else:
        access_token, user_id = flow.finish(raw_input("Enter the authorization code here: ").strip())

    client = dropbox.client.DropboxClient(access_token)
    print 'linked account: ', client.account_info()
    return client


## Downloadfile from Dropbox to pwd
def get_file_dropbox(client, filename, destdir=None):
    folder_metadata = client.metadata('/')
    if not destdir:
        destdir = '.'
    print 'metadata: ', folder_metadata
    f, metadata = client.get_file_and_metadata('/' + filename.split('/')[-1])
    out = open(os.path.join(destdir, filename.split('/')[-1]), 'wb')
    out.write(f.read())
    out.close()
    print metadata


## Upload File from pwd to Dropbox
def put_file_dropbox(client, filename, destdir=None):
    if not destdir:
        destdir = '/'
    f = open(filename, 'rb')
    response = client.put_file(destdir + filename.split('/')[-1], f)
    print 'uploaded: ', response


def main(filename=None):
    import sys
    if not filename:
        try:
            filename = sys.argv[1]            
            client = get_login_client()
            get_file_dropbox(client, filename, destdir=None)
        except:
            pass
    else:
        print 'No Valid File selected to sync'
        pass

if __name__ == '__main__':
    main()
