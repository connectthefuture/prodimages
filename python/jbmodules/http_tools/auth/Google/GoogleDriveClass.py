#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'johnb'

class GoogleDriveClient:

    def __init__(self, file_id=None, local_filepath='', description='', title='', kind = '', acct_type='', properties='', role='', share_email='', folder_color_rgb='', folder_title='', database_id=''):
        import googleapiclient
        self.client = googleapiclient
        self.file_id = file_id
        self.pardir_fileid = ''
        self.drive_file_content = ''
        self.drive_file_data = {}
        self.drive_folder_files = []
        self.drive_folder_data = {}
        self.local_filepath = local_filepath
        self.mime_type = ''

        self.folder_title = folder_title
        self.folder_color_rgb = folder_color_rgb

        ### Permissions
        self.fileid_permissions = ''
        self.user_permission = []
        self.kinds = ["drive#file", "drive#fileLink", "drive#parentReference", "drive#user", "drive#permission"]
        self.roles = ['reader', 'writer', 'owner']
        self.acct_types = ['user', 'group', 'domain', 'anyone']
        if not acct_type:
            self.acct_type = self.acct_types[0]
        if not kind:
            self.kind = self.kinds[0]
        else:
            self.kind = kind
        if not role:
            self.role = self.roles[0]
        else:
            self.role = role
        self.share_email = ''
        if not share_email:
            self.share_email = 'john.bragato@gmail.com'
        else:
            self.permission_id = self.get_permission_id_for_email(self.share_email)

        ## AdditionalData
        if not properties:
            self.properties = [{
                'key': 'databaseId',
                'value': database_id,
                'visability': 'PRIVATE'
            }]
        if not title:
            try:
                self.title = '{}'.format(self.local_filepath.split('/')[-1].split('.')[0])
            except IndexError:
                self.title = ''
        if not description:
            self.description = ''
        self.service = self.instantiate_google_drive_serviceAccount_bfly()


    def instantiate_google_drive_serviceAccount_bfly(self):
        import httplib2
        from googleapiclient.discovery import build
        from oauth2client.client import SignedJwtAssertionCredentials
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
        self.service = build(serviceName, version, http=http)
        return self.service



    ## File and Folder Ops
    def download_file_drive(self):
        request = self.service.files().get_media(fileId=self.file_id)
        fdest = open(self.local_filepath, 'w')
        self.drive_file_content = self.client.http.MediaIoBaseDownload(fdest, request)
        while True:
            try:
                download_progress, done = self.drive_file_content.next_chunk()
            except self.client.errors.HttpError, error:
                print 'An error occurred: %s' % error
                return self.drive_file_content
            if download_progress:
                print 'Download Progress: %d%%' % int(download_progress.progress() * 100)
            if done:
                print 'Download Complete', self.local_filepath
                return self.local_filepath


    def upload_file_drive(self):
        import pprint
        media_body = self.client.MediaFileUpload(self.local_filepath, self.mimetype, resumable=True)
        body = {
            'title': self.title,
            'description': self.description,
            'mimeType': self.mimetype,
            'properties': self.properties
        }
        self.drive_file_data = self.service.files().insert(body=body, media_body=media_body).execute()
        pprint.pprint(self.drive_file_data)
        return self.drive_file_data


    def create_drive_folder(self):
        folder_body = {
            'title': self.title,
            'description': self.description,
            'parents': [{'id': self.pardir_fileid}],
            'mimeType': 'application/vnd.google-apps.folder',
            'folderColorRgb': self.folder_color_rgb,
            'userPermission': self.user_permission
        }
        self.drive_folder_data = self.service.files().insert(media_body=folder_body).execute()
        return self.drive_folder_data


    def save_file_drive_folder(self):
        import pprint
        self.service= self.instantiate_google_drive_serviceAccount_bfly()
        body = {
            'title': self.title,
            'description': self.description,
            'mimeType': self.mimetype,
            "properties": self.properties,
            "parents": [{
                "kind": self.kind,
                "id": self.pardir_fileid
                }]
        }
        ext = self.local_filepath.format(self.local_filepath.split('.')[-1])
        if ext[:3].lower() == 'jpg':
            self.mimetype = 'image/jpeg'
        elif ext[:3].lower() == 'png':
            self.mimetype = 'image/png'
        elif ext[:3].lower() == 'tif':
            self.mimetype = 'image/tiff'
        elif ext[:3].lower() == 'gif':
            self.mimetype = 'image/gif'
        media_body = self.client.MediaFileUpload(self.local_filepath, mimetype=self.mimetype, resumable=True)
        self.drive_file_data = self.service.files().insert(body=body, media_body=media_body).execute()
        pprint.pprint(self.drive_file_data)
        try:
            self.drive_file_data = self.service.files().insert(body=body, media_body=media_body).execute()
            return self.drive_file_data
        except self.client.errors.HttpError, error:
            print 'An error occured: %s' % error
            return None


    def insert_file_in_folder(self):
        #self.pardir_fileid =  'appfolder'
        media_body = self.client.MediaFileUpload(self.local_filepath, mimetype=self.mime_type, resumable=True)
        body = {
            'title': self.title,
            "description": self.description,
            "parents": [{"id": self.pardir_fileid}],
            'mimeType': self.mime_type,
            "properties": self.properties
        }


    ## List Contents of Dirs
    def list_filesdata_current_dir(self):
        req = self.service.files().list()
        self.drive_folder_data = req.execute()
        return self.drive_folder_data


    def list_fileitems_current_dir(self):
        items = self.drive_folder_data['items'][0].items()
        [ self.drive_folder_files.extend(i) for i in items if i ]
        return self.drive_folder_files


    def list_files_in_pardir(self):
        self.drive_folder_files = []
        page_token = None
        while True:
            try:
                param = {}
                if page_token:
                    param['pageToken'] = page_token
                else:
                    param['q'] = "{} in parents".format(self.title)
                listdir = self.service.files().list(**param).execute()
                self.drive_folder_files.extend(listdir['items'])
                page_token = listdir.get('nextPageToken')
                if not page_token:
                    break
            except self.client.errors.HttpError, error:
                print 'An error occurred: %s' % error
                break
        return self.drive_folder_files


    ### Permissions
    def create_public_folder(self):
        body = {
            'title': self.title,
            'mimeType': 'application/vnd.google-apps.folder'
        }

        _public_folder = self.service.files().insert(body=body).execute()
        permission = {
            'value': '',
            'type': 'anyone',
            'role': 'reader'
        }
        self.service.permissions().insert(fileId=_public_folder['id'], body=permission).execute()
        self.pardir_fileid = _public_folder['id']
        return self.pardir_fileid


    def change_permissions_by_fileid(self):
        permission_data = self.service.permissions().insert(
            body = {
                'value': self.share_email,
                #'type': 'group',
                'type': 'user',
                'role': 'reader', ##self.role
                'fileId': self.file_id
            })
        self.fileid_permissions = permission_data.execute()
        return self.fileid_permissions


    def get_permission_id_for_email(self):
      try:
        _permission_data = self.service.permissions().getIdForEmail(email=self.share_email).execute()
        print _permission_data['id']
        self.permission_id = _permission_data['id']
        return self.permission_id
      except self.client.errors.HttpError, error:
        print 'An error occured: %s' % error


    ## Utils
    def get_idtitle_by_fileid(self):
        try:
            self.drive_file_data = self.service.files().get(fileId=self.file_id).execute()
            print 'Title: %s' % self.drive_file_data['title']
            print 'Id: %s' % self.drive_file_data['id']
            self.file_id = self.drive_file_data['id']
            self.title = self.drive_file_data['title']
            return self.file_id, self.title
        except self.errors.HttpError, error:
            print 'An error occurred: %s' % error

