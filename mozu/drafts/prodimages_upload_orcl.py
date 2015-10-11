#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
def upload_productimgs_mozu(src_filepath, mz_imageid=None):
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
        mz_imageid = orcl_get_mz_imageid_bf_imageid(bf_imageid)
        if mz_imageid is not None:
            print 'Old MozuID Retrieved from ORCL', mz_imageid
            documentUploadApi = tenant_url + "/api/content/documentlists/files@mozu/documents/" + mz_imageid + "/content"
            # files = {'media': open("c:\mozu-dc-logo.png", "rb")};
            file_data = open(src_filepath, 'rb').read()
            headers["Content-type"] = mimetype #"image/png";
            content_response = requests.put(documentUploadApi, data=file_data, headers=headers, verify=False);
            document = content_response.json()
            document_id = document["id"]
            print document_id, ' <-- DocId 409 Code'
            print '409 Err --> Bluefly Filename Already in Mozu, if you are trying to update the image, this is not the way.\n\t%s' % src_filepath
            ## TODO: 1)  On duplicate file in mozu, check PGSQL by Filename and compare stored MD5 with current MD5.
            ## TODO: 1A) If same MD5 skip and return MOZUID, else if different.....
            ## TODO  2)  Update Mozu stored image using main_update_put(src_filepath), sending to an "update" endpoint(need to get uri)
            ## TODO: 3)  Update PGSQL MOZUID + MD5
            ## TODO: 4)  Bust image cache on updates in MOZU by forcing MEDIA_VERSION to increment -- Need API endpoint to PM or its going to be super hackey.
            pass
        else:
            print 'MZID is None'
    else:
        print 'Failed with code --> ', document_response.status_code

# make initial table and update timestamp on modify as function and trigger of the function on the table
# def init_pg_mktble_fnc_trig():
#     import psycopg2
#     droptable = "DROP TABLE IF EXISTS MOZU_IMAGE;"
#     createtbl = "CREATE TABLE IF NOT EXISTS MOZU_IMAGE (id serial PRIMARY KEY, bf_imageid varchar NOT NULL, mz_imageid varchar NOT NULL, md5checksum varchar, updated_at TIMESTAMP NOT NULL DEFAULT 'now'::timestamp, update_ct bigint NOT NULL DEFAULT 1, UNIQUE(bf_imageid));"
#     # Auto Mod time Now Func and trig
#     createfunc_nowonupdate = "CREATE OR REPLACE FUNCTION update_updated_at_column() RETURNS trigger BEGIN NEW.updated_at := SYSDATE; RETURN NEW; END;"
#     createtrig_nowonupdate = "CREATE TRIGGER MOZU_IMAGE_updated_at_column BEFORE INSERT OR UPDATE ON MOZU_IMAGE FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();"
#
#     create_timestamperfunc = "CREATE OR REPLACE FUNCTION trig_time_stamper() RETURNS trigger BEGIN NEW.updated_at := CURRENT_TIMESTAMP; RETURN NEW; END;"
#     create_timestampertrig = "CREATE TRIGGER trig_1 BEFORE INSERT OR UPDATE ON MOZU_IMAGE FOR EACH ROW EXECUTE PROCEDURE trig_time_stamper(); OF updated_at"
#
#     # Auto incr after modify
#     #createfunc_tablehits = "CREATE SEQUENCE tablehits INCREMENT BY 1 MINVALUE 1;"
#     # createfunc_incronupdate = "CREATE SEQUENCE update_ct INCREMENT BY 1 MINVALUE 1;
#     #createfunc_incronupdate = "CREATE OR REPLACE FUNCTION incr_update_ct() RETURNS trigger BEGIN NEW.UPDATED_COUNT := nextval('update_ct'); RETURN NEW; END; $BODY$;"
#     #createtrig_incronupdate = "CREATE TRIGGER MOZU_IMAGE_incr_update_ct BEFORE INSERT OR UPDATE ON MOZU_IMAGE FOR EACH ROW EXECUTE PROCEDURE incr_update_ct();"
#     ## Below used if Table exists -- which it obviously should since I just called the mktble above
#     # createfuncalter_incronupdate = "ALTER TABLE MOZU_IMAGE ALTER update_ct SET DEFAULT nextval('update_ct'); "
#
#     conn = get_mzimg_oracle_connection()
#     cur = conn
#
#     # drop if exists to create a new one
#     #cur.execute(droptable)
    #conn.commit()
#
#     cur.execute(createtbl)
    ## conn.commit()
#
#     try:
#         cur.execute(createfunc_nowonupdate)
#         cur.execute(createtrig_nowonupdate)
#         conn.commit()
#         cur.execute(create_timestamperfunc)
#         cur.execute(create_timestampertrig)
#         conn.commit()
#         cur.execute(createfunc_incronupdate)
#         cur.execute(createtrig_incronupdate)
#         conn.commit()
#         cur.execute(createfuncalter_incronupdate)
#         conn.commit()
#     except psycopg2.ProgrammingError, e:
#         print 'Passing Psycopg2 ProgErr...%s' % e
#         pass
#     finally:
#         if conn:
#             conn.commit()
#             conn.close()

### Utility Funx - Get File Data
## util func calcs md5 of file
def md5_checksumer(src_filepath):
    import hashlib
    import os.path as path
    if path.isfile(src_filepath):
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

## Extracts the image metadata from file
def get_exif_all_data(src_filepath):
    import exiftool
    with exiftool.ExifTool() as et:
        metadata = et.get_metadata(src_filepath)  # ['XMP:DateCreated'][:10].replace(':','-')
    return metadata

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

####################
### oracle Funcs
##
########################### Replaced By Alchemy ############################
def get_mzimg_oracle_connection():
    import sqlalchemy,sys
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://MZIMG:p1zza4me@qarac201-vip.qa.bluefly.com:1521/bfyqa1201')
    cur = orcl_engine.raw_connection().cursor()
    conn = orcl_engine.connect()
    print(dir(conn))
    return conn, cur

# Store Key in pgsql
def orcl_insert_bf_imageid_mz_imageid(bf_imageid, mz_imageid, md5checksum=''):
    # HERE IS THE IMPORTANT PART, by specifying a name for the cursor
    # psycopg2 creates a server-side cursor, which prevents all of the
    # records from being downloaded at once from the server
    import datetime, sqlalchemy
    dt = datetime.datetime.now()
    upsert_timestamp =  datetime.datetime.strftime(dt, "%Y-%m-%d %H:%M:%S")
    upsert_timestamp = datetime.datetime.strftime(dt, "%m%d%Y")
    try:
        conn, cur = get_mzimg_oracle_connection()
        #cur = conn
        query = "INSERT INTO MOZU_IMAGE (bf_imageid, mz_imageid, md5checksum) VALUES ('{0}', '{1}', '{2}');".format(bf_imageid, mz_imageid, md5checksum)
        print query, 'QUERY'
        cur.execute(query)
        #cur.execute("INSERT INTO MOZU_IMAGE(bf_imageid, mz_imageid, md5checksum, CREATED_DATE) VALUES(%s, %s, %s, TO_DATE('%s','MMDDYY'));", (bf_imageid, mz_imageid, md5checksum, upsert_timestamp))
        ## conn.commit()
        conn.close()
    except IndexError:
        pass

#########
# Update
def orcl_update_bf_imageid_mz_imageid(bf_imageid, mz_imageid, md5checksum=''):
    # HERE IS THE IMPORTANT PART, by specifying a name for the cursor
    # psycopg2 creates a server-side cursor, which prevents all of the
    # records from being downloaded at once from the server
    import datetime
    dt = datetime.datetime.now()
    upsert_timestamp = datetime.datetime.strftime(dt, "%Y-%m-%d %H:%M:%S")
    upsert_timestamp = datetime.datetime.strftime(dt, "%m%d%Y")
    try:
        conn, cur = get_mzimg_oracle_connection()
        #cur = conn
        #  SET update_ct = update_ct + 1
        cur.execute("""UPDATE MOZU_IMAGE
                        SET mz_imageid='{0}',
                        md5checksum='{1}',
                        MODIFIED_DATE=TO_DATE('{2}','MMDDYY'),
                        UPDATED_COUNT=(UPDATED_COUNT + 1)
                        WHERE bf_imageid='{3}';""".format(mz_imageid, md5checksum, upsert_timestamp, bf_imageid))
        ## conn.commit()
        conn.close()
    except IndexError:
        pass

# Get mozu img ID from bfly file id
def orcl_get_mz_imageid_bf_imageid(bf_imageid):
    conn, cur = get_mzimg_oracle_connection()
    #cur = conn
    print bf_imageid,' BFIMGID'
    try:
        query = """SELECT mz_imageid FROM MOZU_IMAGE WHERE bf_imageid='{0}';""".format(bf_imageid)
        print query
        res = cur.execute(query)
        mz_imageid = [ r for r in res ]
        if len(mz_imageid) > 1:
            return mz_imageid
        else:
            return False
    except TypeError:
        return False

# Get mozu img url
def orcl_get_mozuimageurl_bf_imageid(bf_imageid, destpath=None):
    import requests
    mozu_files_prefix = 'http://cdn-stg-sb.mozu.com/11146-m1/cms/files/'
    mz_imageid = orcl_get_mz_imageid_bf_imageid(bf_imageid)
    mozuimageurl = "{}{}".format(mozu_files_prefix, mz_imageid)
    res = requests.get(mozuimageurl)
    if res.status_code >= 400:
        return ''
    elif not destpath:
        return res
    else:
        with open(destpath) as f:
            f.write(res.content)
        return destpath

# Validate new file before insert or perform update function on failed validation, due to duplicate key in DB
def orcl_validate_md5checksum(md5checksum, bf_imageid=None):
    import requests
    conn, cur = get_mzimg_oracle_connection()
    #cur = conn
    result = ''
    if bf_imageid:
        print 'Not NONE --', bf_imageid
        cur.execute("SELECT bf_imageid FROM MOZU_IMAGE WHERE md5checksum = '{0}' AND bf_imageid = '{1}'".format(md5checksum, bf_imageid))
        result = cur.fetchone()
    else:
        print 'NONE --', bf_imageid
        cur.execute("SELECT bf_imageid FROM MOZU_IMAGE WHERE md5checksum = '{0}'".format(md5checksum))
        result = cur.fetchone()
        ## If Value >1
    print bf_imageid, result,  '--- bf_imageid -- result'

    #conn.commit()
    conn.close()
    if result:
        return result
    else: return ''

## Validate file name only
def orcl_validate_bf_imageid(bf_imageid=None):
    import requests
    conn, cur = get_mzimg_oracle_connection()
    #cur = conn
    result = ''
    if bf_imageid is not None:
        print 'Not NONE --', bf_imageid
        cur.execute("SELECT mz_imageid FROM MOZU_IMAGE WHERE bf_imageid = '{0}'".format(bf_imageid))
        result = cur.fetchone()
    #conn.commit()
    conn.close()
    if result:
        return result
    else: return ''

# if result:
# try:
#         mozu_files_prefix = 'http://cdn-stg-sb.mozu.com/11146-m1/cms/files/'
#         mz_imageid = orcl_get_mz_imageid_bf_imageid(bf_imageid)
#         mozuimageurl = "{}{}".format(mozu_files_prefix, mz_imageid)
#         return bf_imageid, mozuimageurl,
#     except TypeError:
#         return ''
# else:
#     return ''

###################### Now The Alchemy Way ####################



#######################
##########################################################
########################
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
##########################################################
## --> cache bursting to incr the media_version ID# -- ###
def update_pm_photodate_incr_version_hack(src_filepath):
    import requests
    if len(src_filepath) == 9 and src_filepath.isdigit():
        colorstyle = src_filepath
    else:
        colorstyle = path.basename(src_filepath)[:9]
    update_url = 'http://dmzimage01.l3.bluefly.com:8080/photo/{0}'.format(colorstyle)
    data = {"sample_image": "Y", "photographed_date": "now"}
    res = requests.put(update_url, data=data)
    return res
##########################################################
def main_update_put(bf_imageid, mz_imageid,md5checksum):

    ## Finally Store New mozuiD and md5checksum
    orcl_update_bf_imageid_mz_imageid(bf_imageid, mz_imageid,md5checksum)
    return
##########################################################
# ### Main Combined Post or Get -- TODO: --> main_update_put(src_filepath)
# full uploading cmdline shell script, file as sys argv
def main_upload_post(src_filepath):
    import os.path as path
    ##############################
    # remove db setup funcs after init release into prod
    # try:
    #     init_pg_mktble_fnc_trig()
    # except:
    #     pass
    ##############################
    ## Convert it to jpg if not one (ie png, tiff, gif)
    ext = src_filepath.split('.')[-1].lower().replace('jpeg','jpg')
    src_basename = path.basename(src_filepath)
    if ext == 'jpg':
        pass
    else:
        src_filepath = magick_convert_to_jpeg(src_filepath, destdir=None)
    if src_basename[:9].isdigit() and ext:
        bf_imageid = path.basename(src_filepath)  # .split('.')[0]
    else:
        bf_imageid = ''
    md5checksum = md5_checksumer(src_filepath)
    mz_imageid = ''

    args = [
        {'bf_imageid': bf_imageid },
        {'mz_imageid': mz_imageid },
        {'md5checksum': md5checksum }
        ]

    #md5colorstyle_exists = orcl_validate_md5checksum(md5checksum, bf_imageid=bf_imageid)
    # 1A Validate md5 # TODO: NEW # sqlalchemy 
    if bf_imageid: 
        OLDbf_imageid = select('bf_imageid').where('md5checksum'=md5checksum)
        if bf_imageid == OLDbf_imageid:  
            md5colorstyle_exists = md5checksum
        else: 
            md5colorstyle_exists = ''


    #md5colorstyle_exists = orcl_validate_bf_imageid(bf_imageid=bf_imageid).execute()
    # 1B Validate bf_imageid_exists # TODO: NEW # sqlalchemy 
    bf_imageid_exists = select('mz_imageid').where('bf_imageid'=bf_imageid).execute()    
    if bf_imageid_exists:
        if bf_imageid_exists.where('md5checksum'!=md5checksum).execute():
            mz_imageid = select('mz_imageid').where('bf_imageid'=bf_imageid)


    import json
    json_insert = json.dumps(args)

    ## Finished collecting k/v data to send now send if md5colorstyle_exists returns False (meaning we dont have an image for this yet)
    if not md5colorstyle_exists and not bf_imageid_exists:
        try:
            mz_imageid, content_response = upload_productimgs_mozu(src_filepath)
            orcl_insert_bf_imageid_mz_imageid(bf_imageid, mz_imageid, md5checksum)
            # 2 Insert # TODO: NEW # sqlalchemy table.insert()
            printoutput = 'bf_imageid={}\tmz_imageid={}\tmd5checksum={}\n'.format(bf_imageid, mz_imageid, md5checksum).split()
            mr_logger('/mnt/mozu_upload.txt', printoutput)
            print printoutput, ' Line-420RESULT'
            return mz_imageid, bf_imageid
        except TypeError, e:
            print '\n\t...', src_filepath, ' None TypeError --> ', e
            pass
        #finally:
        #    print('Completed ', bf_imageid, md5checksum)
    elif bf_imageid_exists and not md5colorstyle_exists:
        updated_mz_imageid, content_response = upload_productimgs_mozu(src_filepath, mz_imageid=mz_imageid)
        orcl_update_bf_imageid_mz_imageid(bf_imageid, updated_mz_imageid, md5checksum=md5checksum)
        # 3 Update # TODO: NEW # sqlalchemy table.update()
    else:
        print md5colorstyle_exists, ' \n\t<-- Duplicated - Passing -- Exists -- with --> ', bf_imageid


# Query/Display previous/currentDB info
def main_retrieve_get(**kwargs):
    args_ct=len(kwargs.items())
    bf_imageid = kwargs.get('bf_imageid')
    mozu_files_prefix = 'http://cdn-stg-sb.mozu.com/11146-m1/cms/files/'
    mz_imageid = orcl_get_mz_imageid_bf_imageid(bf_imageid)
    mozuimageurl = "{}{}".format(mozu_files_prefix,mz_imageid)
    print 'bf_imageid={}\nmz_imageid={}'.format(bf_imageid, mz_imageid)
    return (mozuimageurl, bf_imageid,)


if __name__ == '__main__':
    import sys
    import os.path as path
    ext = '.jpg'
    if path.isfile(sys.argv[1]):
        src_filepath = sys.argv[1]
        ext = src_filepath.split('.')[-1]
        result = main_upload_post(src_filepath)
        print "Result --> ", result, src_filepath
    elif sys.argv[1][:9].isdigit() and len(sys.argv[1]) < 20:
        bf_imageid = sys.argv[1]
        try:
            destpath = sys.argv[2]
            if path.isfile(destpath):
                orcl_get_mozuimageurl_bf_imageid(bf_imageid, destpath=destpath)
            elif path.isdir(destpath):
                orcl_get_mozuimageurl_bf_imageid(bf_imageid, destpath=path.join(destpath, bf_imageid))
        except IndexError:
            destpath = ''
