#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'johnb'


from googleapiclient import errors, http
ProductionRoot  = '0B0Z4BGpAAp5KfmJQUjFlSjlPVTFUcGo1eWpVRDhmekdzLVVsWUYyM1BBZGhHUGRTTVpUU1E'
MarketplaceRoot = '0B0Z4BGpAAp5Kfm5UOWk3WFd2b1ZIVzNMbDliUVNsS2tHOVJXc0loRERDMDRzQmkzV0JRaHM'
EditorialShare  = '0B0Z4BGpAAp5KfnRZaWl4cHMxUGg4MGI0LUFjUWFDdzQ4VWsyTi11OGJPQVlRakRKSXNScHM'
VendorShare     = '0B0Z4BGpAAp5KfmJQUjFlSjlPVTFUcGo1eWpVRDhmekdzLVVsWUYyM1BBZGhHUGRTTVpUU1E'
LookletImages   = '0B0Z4BGpAAp5KfkpZeENQamp0UWpZaWtEWHJGd0xMa3dGV01acG1ESENqRzRfaW5od2JjV1U'
StillImages     = '0B0Z4BGpAAp5KfmxtRktkUGhLckdLSXE0bzA2azhMUW1yVFd6R2VlUUxMN0lsY0NZUDdBaTg'
VendorImages    = '0B0Z4BGpAAp5Kfm5UOWk3WFd2b1ZIVzNMbDliUVNsS2tHOVJXc0loRERDMDRzQmkzV0JRaHM'

from googleapiclient import errors, http
ProductionRoot  = '0B0Z4BGpAAp5KfmJQUjFlSjlPVTFUcGo1eWpVRDhmekdzLVVsWUYyM1BBZGhHUGRTTVpUU1E'
MarketplaceRoot = '0B0Z4BGpAAp5Kfm5UOWk3WFd2b1ZIVzNMbDliUVNsS2tHOVJXc0loRERDMDRzQmkzV0JRaHM'
EditorialShare  = '0B0Z4BGpAAp5KfnRZaWl4cHMxUGg4MGI0LUFjUWFDdzQ4VWsyTi11OGJPQVlRakRKSXNScHM'
VendorShare     = '0B0Z4BGpAAp5KfmJQUjFlSjlPVTFUcGo1eWpVRDhmekdzLVVsWUYyM1BBZGhHUGRTTVpUU1E'
LookletImages   = '0B0Z4BGpAAp5KfkpZeENQamp0UWpZaWtEWHJGd0xMa3dGV01acG1ESENqRzRfaW5od2JjV1U'
StillImages     = '0B0Z4BGpAAp5KfmxtRktkUGhLckdLSXE0bzA2azhMUW1yVFd6R2VlUUxMN0lsY0NZUDdBaTg'
VendorImages    = '0B0Z4BGpAAp5Kfm5UOWk3WFd2b1ZIVzNMbDliUVNsS2tHOVJXc0loRERDMDRzQmkzV0JRaHM'

from googleapiclient import http,errors
class GoogleDriveClient:
    def __init__(self, file_id='', local_filepath='', description='', title='', scope='', role='', kind = '', database_id='', prop_key='', prop_value= '', parent_id='', q=''): 
        self.rootdirid = "0AA7omFHcbQaiUk9PVA"
        if not file_id:
            self.file_id = self.rootdirid
        else:
            self.file_id = file_id
        if not parent_id:
            self.parent_id = self.rootdirid
        else:
            self.parent_id = parent_id
        self.parents = [self.parent_id]
        self.local_filepath = local_filepath

        if not title:
            try:
                self.title = '{}'.format(self.local_filepath.split('/')[-1].split('.')[0])
            except IndexError:
                self.title = ''
        else:
            self.title = title
        self.mime_type = 'image/jpeg'
        self.description = description
        #self.pardir_fileid = ''
        self.kinds = ["drive#file", "drive#fileList", "drive#fileLink", "drive#parentReference", "drive#user", "drive#permission", "drive#comment", "drive#commentReply"]
        self.roles = ['reader', 'writer', 'owner', 'commenter']
        if not kind:
            self.kind = self.kinds[0]
        else:
            self.kind = kind
        if not role:
            self.role = self.roles[0]
        else:
            self.role = role
        
        self.rest_scopes = [ 
                            'https://www.googleapis.com/auth/drive',
                            'https://www.googleapis.com/auth/drive.readonly',
                            'https://www.googleapis.com/auth/drive.file',
                            'https://www.googleapis.com/auth/drive.appdata',
                            'https://www.googleapis.com/auth/drive.metadata',
                            'https://www.googleapis.com/auth/drive.metadata.readonly',
                            'https://www.googleapis.com/drive/v2/files',
                            'https://www.googleapis.com/upload/drive/v2/files'
                            ]
        if not scope:
            self.scope    = 'https://www.googleapis.com/auth/drive.file'
        else:
            self.scope = scope
                
        self.perm_types = ['user', 'group', 'domain', 'anyone']
        self.prop_key = prop_key
        self.prop_value = prop_value
        self.visibility = 'Public'
        self.q = q
        ### Properties
        if not prop_key and not prop_value:
            self.properties = [{
               'key': 'databaseId',
               'value': database_id,
               'visibility': self.visibility
            }]
        elif prop_key and prop_value:
            #self.properties = properties
            self.prop_key = prop_key
            self.prop_value = prop_value
            self.properties = [{
               'key': self.prop_key,
               'value': self.prop_value,
               'visibility': self.visibility
            }]
        self.service = self.instantiate_google_drive_serviceAccount_bfly()


    ### OK ###
    def instantiate_google_drive_serviceAccount_bfly(self):
        import httplib2
        from googleapiclient.discovery import build
        from oauth2client.client import SignedJwtAssertionCredentials
        serviceName = 'drive'
        version = 'v2'
        client_email = '153570890903-3tl6bkluun2r32smkpgtqdultfrctvg6@developer.gserviceaccount.com'
        client_id = '153570890903-3tl6bkluun2r32smkpgtqdultfrctvg6.apps.googleusercontent.com'
        scope = 'https://www.googleapis.com/auth/drive'
        # filescope='https://www.googleapis.com/auth/drive.file'
        # metadatascope='https://www.googleapis.com/auth/drive.metadata'
        f = file('/root/drive-photo-bfly-privatekey.p12', 'rb')
        key = f.read()
        f.close()
        credentials = SignedJwtAssertionCredentials(client_email, key, scope=scope)
        _http = httplib2.Http()
        _http = credentials.authorize(_http)
        self.service = build(serviceName, version, http=_http)
        return self.service


    ## OK ##
    ## File and Folder Ops
    def download_file_drive(self):
        request = self.service.files().get_media(fileId=self.file_id)
        fdest = open(self.local_filepath, 'w')
        _file_content = http.MediaIoBaseDownload(fdest, request)
        while True:
            try:
                download_progress, done = _file_content.next_chunk()
            except errors.HttpError, error:
                print 'An error occurred: %s' % error
                return _file_content
            if download_progress:
                print 'Download Progress: %d%%' % int(download_progress.progress() * 100)
            if done:
                print 'Download Complete', self.local_filepath
                return self.local_filepath

    ## OK ##
    def upload_file_drive(self):
        import pprint
        media_body = http.MediaFileUpload(self.local_filepath, mimetype=self.mime_type , resumable=True)
        body = {
            'title': self.title,
            'description': self.description,
            'mimeType': self.mime_type,
            'properties': self.properties
        }
        if self.parent_id:
            body['parents'] = [{'id': self.parent_id}]

        _uploaded_file_data = self.service.files().insert(body=body, media_body=media_body).execute()
        pprint.pprint(_uploaded_file_data)
        return _uploaded_file_data



    def rename_drive_file(self):
        try:
            _file = {'title': self.title}
            # Rename the file.
            _updated_file = self.service.files().patch(fileId=self.file_id, body=_file, fields='title').execute()
            return _updated_file
        except errors.HttpError, error:
            print 'An error occurred: %s' % error
            return None

    def create_drive_folder(self):
        body = {
            'title': self.title,
            'description': self.description,
            'mimeType': 'application/vnd.google-apps.folder',
            #'folderColorRgb': self.folder_color_rgb,
            #'userPermission': self.user_permission
        }
        if self.parent_id:
            body['parents'] = [{'id': self.parent_id}]

        _new_folder_data = self.service.files().insert(body=body).execute()['items'][0].items()
        return _new_folder_data

    ## Add-Edit Additional Custom File Properties
    def insert_property(self):
        body = self.properties[0]
        try:
            p = self.service.properties().insert(fileId=self.file_id, body=body).execute()
            return p
        except errors.HttpError, error:
            print 'An error occurred: %s' % error
        return None

    def update_property(self):
        try:
            # First retrieve the property from the API.
            _prop = self.service.properties().get(fileId=self.file_id, propertyKey=self.prop_key,
                                                  visibility=self.visibility).execute()
            _prop['value'] = self.prop_value
            return self.service.properties().update(fileId=self.file_id, propertyKey=self.prop_key,
                                                    visibility=self.visibility, body=_prop).execute()
        except errors.HttpError, error:
            print 'An error occurred: %s' % error
        return None

    ### OK ###
    ## List Contents of Dirs
    def list_filesdata_current_dir(self):
        req = self.service.files().list()
        _folder_data = req.execute()
        return _folder_data

    ### OK ###
    def list_ret_IDs_indir(self):
        body = {}
        if self.parent_id:
            body['parents'] = [{'id': self.parent_id}]

        results = self.service.files().list(maxResults=20).execute()
        items = results.get('items', [])
        if not items:
            print 'No files found.'
        else:
            print 'Files:'
            infodict = {}
            for item in items:
                baseinfo = {}
                print '{0} --{1}-- ({2}) --{3}'.format(item['title'], item['mimeType'], item['id'], item['parents'])
                baseinfo['id'] = item['id']
                # baseinfo['title'] = item['fileId']
                baseinfo['title'] = item['title']
                baseinfo['mimeType'] = item['mimeType']
                baseinfo['parents'] = item['parents']
                # baseinfo['title'] = item['fileExtension']
                baseinfo['selfLink'] = item['selfLink']
                baseinfo['alternateLink'] = item['alternateLink']
                #baseinfo['thumbnailLink'] = item['thumbnailLink']
                infodict[item['id']] = baseinfo
            return infodict
    
    ## Shortcut to File
    def create_file_shortcut(self):
        body = {
            'title': self.title,
            'description': self.description,
            'mimeType': 'application/vnd.google-apps.drive-sdk'
        }
        if self.parent_id:
            body['parents'] = [{'id': self.parent_id}]

        _file = self.service.files().insert(body=body).execute()
        print 'File ID: %s' % _file['id']
        return _file


    ## Shared Folder    
    ### OK ###
    def create_public_folder(self):
        body = {
            'title': self.title,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        if self.parent_id:
            body['parents'] = [{'id': self.parent_id}]
        _public_folder = self.service.files().insert(body=body).execute()
        permission = {
            'value': '',
            'type': 'anyone',
            'role': 'reader'
        }
        self.service.permissions().insert(fileId=_public_folder['id'], body=permission).execute()
        #self.pardir_fileid = _public_folder['id']
        #return self.pardir_fileid
        return _public_folder['id']



    # def list_fileitems_current_dir(self):
    #     items = self.drive_folder_data['items'][0].items()
    #     [ self.drive_folder_files.extend(i) for i in items if i ]
    #     return self.drive_folder_files
    
    def find_retrieve_all_files(self):
        _drive_folder_files = []
        page_token = None
        while True:
            try:
                params = {}
                if page_token:
                    params['pageToken'] = page_token
                params['q'] = "properties has \{key={0} and value={1} and visibility={2}\}".format(self.prop_key ,self.prop_value, self.visibility)
                _files = self.service.files().list(**params).execute()
                _drive_folder_files.append(_files['items'])
                page_token = _files.get('nextPageToken')
                if not page_token:
                    break
            except errors.HttpError, error:
                print 'An error occurred: %s' % error
                break
        return _drive_folder_files

    #.parents().get(fileId=file_id, parentId=folder_id).execute()
    ### OK ###
    def print_ret_files_in_folder(self):            
        page_token = None
        while True:
            try:
                params = {}
                if page_token:
                    params['pageToken'] = page_token
                children = self.service.children().list(folderId=self.parent_id, **params).execute()
                childrens = {}
                for child in children.get('items', []):
                    try:
                        childrens[child['id']] = child['title']
                        print 'File Id: %s' % child['id']
                    except KeyError:
                        pass
                page_token = children.get('nextPageToken')
                if not page_token:
                    return childrens
                    break
            except errors.HttpError, error:
                print 'An error occurred: %s' % error
                break



### PubSub Push Notifications Client
class GooglePubSubClient:
    def __init__(self, project_name=None, topic_name=None):
        from oauth2client import client as oauth2client
        self.PUBSUB_SCOPES = ['https://www.googleapis.com/auth/pubsub']
        self.oauth2client = oauth2client
        self.service = self.instantiate_pubsub_client()
        self.project_name = project_name
        self.topic_name = topic_name

    def instantiate_pubsub_client(self,httpobj=None):
        import httplib2
        from apiclient import discovery
        credentials = self.oauth2client.GoogleCredentials.get_application_default()
        if credentials.create_scoped_required():
            credentials = credentials.create_scoped(self.PUBSUB_SCOPES)
        if not httpobj:
            httpobj = httplib2.Http()
        credentials.authorize(httpobj)
        return discovery.build('pubsub', 'v1beta2', http=httpobj)

    def create_pubsub_subscription(self):
        # Only needed if you are using push delivery
        #push_endpoint = 'https://someproject.appspot.com/myhandler'
        # Create a POST body for the Pub/Sub request
        if not self.project_name:
            self.project_name = 'default'
        body = {
            # The name of the topic from which this subscription receives messages
            'topic': 'projects/{0}/topics/{1}'.format(self.project_name, self.topic_name)
            # Only needed if you are using push delivery
            # 'pushConfig': {
            #     'pushEndpoint': push_endpoint
            # }
        }
        _subscription = self.service.projects().subscriptions().create(name='projects/{0}/subscriptions/{1}'.format(self.project_name, self.topic_name), body=body).execute()
        print 'Created: %s' % _subscription.get('name')
        return _subscription

    def get_subscriptions_list(self):
        next_page_token = None
        _subscriptions = []
        while True:
            resp = self.service.projects().subscriptions().list(
                project='projects/{}'.format(self.project_name),
                pageToken=next_page_token).execute()
            # Process each subscription
            for subscription in resp['subscriptions']:
                print subscription['name']
                _subscriptions.append(subscription)
            next_page_token = resp.get('nextPageToken')
            if not next_page_token:
                #break
                return _subscriptions

    def pull_acknowledge_msg(self):
        import base64
        # You can fetch multiple messages with a single API call.
        batch_size = 100
        _subscription = 'projects/{0}/subscriptions/{1}'.format(self.project_name, self.topic_name)
        # Create a POST body for the Pub/Sub request
        body = {
            # Setting ReturnImmediately to false instructs the API to wait
            # to collect the message up to the size of MaxEvents, or until
            # the timeout.
            'returnImmediately': False,
            'maxMessages': batch_size,
        }

        msg_data = []
        while True:
            resp = self.service.projects().subscriptions().pull(subscription=_subscription,
                                                               body=body).execute(num_retries=3)
            received_messages = resp.get('receivedMessages')
            if received_messages is not None:
                ack_ids = []
                for received_message in received_messages:
                    pubsub_message = received_message.get('message')
                    if pubsub_message:
                        # Process messages
                        msg_data.append(base64.b64decode(str(pubsub_message.get('data'))))
                        # Get the message's ack ID
                        ack_ids.append(received_message.get('ackId'))

                # Create a POST body for the acknowledge request
                ack_body = {'ackIds': ack_ids}

                # Acknowledge the message.
                self.service.projects().subscriptions().acknowledge( subscription=_subscription, body=ack_body).execute()
                return msg_data, ack_ids



import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
class GoogleGmailClient:  
    def __init__(self,user_id='me', to=None, subject='Automated', message_text=None, localdir=None, filename=None):
        self.user_id = user_id
        if to is not None:
            self.to = to
        else:
            self.to = 'john.bragato@gmail.com, john.bragato@bluefly.com'
        self.subject = subject
        self.message_text  = message_text
        self.localdir = localdir
        self.filename = filename
        self.scopes = [ 'https://mail.google.com/',
                        'https://www.googleapis.com/auth/gmail.modify',
                        'https://www.googleapis.com/auth/gmail.readonly',
                        'https://www.googleapis.com/auth/gmail.compose' ]
        self.service = self.instantiate_gmail_serviceAccount_bfly()
        self.message = self.create_message()

    def instantiate_gmail_serviceAccount_bfly(self):
        import httplib2
        from googleapiclient.discovery import build
        from oauth2client.client import SignedJwtAssertionCredentials
        serviceName = 'gmail'
        version = 'v1'
        api_key = 'AIzaSyD09iZ54he2CKlayiBmw9zvkVt7Z6HbSY4'
        client_email = '442933852469-mibsk7qkepe62njis1rv6gi1em0v011k@developer.gserviceaccount.com'
        client_id = '442933852469-mibsk7qkepe62njis1rv6gi1em0v011k.apps.googleusercontent.com'
        scope = self.scopes[0] #'https://www.googleapis.com/auth/gmail.modify'
        f = file('/root/bfly-gmail-privatekey.p12','rb')
        key = f.read()
        f.close()
        credentials = SignedJwtAssertionCredentials(client_email, key, scope=scope)
        _http = httplib2.Http()
        _http = credentials.authorize(_http)
        self.service = build(serviceName, version, http=_http)
        return self.service


    def send_message(self):
        """Send an email message.
        Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        message: Message to be sent.

        Returns:
        Sent Message.
        """
        try:
            _message = (self.service.users().messages().send(userId=self.user_id, body=self.message).execute())
            print 'Message Id: %s' % _message['id']
            return _message
        except errors.HttpError, error:
            print 'An error occurred: %s' % error


    def create_draft(self):
        """Create and insert a draft email. Print the returned draft's message and id.
        Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        self.message: The body of the email message, including headers.

        Returns:
        Draft object, including draft id and message meta data.
        """

        try:
            _message = {'message': self.message}
            draft = service.users().drafts().create(userId=user_id, body=_message).execute()

            print 'Draft id: %s\nDraft message: %s' % (draft['id'], draft['message'])

            return draft
        except errors.HttpError, error:
            print 'An error occurred: %s' % error
            return None


    def create_message(self):
        """Create a message for an email.
        Args:
        user_id: Email address of the user_id.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.

        Returns:
        An object containing a base64url encoded email object.
        """
        _message = MIMEText(self.message_text)
        _message['to'] = self.to
        _message['from'] = self.user_id
        _message['subject'] = self.subject
        self.message = {'raw': base64.urlsafe_b64encode(_message.as_string())}
        return self.message


    def create_message_with_attachment(self):
        """Create a message for an email.
        Args:
        user_id: Email address of the user_id.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.
        localdir: The directory containing the file to be attached.
        filename: The name of the file to be attached.

        Returns:
        An object containing a base64url encoded email object.
        """
        import os
        _message = MIMEMultipart()
        _message['to'] = self.to
        _message['from'] = self.user_id
        _message['subject'] = self.subject

        msg = MIMEText(self.message_text)
        _message.attach(msg)

        path = os.path.join(self.localdir, self.filename)
        content_type, encoding = mimetypes.guess_type(path)

        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
            main_type, sub_type = content_type.split('/', 1)
        if main_type == 'text':
            fp = open(path, 'rb')
            msg = MIMEText(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'image':
            fp = open(path, 'rb')
            msg = MIMEImage(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'audio':
            fp = open(path, 'rb')
            msg = MIMEAudio(fp.read(), _subtype=sub_type)
            fp.close()
        else:
            fp = open(path, 'rb')
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(fp.read())
            fp.close()

        msg.add_header('Content-Disposition', 'attachment', filename=self.filename)
        _message.attach(msg)

        self.message = {'raw': base64.urlsafe_b64encode(_message.as_string())}
        return self.message




def send_an_email(to,message):
    c = GoogleGmailClient()
    c.message_text = message
    c.to = to
    c.create_message()
    ret = c.send_message()
    print ret
    return ret

def main():
    pass



if __name__ == '__main__':
    main()

