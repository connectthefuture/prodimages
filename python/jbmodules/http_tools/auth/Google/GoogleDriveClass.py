#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
            self.scope    = self.rest_scopes # 'https://www.googleapis.com/auth/drive.file'
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
        # filescope='https://www.googleapis.com/auth/drive.file'
        # metadatascope='https://www.googleapis.com/auth/drive.metadata'
        f = file('/root/drive-photo-bfly-privatekey.p12', 'rb')
        key = f.read()
        f.close()
        credentials = SignedJwtAssertionCredentials(client_email, key, scope=self.scope)
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


####### AppDataDir
    def watch_file(self):
        """Watch for all changes to a user's Drive.

        Args:
        service: Drive API service instance.
        file_id: ID of the file to watch.
        channel_id: Unique string that identifies this channel.
        channel_type: Type of delivery mechanism used for this channel.
        channel_address: Address where notifications are delivered.

        Returns:
        The created channel if successful, None otherwise.
        """
        channel_id = 'channel1'
        channel_type = 'api#channel'
        channel_address = 'Notification Address URI'
        body = {
        'id': channel_id,
        'type': channel_type,
        'address': channel_address
        }
        try:
            new_channel = self.service.files().watch(fileId=self.file_id, body=body).execute()
            return new_channel
        except errors.HttpError, error:
            print 'An error occurred: %s' % error
            return None


    def print_application_data_folder_metadata(self):
        """Print metadata for the Application Data folder.

        Args:
        service: Drive API service instance.
        """
        try:
            _file = self.service.files().get(fileId='appfolder').execute()
            print 'Id: %s' % _file['id']
            print 'Title: %s' % _file['title']
        except errors.HttpError, error:
            print 'An error occurred: %s' % error


    def insert_file_in_application_data_folder(self):
        """Insert new file in the Application Data folder.

        Args:
        service: Drive API service instance.
        title: Title of the file to insert, including the extension.
        description: Description of the file to insert.
        mime_type: MIME type of the file to insert.
        filename: Filename of the file to insert.
        Returns:
        Inserted file metadata if successful, None otherwise.
        """
        _media_body = http.MediaFileUpload(self.title, mimetype=self.mime_type, resumable=True)
        _body = {
        'title': self.title,
        'description': self.description,
        'mimeType': self.mime_type,
        'parents': [{'id': 'appfolder'}]
        }

        try:
            _file = self.service.files().insert(body=_body,media_body=_media_body).execute()
            return _file
        except errors.HttpError, error:
            print 'An error occured: %s' % error
            return None

    def list_files_in_application_data_folder(self):
        """List all files contained in the Application Data folder.

        Args:
        service: Drive API service instance.
        Returns:
        List of File resources.
        """
        result = []
        page_token = None
        while True:
            try:
                param = {}
                if page_token:
                    param['pageToken'] = page_token
                else:
                    param['q'] = "'appfolder' in parents"
                _files = self.service.files().list(**param).execute()

                result.extend(_files['items'])
                page_token = _files.get('nextPageToken')
                if not page_token:
                    break
            except errors.HttpError, error:
                print 'An error occurred: %s' % error
                break
        return result

##########################
##########################
class DriveState(object):
    """Store state provided by Drive."""
    def __init__(self, state):
        """Create a new instance of drive state.

        Parse and load the JSON state parameter.

        Args:
          state: State query parameter as a string.
        """
        import json
        state_data = json.loads(state)
        self.action = state_data['action']
        self.ids = map(str, state_data.get('ids', []))


##########################
######### REDIS ##########
##########################
# ### Redis Client **K/V Store**
# ** \<colorstyle\>, \<file_id\>=\<local_filepath\> **
#
# ****[key] : {‘field’ -> ‘value’, ‘field’ -> ‘value’, ‘field’ -> ‘value’}****
#
#     """[users] – {set} – (“adam”, “bob”, “carol”)
#        [user:*username*:fullname] – {string} – (“Adam Smith”, “Bob Barker”, “Carol Burnett”)
#        [user:*username*:password] – {string} – (md5 hash password, no example)"""
##########################
######### REDIS ##########
##########################
import redis
#redis_host = 'pub-redis-17996.us-east-1-4.3.ec2.garantiadata.com'
#redis_port = 17996
redis_host = '127.0.0.1'
redis_port = 6379

r = redis.Redis(host=redis_host, port=redis_port,  encoding='utf-8', encoding_errors='strict')  ##,db=0, password=None, socket_timeout=None, connection_pool=None, unix_socket_path=None)

def add_new_drive2local_dbmap(file_id, parent_id=None, alternateLink=None, selfLink=None, downloadUrl=None, local_filepath=None, filename=None, drive_version=None):
    if not filename:
        filename=local_filepath.split('/')[-1]
    if filename is not None and filename[:9].isdigit():
        colorstyle = filename[:9]
        alt = filename.split('_')[1].split('.')[0][-1]
        if alt.isdigit():
            pass
        else:
            alt = 'NA'
    else:
        colorstyle='NA'
        alt='NA'

    if r.sadd("google_drive:ll_editorial", file_id):
    #if r.mset("google_drive:ll_editorial", file_id):
        ## Faking Hashes with Sets
        ## r.set("file_id:%s:colorstyle" % file_id, colorstyle)
        ## r.set("file_id:%s:local_filepath" % file_id, local_filepath)
        r.hset("file_id:%s" % file_id, "parent_id", parent_id)
        r.hset("file_id:%s" % file_id, "filename", filename)
        r.hset("file_id:%s" % file_id, "alternateLink", alternateLink)
        if selfLink is not None:
            r.hset("file_id:%s" % file_id, "selfLink", selfLink)
        if downloadUrl is not None:
            r.hset("file_id:%s" % file_id, "downloadUrl", downloadUrl)
        r.hset("file_id:%s" % file_id, "colorstyle", colorstyle)
        r.hset("file_id:%s" % file_id, "alt", alt)
        r.hset("file_id:%s" % file_id, "local_filepath", local_filepath)
        r.hmset("file_id:%s" % file_id, {"drive_version": drive_version})
        r.hsetnx("file_id:%s" % file_id, "ref_count", 0)
        r.hincrby("file_id:%s" % file_id, "ref_count", 1)
        print r.hvals("file_id:%s" % file_id)
        return True
    else:
        return False


def drive_uploading_folder_map2redis(dname=None, parent_id=None):
    ## Uploading
    #import GoogleDriveClient
    client = GoogleDriveClient()
    import os
    dname = dname
    client.title = dname.split('/')[-1]
    if not parent_id:
        client.parent_id = client.create_public_folder()
    else:
        client.parent_id = parent_id
    os.chdir(dname)
    localdirlist = os.listdir(dname)
    print localdirlist

    ##client.parent_id = parent_id
    for f in localdirlist:
        client.local_filepath = os.path.abspath(f)
        client.title = os.path.basename(client.local_filepath)
        client.description = dname
        res = client.upload_file_drive()
        file_id = res['id']
        _parent_id = res['parents'][0].get('id')
        alternateLink = res['alternateLink']
        drive_version = res['version']
        try:
            selfLink = res['selfLink']
        except KeyError:
            selfLink = None
        try:
            downloadUrl = res['downloadUrl']
        except KeyError:
            downloadUrl = None
        title = res['title']
        add_new_drive2local_dbmap(file_id, parent_id=_parent_id, alternateLink=alternateLink, selfLink=selfLink, downloadUrl=downloadUrl, local_filepath=client.local_filepath, filename=title, drive_version=drive_version)


def drive_downloading(destdir=None, file_id=None):
    ## Downloading
    #import GoogleDriveClient
    import os.path
    client = GoogleDriveClient()
    client.file_id = file_id
    if not client.title:
        client.title = client.file_id
    client.local_filepath = os.path.join(destdir, client.title)
    client.download_file_drive()


#c = GoogleDriveClient()
#print c.list_ret_IDs_indir()
if __name__ == '__main__':
    import sys
    drive_uploading_folder_map2redis(dname=sys.argv[1], parent_id=None)

