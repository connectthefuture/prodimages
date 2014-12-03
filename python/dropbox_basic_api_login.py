#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dropbox

# Get your app key and secret from the Dropbox developer website
#### SET AUTH VARS ####
app_key = 'ikcr68gddbxed1t'
app_secret = 'i4wjfxe0umdvx7c'
private_access_token = 'aFNqVSoDKPEAAAAAAAAMcj7D7el49caS8gBocryRW99VpF-5K6_GRJi6pQZ5Ii2K'

### Optional ###
username = 'john.bragato@bluefly.com'  
password = 'secret'
# access_type can be 'app_folder' or 'dropbox', depending on
# how you registered your app.
## folder name image_sync_api
## app-name image-sync-api
access_type = 'app_folder'  

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

## Upload File from pwd to Dropbox
f = open('/Users/johnb/Desktop/primes.py', 'rb')
response = client.put_file('/primes.py', f)
print 'uploaded: ', response


## Downloadfile from Dropbox to pwd
folder_metadata = client.metadata('/')
print 'metadata: ', folder_metadata

f, metadata = client.get_file_and_metadata('/primes.py')
out = open('/Users/johnb/Desktop/primes.txt', 'wb')
out.write(f.read())
out.close()
print metadata

