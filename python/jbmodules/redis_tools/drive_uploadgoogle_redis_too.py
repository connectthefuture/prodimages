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
    def __init__(self, file_id='', local_filepath='', description='', title='', scope='', role='', kind = '', database_id='', prop_key='', prop_value= '', parent_id='', folder_color_rgb='', new_comment='', q=''):
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
        self.visibility = 'Private' ## 'Public'
        self.q = q
        ### Properties
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
        self.new_comment = new_comment
        self.comment_id = ''
        self.indexable_text = ''
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


###### Properties
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


###### Comments and Selects Methods/Properties
    ## Add-Edit-List Comments/Selects for Files
    @property
    def comments_from_fileid(self):
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


# In[2]:

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

