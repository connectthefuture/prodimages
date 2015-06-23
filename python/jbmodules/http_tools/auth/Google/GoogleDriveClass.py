#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'johnb'

class GoogleDriveClient:

    def __init__(self, file_id=None, local_filepath='', description='', title='', kind = '', perm_type='', perm_value='', properties='', role='', share_email='', folder_color_rgb='', folder_title='', database_id='', prop_key='', prop_value= ''):
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
        self.visibility = 'Public'
        self.kinds = ["drive#file", "drive#fileLink", "drive#parentReference", "drive#user", "drive#permission"]
        self.roles = ['reader', 'writer', 'owner']
        self.perm_types = ['user', 'group', 'domain', 'anyone']
        if not share_email:
            self.share_email = 'john.bragato@gmail.com'
            self.permission_id = self.get_permission_id_for_email()
        else:
            self.share_email = share_email
            self.permission_id = self.get_permission_id_for_email()
        self.perm_value = perm_value
        if not perm_type:
            self.perm_type = self.perm_types[0]
        else:
            self.perm_type = perm_type
        if not kind:
            self.kind = self.kinds[0]
        else:
            self.kind = kind
        if not role:
            self.role = self.roles[0]
        else:
            self.role = role


        ## Filename + Desc and AdditionalData Properties
        if not title:
            try:
                self.title = '{}'.format(self.local_filepath.split('/')[-1].split('.')[0])
            except IndexError:
                self.title = ''
        else:
            self.title = title

        if not description:
            self.description = ''
        else:
            self.description = description

        ### Properties
        if not properties and not prop_key and not prop_value:
            self.properties = [{
               'key': 'databaseId',
               'value': database_id,
               'visability': 'PRIVATE'
            }]
        else:
            self.properties = properties
            self.prop_key = prop_key
            self.prop_value = prop_value

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

    ## Additional Custom File Properties
    def insert_property(self):
        body = self.properties[0]
        try:
            p = self.service.properties().insert(fileId=self.file_id, body=body).execute()
            return p
        except self.client.errors.HttpError, error:
            print 'An error occurred: %s' % error
        return None


    def update_property(self):
        try:
            # First retrieve the property from the API.
            _prop = self.service.properties().get(fileId=self.file_id, propertyKey=self.prop_key, visibility=self.visibility).execute()
            _prop['value'] = self.prop_value
            return self.service.properties().update(fileId=self.file_id, propertyKey=self.prop_key, visibility=self.visibility, body=_prop).execute()
        except self.client.errors.HttpError, error:
            print 'An error occurred: %s' % error
        return None


    ## Shared Folder
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

    ### Permissions
    def insert_new_permission(self):
        _permission = {
            'value': self.perm_value,
            'type':  self.perm_type,
            'role':  self.role,
            'visibility': self.visibility
        }
        try:
            return self.service.permissions().insert(fileId=self.file_id, body=_permission).execute()
        except self.client.errors.HttpError, error:
            print 'An error occurred: %s' % error
        return None

    def update_fileid_permission(self):
        try:
            # First retrieve the permission from the API.
            _permission_data = self.service.permissions().get(fileId=self.file_id, permissionId=self.permission_id).execute()
            _permission_data['role'] = self.role
            return self.service.permissions().update(fileId=self.file_id, permissionId=self.permission_id, body=_permission_data).execute()
        except self.client.errors.HttpError, error:
            print 'An error occurred: %s' % error
        return None


    def change_permission_by_fileid(self):
        _permission_data = self.service.permissions().insert(
            body={
                'value': self.share_email,
                # 'type': 'group',
                'type': self.perm_type,
                'role': self.role,  ##self.role
                'fileId': self.file_id
            })
        self.fileid_permissions = _permission_data.execute()
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

