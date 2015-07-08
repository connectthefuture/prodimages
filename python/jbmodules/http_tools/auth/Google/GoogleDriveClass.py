#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'johnb'

ProductionRoot  = '0B0Z4BGpAAp5KfmJQUjFlSjlPVTFUcGo1eWpVRDhmekdzLVVsWUYyM1BBZGhHUGRTTVpUU1E'
MarketplaceRoot = '0B0Z4BGpAAp5Kfm5UOWk3WFd2b1ZIVzNMbDliUVNsS2tHOVJXc0loRERDMDRzQmkzV0JRaHM'
EditorialShare  = '0B0Z4BGpAAp5KfnRZaWl4cHMxUGg4MGI0LUFjUWFDdzQ4VWsyTi11OGJPQVlRakRKSXNScHM'
VendorShare     = '0B0Z4BGpAAp5KfmJQUjFlSjlPVTFUcGo1eWpVRDhmekdzLVVsWUYyM1BBZGhHUGRTTVpUU1E'
LookletImages   = '0B0Z4BGpAAp5KfkpZeENQamp0UWpZaWtEWHJGd0xMa3dGV01acG1ESENqRzRfaW5od2JjV1U'
StillImages     = '0B0Z4BGpAAp5KfmxtRktkUGhLckdLSXE0bzA2azhMUW1yVFd6R2VlUUxMN0lsY0NZUDdBaTg'
VendorImages    = '0B0Z4BGpAAp5Kfm5UOWk3WFd2b1ZIVzNMbDliUVNsS2tHOVJXc0loRERDMDRzQmkzV0JRaHM'

from googleapiclient import http,errors
class GoogleDriveClient:
    def __init__(self, file_id='', local_filepath='', description='', title='', scope='', role='', kind = '', database_id='', prop_key='', prop_value= '', parent_id='', folder_color_rgb='', new_comment='', q='', third_party_email=''):
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
        self.mime_type = '' #'image/jpeg'
        self.description = description
        self.q = q
        #self.pardir_fileid = ''

        ### Permissions - Scopes
        self.kinds = ["drive#file", "drive#fileList", "drive#fileLink", "drive#parentReference", "drive#user",
                      "drive#permission", "drive#comment", "drive#commentReply"]
        self.roles = ['owner', 'reader', 'writer', 'commenter']
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
        self.perm_id = self.get_perm_id_from_email()
        self.perm_types = ['user', 'group', 'domain', 'anyone']
        self.perm_type = self.perm_types[0]
        self.perm_value = ''


        ### Properties
        self.prop_key = prop_key
        self.prop_value = prop_value
        self.visibility = 'Public'  ## 'Private'

        if not prop_key and not prop_value:
            if not database_id:
                database_id = self.file_id
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

        ## Comments, Search, Misc
        self.new_comment = new_comment
        self.comment_id = ''
        self.indexable_text = ''
        self.third_party_email = third_party_email
        if not folder_color_rgb:
            self.folder_color_rgb = '#6699CC'
        else:
            self.folder_color_rgb = folder_color_rgb
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


###### Files
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


#######################
    def download_file_content(self):
        """Download a file's content.

        Args:
          service: Drive API service instance.
          drive_file: Drive File instance.

        Returns:
          File's content if successful, None otherwise.
        """
        #gdox
        # _download_url = file['exportLinks']['application/pdf']
        # _download_url = file['webContentLink']
        _download_url = self.service.files().get('downloadUrl')

        if _download_url:
            resp, content = self.service._http.request(_download_url)
            if resp.status == 200:
                print 'Status: %s' % resp
                return content
            else:
                print 'An error occurred: %s' % resp
                return None
        else:
            # The file doesn't have any content stored on Drive.
            return None


    ## OK ##
    def upload_file_drive(self):
        import pprint
        media_body = http.MediaFileUpload(self.local_filepath, mimetype=self.mime_type , resumable=True)
        try:
            if not self.indexable_text:
                _indexableText = ' '.join(str(self.description + self.title + self.properties[0].values()[0] + self.properties[0].values()[1]))
            else:
                _indexableText = self.indexable_text
        except TypeError:
            _indexableText = self.indexable_text
        body = {
            'title': self.title,
            'description': self.description,
            'mimeType': self.mime_type,
            'properties': self.properties,
            'indexableText': _indexableText
        }
        if self.parent_id:
            body['parents'] = [{'id': self.parent_id}]

        _uploaded_file_data = self.service.files().insert(body=body, media_body=media_body).execute()
        pprint.pprint(_uploaded_file_data)
        return _uploaded_file_data

    def update_file(self):
        """service, file_id, new_title, new_description, new_mime_type, new_filename, new_revision):
        Update an existing file's metadata and content.

        Args:
          service: Drive API service instance.
          file_id: ID of the file to update.
          new_title: New title for the file.
          new_description: New description for the file.
          new_mime_type: New MIME type for the file.
          new_filename: Filename of the new content to upload.
          new_revision: Whether or not to create a new revision for this file.
        Returns:
          Updated file metadata if successful, None otherwise.
        """
        try:
            # First retrieve the file from the API.
            _file = self.service.files().get(fileId=self.file_id).execute()

            # File's new metadata.
            _file['title'] = self.title
            _file['description'] = self.description
            #_file['mimeType'] = self.mime_type
            _properties = str(_file['properties'].values())
            _imageMetadata = str(_file['imageMediaMetadata'].values())
            try:
                if not self.indexable_text:
                    _file['indexableText'] = ' '.join(str(_file['description'] + _file['title'] +  _properties + _imageMetadata))
                else:
                    _file['indexableText'] = self.indexable_text
                print _file['indexableText']
            except TypeError:
                print 'TYPE ERROR ON 186 WERE YOU EXPECTED'

            # File's new content.
            media_body = http.MediaFileUpload(self.title, resumable=True)
            # Send the request to the API.
            updated_file =  self.service.files().update(fileId=self.file_id, body=_file, newRevision=False, media_body=media_body).execute()
            return updated_file
        except errors.HttpError, error:
            print 'An error occurred: %s' % error
            return None

    def rename_drive_file(self):
        try:
            _file = {'title': self.title}
            # Rename the file.
            _updated_file = self.service.files().patch(fileId=self.file_id, body=_file, fields='title').execute()
            return _updated_file
        except errors.HttpError, error:
            print 'An error occurred: %s' % error
            return None

    ## Create Shortcut to File
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

    ## Change Files Parent Folder
    def move_insert_file_into_folder(self):
      """Insert a file into a folder.
      Args:
        service: Drive API service instance.
        parent_id: ID of the folder to insert the file into.
        file_id: ID of the file to insert.
      Returns:
        The inserted parent if successful, None otherwise.
      """
      _new_parent = {'id': self.parent_id}
      try:
        return self.service.parents().insert(fileId=self.file_id, body=_new_parent).execute()
      except errors.HttpError, error:
        print 'An error occurred: %s' % error
      return None


##### Folders
    def getprint_parents_by_fileid(self):
        """Print a file's parents.

        Args:
          service: Drive API service instance.
          file_id: ID of the file to print parents for.
        """
        parents_ids = []
        try:
            _parents = self.service.parents().list(fileId=self.file_id).execute()
            for parent in _parents['items']:
                print 'File Id: %s' % parent['id']
                parents_ids.append(parent['id'])
            return parents_ids
        except errors.HttpError, error:
            print 'An error occurred: %s' % error


    ## OK ##
    def create_drive_folder(self):
        body = {
            'title': self.title,
            'description': self.description,
            'mimeType': 'application/vnd.google-apps.folder',
            'folderColorRgb': self.folder_color_rgb
            #'userPermission': self.user_permission
        }
        if self.parent_id:
            body['parents'] = [{'id': self.parent_id}]

        _new_folder_data = self.service.files().insert(body=body).execute()['items'][0].items()
        return _new_folder_data


####### Shared Public Folder
    ### OK ###
    def create_public_folder(self):
        body = {
            'title': self.title,
            'mimeType': 'application/vnd.google-apps.folder',
            'folderColorRgb': self.folder_color_rgb
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
        # self.pardir_fileid = _public_folder['id']
        #return self.pardir_fileid
        return _public_folder['id']

####################################
###### Permissions and FileSharing #
####################################
    ##@property
    def get_perm_id_from_email(self):
        """Prints the Permission ID for an email address.

        Args:
        service: Drive API service instance.
        email: Email address to retrieve ID for.
        """
        try:
            _resp = self.service.permissions().getIdForEmail(email=self.third_party_email).execute()
            print _resp['id']
            return _resp['id']
        except errors.HttpError, error:
            print 'An error occured: %s' % error


    def insert_permission(self):
        """Insert a new permission.

        Args:
        service: Drive API service instance.
        file_id: ID of the file to insert permission for.
        value: User or group e-mail address, domain name or None for 'default'
           type.
        perm_type: The value 'user', 'group', 'domain' or 'default'.
        role: The value 'owner', 'writer' or 'reader'.
        Returns:
        The inserted permission if successful, None otherwise.
        """
        _new_permission = {
        'value': self.perm_value,
        'type': self.perm_type,
        'role': self.role
        }
        try:
            return self.service.permissions().insert(fileId=self.file_id, body=_new_permission).execute()
        except errors.HttpError, error:
            print 'An error occurred: %s' % error
            return None


    def update_permission(self):
        """Update a permission's role.

        Args:
        service: Drive API service instance.
        file_id: ID of the file to update permission for.
        perm_id: ID of the permission to update.
        new_role: The value 'owner', 'writer' or 'reader'.

        Returns:
        The updated permission if successful, None otherwise.
        """
        try:
            # First retrieve the permission from the API.
            _permission = self.service.permissions().get(fileId=self.file_id, permissionId=self.perm_id).execute()
            _permission['role'] = self.role
            return self.service.permissions().update(fileId=self.file_id, permissionId=self.perm_id, body=_permission).execute()
        except errors.HttpError, error:
            print 'An error occurred: %s' % error
            return None


    def retrieve_permissions(self):
        """Retrieve a list of permissions.

        Args:
        service: Drive API service instance.
        file_id: ID of the file to retrieve permissions for.
        Returns:
        List of permissions.
        """
        try:
            _permissions = self.service.permissions().list(fileId=self.file_id).execute()
            return _permissions.get('items', [])
        except errors.HttpError, error:
            print 'An error occurred: %s' % error
            return None


####################################
###### Properties - Custom  ########
####################################
## Add-Edit Additional Custom File Properties
    def insert_property(self):
        body = self.properties[0]
        try:
            _p = self.service.properties().insert(fileId=self.file_id, body=body).execute()
            return _p
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

    def retrieve_properties(self):
        """Retrieve a list of custom file properties.

        Args:
          service: Drive API service instance.
          file_id: ID of the file to retrieve properties for.
        Returns:
          List of custom properties.
        """
        try:
            props = self.service.properties().list(fileId=self.file_id).execute()
            return props.get('items', [])
        except errors.HttpError, error:
            print 'An error occurred: %s' % error
        return None

    def remove_permission(self):
        """Remove a permission.

        Args:
        service: Drive API service instance.
        file_id: ID of the file to remove the permission for.
        permission_id: ID of the permission to remove.
        """
        try:
            self.service.permissions().delete(fileId=self.file_id, permissionId=self.perm_id).execute()
        except errors.HttpError, error:
            print 'An error occurred: %s' % error

###### Comments and Selects Methods/Properties
    ## Add-Edit-List Comments/Selects for Files
    @property
    def comments_for_fileid(self):
        """Retrieve a list of comments.
        Args:
        service: Drive API service instance.
        file_id: ID of the file to retrieve comments for.
        Returns:
        List of comments.
        """
        try:
            _comments = self.service.comments().list(fileId=self.file_id).execute()
            return _comments.get('items', [])
        except errors.HttpError, error:
            print 'An error occurred: %s' % error
        return None

    def insert_comment(self):
        """Insert a new document-level comment.

        Args:
        service: Drive API service instance.
        file_id: ID of the file to insert comment for.
        content: Text content of the comment.
        Returns:
        The inserted comment if successful, None otherwise.
        """
        _new_comment = {
          'content': self.new_comment
        }
        try:
            return self.service.comments().insert(fileId=self.file_id, body=_new_comment).execute()
        except errors.HttpError, error:
            print 'An error occurred: %s' % error
            return None

    def print_single_comment(self):
        """Print information about the specified comment.

        Args:
        service: Drive API service instance.
        file_id: ID of the file to print comment for.
        comment_id: ID of the comment to print.
        """
        try:
            _comment = self.service.comments().get(fileId=self.file_id, commentId=self.comment_id).execute()
            print 'Modified Date: %s' % _comment['modifiedDate']
            print 'Author: %s' % _comment['author']['displayName']
            print 'Content: %s' % _comment['content']
        except errors.HttpError, error:
            print 'An error occurred: %s' % error


###############################################
################### Revisions #################
###############################################
    @property
    def revisions_for_fileid(self):
        """Retrieve a list of revisions.

        Args:
        service: Drive API service instance.
        file_id: ID of the file to retrieve revisions for.
        Returns:
        List of revisions.
        """
        try:
            _revisions = self.service.revisions().list(fileId=self.file_id).execute()
            return _revisions.get('items', [])
        except errors.HttpError, error:
            print 'An error occurred: %s' % error
            return None


####### ###### ###### ###### ###### ###### ######
####### ## Print/Get File or Folder info # ######
####### ###### ###### ###### ###### ###### ######
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
                print '{0} \t-- {1} --\tfile_id--> ({2})\tparent_id--> {3}'.format(item['title'], item['mimeType'], item['id'], item['parents'][0].get('id'))
                baseinfo['id'] = item['id']
                baseinfo['drive_version'] = item['version']
                baseinfo['title'] = item['title']
                baseinfo['mimeType'] = item['mimeType']
                baseinfo['parents'] = item['parents'][0]
                baseinfo['parent_id'] = item['parents'][0].get('id')
                try:
                    baseinfo['md5Checksum'] = item['md5Checksum']
                except KeyError:
                    baseinfo['md5Checksum'] = 'NA'
                try:
                    baseinfo['downloadUrl'] = item['downloadUrl']
                except KeyError:
                    baseinfo['downloadUrl'] = 'NA'
                baseinfo['selfLink'] = item['selfLink']
                baseinfo['alternateLink'] = item['alternateLink']
                #baseinfo['thumbnailLink'] = item['thumbnailLink']
                infodict[item['id']] = baseinfo
            return infodict


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
                    #break
            except errors.HttpError, error:
                print 'An error occurred: %s' % error
                break


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

