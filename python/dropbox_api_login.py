#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dropbox

# Get your app key and secret from the Dropbox developer website
app_key = 'ikcr68gddbxed1t'
app_secret = 'i4wjfxe0umdvx7c'

private_access_token = 'aFNqVSoDKPEAAAAAAAAMR4wMdhoO3Cs0D6BUjX82-bE7Q689jokjSxLDyvujUEpJ'


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

## Upload File from pwd to Dropbox
f = open('crontab.txt', 'rb')
response = client.put_file('/crontab.txt', f)
print 'uploaded: ', response


## Downloadfile from Dropbox to pwd
folder_metadata = client.metadata('/')
print 'metadata: ', folder_metadata

f, metadata = client.get_file_and_metadata('/crontab.txt')
out = open('crontab.txt', 'wb')
out.write(f.read())
out.close()
print metadata


###########
import flask
@app.route('/')
def home():
    if not 'access_token' in session:
        return redirect(url_for('dropbox_auth_start'))
    return 'Authenticated.'

@app.route('/dropbox-auth-start')
def dropbox_auth_start():
    return redirect(get_auth_flow().start())

@app.route('/dropbox-auth-finish')
def dropbox_auth_finish():
    try:
        access_token, user_id, url_state = get_auth_flow().finish(request.args)
    except:
        abort(400)
    else:
        session['access_token'] = access_token
    return redirect(url_for('home'))

def get_auth_flow():
    redirect_uri = url_for('dropbox_auth_finish', _external=True)
    return DropboxOAuth2Flow(app_key, app_secret, redirect_uri,session, 'dropbox-auth-csrf-token')
        
