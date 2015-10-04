
# coding: utf-8

###########################
######################################################
###########################
#### Mozu Connection + Upload New Images
# db_uri = 'oracle+cx_oracle://MZIMG:p1zza4me@qarac201-vip.qa.bluefly.com:1521/bfyqa1201'
# conn = sqlalchemy.create_engine(db_uri, implicit_returning=False, coerce_to_decimal=False)
#### Mozu Auth - Upload - GetKey ####
def get_mozu_authtoken(tenant_url):
    import requests, json
    #  "http://requestb.in/q66719q6" #
    auth_url = "https://home.staging.mozu.com/api/platform/applications/authtickets"
    tenant_url = tenant_url
    headers = {'Content-type': 'application/json',
               'Accept-Encoding': 'gzip, deflate'}
    auth_request = {'applicationId' : 'bluefly.product_images.1.0.0.release', 'sharedSecret' : '53de2fb67cb04a95af323693caa48ddb'}

    auth_response = requests.post(auth_url, data=json.dumps(auth_request), headers=headers, verify=False)
    # parse params from filepath
    # TODO: 5) add Validation(regex) to prevent unwanted updates
    ##
    print "Auth Response: %s" % auth_response.status_code
    auth_response.raise_for_status()
    auth = auth_response.json()
    print "Auth Ticket: %s" % auth["accessToken"]
    return auth["accessToken"]

# Upload and Return MozuID
#### Mozu Connection + Upload New Images
# db_uri = 'oracle+cx_oracle://MZIMG:p1zza4me@qarac201-vip.qa.bluefly.com:1521/bfyqa1201'
# conn = sqlalchemy.create_engine(db_uri, implicit_returning=False, coerce_to_decimal=False
# Upload and Return MozuID
def upload_productimgs_mozu(src_filepath):
    import requests, json
    import os.path as path
    tenant_url = "https://t11146.staging-sb.mozu.com/"
    headers = {'Content-type': 'application/json', 'x-vol-app-claims' : get_mozu_authtoken(tenant_url), 'x-vol-tenant' : '11146', 'x-vol-master-catalog' : '1' }
    #, 'x-vol-dataview-mode': 'Pending', # ??'x-vol-site' : '1', }
    document_data_api = tenant_url + "/api/content/documentlists/files@mozu/documents"
    bf_imageid   = path.basename(src_filepath) #[:-1]
    print bf_imageid, src_filepath
    ext = bf_imageid.split('.')[-1]
    document    = ''
    document_id = ''
    document_payload = {'listFQN' : 'files@mozu', 'documentTypeFQN' : 'image@mozu', 'name' : bf_imageid, 'extension' : ext}
    document_response = requests.post(document_data_api, data=json.dumps(document_payload), headers=headers, verify=False )
    #document_response.raise_for_status()
    if document_response.status_code < 400:
        document = document_response.json()
        try:
            document_id = document["id"]
            # colorstyle    = bf_imageid[:9]
            # insert_docid_db(db_name,document_id=document_id, bf_imageid=bf_imageid, colorstyle=colorstyle, img_number=sequence)
        except KeyError:
            document_response = requests.put(document_data_api, data=json.dumps(document_payload), headers=headers, verify=False)
            document = document_response.json()
            document_id = document["id"]
            document_response.raise_for_status()
        ## create rest url with doc id from resp
        document_content_api = tenant_url + "/api/content/documentlists/files@mozu/documents/" + document_id + "/content"
        #files = {'media': open(src_filepath, 'rb')}
        mimetype = "image/{}".format(ext.lower().replace('jpg','jpeg'))
        headers["Content-type"] = mimetype
        file_data = open(src_filepath, 'rb').read()
        content_response = requests.put(document_content_api, data=file_data, headers=headers, verify=False)
        print "document ID: %s" % document_id
        print "document_payload: %s" % document_payload
        print "Document content upload Response: %s" % content_response.text
        #document_response.raise_for_status()
        return document_id, content_response
        #return bf_imageid, mz_imageid
    elif document_response.status_code == 409:
        mimetype = "image/{}".format(ext.lower().replace('jpg', 'jpeg'))
        headers["Content-type"] = mimetype
        print document_id, ' <-- DocId 409 Code Numero 1'
        print 'LOCOS -->', locals()
        
        db_query = mozu_image_table_instance().select().where(bf_imageid==bf_imageid).execute()
        r1 = db_query.fetchone() #['mz_imageid'], ' <-- mz_imageid'
        old_mz_imageid = r1['mz_imageid']
        old_md5checksum = r1['md5checksum']
        print old_mz_imageid, ' <--- R1'
        if old_mz_imageid is not None:
            print 'Old MozuID Retrieved from ORCL', dir(old_mz_imageid)
            documentUploadApi = tenant_url + "/api/content/documentlists/files@mozu/documents/" + old_mz_imageid + "/content"
            # files = {'media': open("c:\mozu-dc-logo.png", "rb")};
            file_data = open(src_filepath, 'rb').read()
            headers["Content-type"] = mimetype #"image/png";
            print old_mz_imageid , 'MZID then docid itercontent stuff'
            #print dir(document_response)
            update_content_response = requests.put(documentUploadApi, data=file_data, headers=headers, verify=False);
            print update_content_response.status_code, update_content_response.headers
#             ext = bf_imageid.split('.')[-1]
#             document    = ''
#             document_id = ''
#             document_payload = {'listFQN' : 'files@mozu', 'documentTypeFQN' : 'image@mozu', 'name' : bf_imageid, 'extension' : ext}
            document = update_content_response.json()
            document_id = document["id"]
            print document_id, ' <-- DocId 409 Code'
            print '409 Err --> Bluefly Filename Already in Mozu, if you are trying to update the image, this is not the way.\n\t%s' % src_filepath
            ## TODO: 1)  On duplicate file in mozu, check PGSQL by Filename and compare stored MD5 with current MD5.
            ## TODO: 1A) If same MD5 skip and return MOZUID, else if different.....
            ## TODO  2)  Update Mozu stored image using main_update_put(src_filepath), sending to an "update" endpoint(need to get uri)
            ## TODO: 3)  Update PGSQL MOZUID + MD5
            ## TODO: 4)  Bust image cache on updates in MOZU by forcing MEDIA_VERSION to increment -- Need API endpoint to PM or its going to be super hackey.
            return document_id, content_response
        else:
            print 'MZID is None'
    else:
        print 'No Mozuid in DB, Failed with code --> ', document_response.status_code
        


###########################
######################################################
###########################
### Utility Funx - Get File Data
## util func calcs md5 of file

def md5_checksumer(src_filepath):
    import hashlib
    import os.path as path
    if src_filepath is not None and path.isfile(src_filepath):
        filepath = path.abspath(src_filepath)
        try:
            _file = open(filepath, "rb")
            content = _file.read()
            _file.close()
            md5 = hashlib.md5(content)
            _hash = md5.hexdigest()
            return _hash
        except:
            return False

# Converts image to jpeg
def magick_convert_to_jpeg(img, destdir=None):
    import subprocess
    ext = img.split('.')[-1]
    outfile = img.split('/')[-1].split('.')[0] + ".jpg"
    if not destdir:
        pass
    else:
        import os.path as path
        outfile = path.join(destdir, outfile)
    subprocess.call([
        'convert',
        '-colorspace',
        'RGB',
        "-format",
        ext,
        img,
        "-depth",
        "16",
        "-density",
        "72x72",
        # "-profile",
        # "/usr/local/color_profiles/AdobeRGB1998.icc",
        # "-colorspace",
        # "RGB",
        "-define",
        "jpeg:dct-method\=float",
        "-define",
        "jpeg:sampling-factor\=4:2:2",
        "-filter",
        "LanczosSharp",
        "-compress",
        "JPEG",
        '-quality',
        '90%',
        # "-profile",
        # '/usr/local/color_profiles/sRGB.icm',
        "-interlace",
        "Plane",
        "-colorspace",
        'sRGB',
        "-depth",
        "8",
        "-format",
        "jpeg",
        "-strip",
        outfile
        ])
    return outfile

########################
## Extracts the image metadata from file
def get_exif_all_data(src_filepath):
    import exiftool
    print type(src_filepath), src_filepath
    if src_filepath is not None:
        if src_filepath.split('.')[-1].lower() == 'jpg' or 'png':
            with exiftool.ExifTool() as et:
                metadata = et.get_metadata(src_filepath)  # ['XMP:DateCreated'][:10].replace(':','-')
            return metadata
    else: pass


## Compile Inserts as dict with key == bluefly file name
def compile_data_db_import(list_of_images,**kwargs):
    images_insert_dict = {}
    for img in list_of_images:
        bf_imageid = img.split('/')[-1]
        
        try:
            mozu_image_table = mozu_image_table_instance()
            md5checksum = md5_checksumer(img)
            image_metadata = get_exif_all_data(img)
        except TypeError: 
            print 'TYPE Error'
            pass

        images_insert_dict[img] = dict(bf_imageid  = bf_imageid, 
                                                mz_imageid  = kwargs.get('mz_imageid', 'NA'), 
                                                md5checksum = md5checksum)
                                                #image_metadata = image_metadata)
        #print 'METADATA --> ', image_metadata
    return images_insert_dict
   
### Generic Logger
def mr_logger(filepath,*args):
    import datetime
    current_dt = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
    logged_items = []
    if len(args) > 0:
        for arg in args:
            logit = "{}\t{}\n".format(current_dt,arg)
            logged_items.append(logit)
    for i in logged_items:
        with open(filepath, 'ab+') as f:
            f.write(i)
    return filepath

###########################
######################################################
###########################
### DB - oracle Alchemy Funcs and Table Defs
##
########################### Replaced By Alchemy ############################

def mozu_image_table_instance(**kwargs):
    import sqlalchemy, datetime
    from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData, create_engine
    from sqlalchemy import Sequence, FetchedValue, Text
    from sqlalchemy.dialects import oracle as oracle_dialect

    db_uri = 'oracle+cx_oracle://MZIMG:p1zza4me@qarac201-vip.qa.bluefly.com:1521/bfyqa1201'
    engine = sqlalchemy.create_engine(db_uri, implicit_returning=False, coerce_to_decimal=False)
    metadata = MetaData(bind=engine)  #, quote_schema=True, schema='bfyqa1201')
    mozu_image_table = Table( 'mozu_image', metadata,
        #Column('id', Integer, Sequence('mozu_image_seq_trigger'), primary_key=True),
        Column('id', Integer, server_default=FetchedValue(), primary_key=True),
        Column('bf_imageid', String(19), unique=True, nullable=False),
        Column('mz_imageid', String(37)), 
        Column('md5checksum', String(32)),
        Column('created_date', oracle_dialect.DATE, server_default=FetchedValue()), 
        Column('modified_date', oracle_dialect.DATE, onupdate=datetime.datetime.now), 
        Column('updated_count', Integer, default=0)    
        )
    return mozu_image_table

###########################
######################################################
###########################
### Main - Conditions ##
def main(insert_list_filepaths):
    #insert_list = []
    # for f in sys.argv:
    #     insert_list.append(f)
    import sqlalchemy
    images_insert_dict = compile_data_db_import(insert_list_filepaths)
    # Insert
    for k,v in images_insert_dict.iteritems():
        bf_imageid = v['bf_imageid']
        mz_imageid = v['mz_imageid']
        md5checksum = v['md5checksum']
        #image_metadata = v['image_metadata']
        mozu_image_table = mozu_image_table_instance()
        try:
            mz_imageid, content_response = upload_productimgs_mozu(k)
            v['mz_imageid'] = mz_imageid
            insert_records = mozu_image_table.insert(values=dict(**v))
            insert_records.execute()
            print 'Inserted --> ', v.items(), ' <-- ', insert_records
        # Update
        except sqlalchemy.exc.IntegrityError:
            print 'IntegrityError ', v
            old_mz_imageid = mozu_image_table.select(whereclause=(
                                                                (mozu_image_table.c.bf_imageid == v['bf_imageid']) 
                                                                &
                                                                (mozu_image_table.c.md5checksum <> v['md5checksum'])
                                                                )
                                                    )
            #updated_mz_imageid, content_response = upload_productimgs_mozu(k, mz_imageid=old_mz_imageid)
            updated_mz_imageid =  v['mz_imageid'].replace('-','_')
            v['mz_imageid'] = updated_mz_imageid
            update_records = mozu_image_table.update(values=dict(**v),whereclause=mozu_image_table.c.bf_imageid==v['bf_imageid'])
            res = update_records.execute()
            print res, 'Updated--> ', v.items(), ' <-- ', update_records
            pass




