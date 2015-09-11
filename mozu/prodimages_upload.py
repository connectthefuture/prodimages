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
def upload_productimgs_mozu(src_filepath, mozuimageid=None):
    import requests, json
    import os.path as path
    tenant_url = "https://t11146.staging-sb.mozu.com/"
    headers = {'Content-type': 'application/json', 'x-vol-app-claims' : get_mozu_authtoken(tenant_url), 'x-vol-tenant' : '11146', 'x-vol-master-catalog' : '1' }
    #, 'x-vol-dataview-mode': 'Pending', # ??'x-vol-site' : '1', }
    document_data_api = tenant_url + "/api/content/documentlists/files@mozu/documents"
    bflyimageid   = path.basename(src_filepath) #[:-1]
    ext = bflyimageid.split('.')[-1]
    document    = ''
    document_id = ''
    document_payload = {'listFQN' : 'files@mozu', 'documentTypeFQN' : 'image@mozu', 'name' : bflyimageid, 'extension' : ext}
    document_response = requests.post(document_data_api, data=json.dumps(document_payload), headers=headers, verify=False )
    #document_response.raise_for_status()
    if document_response.status_code < 400:
        document = document_response.json()
        try:
            document_id = document["id"]
            # colorstyle    = bflyimageid[:9]
            # insert_docid_db(db_name,document_id=document_id, bflyimageid=bflyimageid, colorstyle=colorstyle, img_number=sequence)
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
        #return bflyimageid, mozuimageid
    elif document_response.status_code == 409:
        mimetype = "image/{}".format(ext.lower().replace('jpg', 'jpeg'))
        headers["Content-type"] = mimetype
        print document_id, ' <-- DocId 409 Code Numero 1'
        print 'LOCOS -->', locals()
        documentUploadApi = tenant_url + "/api/content/documentlists/files@mozu/documents/" + mozuimageid + "/content"
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
        print 'Failed with code --> ', document_response.status_code

#
def get_psycopg_connection():
    import os, psycopg2, urlparse, sys
    import psycopg2.extras
    connurl = 'postgres://cojkwmymqgbslk:0y3KViCM5vkAkiYXvvdcdHfVrT@ec2-54-204-0-120.compute-1.amazonaws.com:5432/dco1s4iscdv2as'
    os.environ["DATABASE_URL"] = connurl
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["DATABASE_URL"])
    conn = psycopg2.connect(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port)
    conn.autocommit = True
    if len(sys.argv) > 1 and sys.argv[1][:3].lower() == 'dic':
        conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return conn

# make initial table and update timestamp on modify as function and trigger of the function on the table
def init_pg_mktble_fnc_trig():
    import psycopg2
    droptable = "DROP TABLE IF EXISTS images_bfly_mozu;"
    createtbl = "CREATE TABLE IF NOT EXISTS images_bfly_mozu (id serial PRIMARY KEY, bflyimageid varchar NOT NULL, mozuimageid varchar NOT NULL, md5checksum varchar, updated_at TIMESTAMP NOT NULL DEFAULT 'now'::timestamp, update_ct bigint NOT NULL DEFAULT 1, UNIQUE(bflyimageid));"
    # Auto Mod time Now Func and trig
    createfunc_nowonupdate = "CREATE OR REPLACE FUNCTION update_updated_at_column() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN NEW.updated_at := NOW(); RETURN NEW; END; $$;"
    createtrig_nowonupdate = "CREATE TRIGGER images_bfly_mozu_updated_at_column BEFORE INSERT OR UPDATE ON images_bfly_mozu FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();"

    create_timestamperfunc = "CREATE OR REPLACE FUNCTION trig_time_stamper() RETURNS trigger AS $$ BEGIN NEW.updated_at := CURRENT_TIMESTAMP; RETURN NEW; END; $$ LANGUAGE plpgsql VOLATILE;"
    create_timestampertrig = "CREATE TRIGGER trig_1 BEFORE INSERT OR UPDATE ON images_bfly_mozu FOR EACH ROW EXECUTE PROCEDURE trig_time_stamper(); OF updated_at"

    # Auto incr after modify
    createfunc_tablehits = "CREATE SEQUENCE tablehits INCREMENT BY 1 MINVALUE 1;"
    # createfunc_incronupdate = "CREATE SEQUENCE update_ct INCREMENT BY 1 MINVALUE 1;
    createfunc_incronupdate = "CREATE OR REPLACE FUNCTION incr_update_ct() RETURNS trigger LANGUAGE plpgsql AS $BODY$ BEGIN NEW.updated_ct := nextval('update_ct'); RETURN NEW; END; $BODY$;"
    createtrig_incronupdate = "CREATE TRIGGER images_bfly_mozu_incr_update_ct BEFORE INSERT OR UPDATE ON images_bfly_mozu FOR EACH ROW EXECUTE PROCEDURE incr_update_ct();"
    ## Below used if Table exists -- which it obviously should since I just called the mktble above
    # createfuncalter_incronupdate = "ALTER TABLE images_bfly_mozu ALTER update_ct SET DEFAULT nextval('update_ct'); "

    conn = get_psycopg_connection()
    cur = conn.cursor()

    # drop if exists to create a new one
    #cur.execute(droptable)
    #conn.commit()

    cur.execute(createtbl)
    conn.commit()

    try:
        #cur.execute(createfunc_nowonupdate)
        #cur.execute(createtrig_nowonupdate)
        #conn.commit()
        cur.execute(create_timestamperfunc)
        cur.execute(create_timestampertrig)
        conn.commit()
        cur.execute(createfunc_incronupdate)
        cur.execute(createtrig_incronupdate)
        conn.commit()
        #cur.execute(createfuncalter_incronupdate)
        #conn.commit()
    except psycopg2.ProgrammingError, e:
        print 'Passing Psycopg2 ProgErr...%s' % e
        pass
    finally:
        if conn:
            conn.commit()
            conn.close()

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
    current_dt = datetime.datetime.strptime(datetime.datetime.now(), '%Y-%m-%d')
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
### postgres Funcs
# Store Key in pgsql
def pgsql_insert_bflyimageid_mozuimageid(bflyimageid, mozuimageid, md5checksum=''):
    # HERE IS THE IMPORTANT PART, by specifying a name for the cursor
    # psycopg2 creates a server-side cursor, which prevents all of the
    # records from being downloaded at once from the server
    try:
        conn = get_psycopg_connection()
        cur = conn.cursor()
        ##cur.execute("INSERT INTO images_bfly_mozu (bflyimageid, mozuimageid, md5checksum) VALUES (%s, %s, %s) ;", (bflyimageid, mozuimageid, md5checksum))
        cur.execute("INSERT INTO images_bfly_mozu(bflyimageid, mozuimageid, md5checksum) VALUES(%s, %s, %s) ON CONFLICT UPDATE SET mozuimageid = 'mozuimageidVals';", (bflyimageid, mozuimageid, md5checksum))
        conn.commit()
        conn.close()
    except IndexError:
        pass

#########
# Update
def pgsql_update_bflyimageid_mozuimageid(bflyimageid, mozuimageid, md5checksum=''):
    # HERE IS THE IMPORTANT PART, by specifying a name for the cursor
    # psycopg2 creates a server-side cursor, which prevents all of the
    # records from being downloaded at once from the server
    try:
        conn = get_psycopg_connection()
        cur = conn.cursor()
        #  SET update_ct = update_ct + 1
        cur.execute("UPDATE images_bfly_mozu SET mozuimageid=%s, SET md5checksum=%s, SET updated_ct = (updated_ct + 1) WHERE bflyimageid=%s;", (mozuimageid, md5checksum, bflyimageid))
        conn.commit()
        conn.close()
    except IndexError:
        pass

# Get mozu img ID from bfly file id
def pgsql_get_mozuimageid_bflyimageid(bflyimageid):
    conn = get_psycopg_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT mozuimageid FROM images_bfly_mozu WHERE bflyimageid = '{}'".format(bflyimageid))
        mozuimageid = cur.fetchone()
        if mozuimageid:
            return mozuimageid
        else:
            return False
    except TypeError:
        return False

# Get mozu img url
def pgsql_get_mozuimageurl_bflyimageid(bflyimageid, destpath=None):
    import requests
    mozu_files_prefix = 'http://cdn-stg-sb.mozu.com/11146-m1/cms/files/'
    mozuimageid = pgsql_get_mozuimageid_bflyimageid(bflyimageid)
    mozuimageurl = "{}{}".format(mozu_files_prefix, mozuimageid)
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
def pgsql_validate_md5checksum(md5checksum, bflyimageid=None):
    import requests
    conn = get_psycopg_connection()
    cur = conn.cursor()
    result = ''
    if bflyimageid:
        print 'Not NONE --', bflyimageid
        cur.execute("SELECT bflyimageid FROM images_bfly_mozu WHERE md5checksum = %s AND bflyimageid = %s", (md5checksum, bflyimageid))
        result = cur.fetchone()
    else:
        print 'NONE --', bflyimageid
        cur.execute("SELECT bflyimageid FROM images_bfly_mozu WHERE md5checksum = '{}'".format(md5checksum))
        result = cur.fetchone()
        ## If Value >1
    print bflyimageid, result,  '--- bflyImageID -- result'

    conn.commit()
    conn.close()
    if result:
        return result
    else: return ''

## Validate file name only
def pgsql_validate_bflyimageid(bflyimageid=None):
    import requests
    conn = get_psycopg_connection()
    cur = conn.cursor()
    result = ''
    if bflyimageid is not None:
        print 'Not NONE --', bflyimageid
        cur.execute("SELECT mozuimageid FROM images_bfly_mozu WHERE bflyimageid = '{}'".format(bflyimageid))
        result = cur.fetchone()
    conn.commit()
    conn.close()
    if result:
        return result
    else: return ''

# if result:
# try:
#         mozu_files_prefix = 'http://cdn-stg-sb.mozu.com/11146-m1/cms/files/'
#         mozuimageid = pgsql_get_mozuimageid_bflyimageid(bflyimageid)
#         mozuimageurl = "{}{}".format(mozu_files_prefix, mozuimageid)
#         return bflyimageid, mozuimageurl,
#     except TypeError:
#         return ''
# else:
#     return ''

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
def main_update_put(bflyimageid, mozuimageid,md5checksum):


    ## Finally Store New mozuiD and md5checksum
    pgsql_update_bflyimageid_mozuimageid(bflyimageid, mozuimageid,md5checksum)
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
        bflyimageid = path.basename(src_filepath)  # .split('.')[0]
    else:
        bflyimageid = None
    md5checksum = md5_checksumer(src_filepath)
    mozuimageid = ''
    md5result = pgsql_validate_md5checksum(md5checksum, bflyimageid=bflyimageid)
    mozuimageid = pgsql_validate_bflyimageid(bflyimageid=bflyimageid)
    ## Finished collecting k/v data to send now send if md5result returns False (meaning we dont have an image for this yet)
    if not md5result and not mozuimageid:
        try:
            mozuimageid, content_response = upload_productimgs_mozu(src_filepath)
            pgsql_insert_bflyimageid_mozuimageid(bflyimageid, mozuimageid, md5checksum)
            print 'bflyimageid={}\nmozuimageid={}\nmd5checksum={}'.format(bflyimageid, mozuimageid, md5checksum)
            return mozuimageid, bflyimageid
        except TypeError, e:
            print '\n\t...', src_filepath, ' None TypeError --> ', e
            pass
        finally:
            print('Completed ', bflyimageid, md5checksum)
    elif mozuimageid and not md5result:
        updated_mozuimageid, content_response = upload_productimgs_mozu(src_filepath,mozuimageid=mozuimageid)
        pgsql_update_bflyimageid_mozuimageid(bflyimageid, updated_mozuimageid, md5checksum=md5checksum)
    else:
        print md5result, ' \n\t<-- Duplicated - Passing -- Exists -- with --> ', bflyimageid

# Query/Display previous/currentDB info
def main_retrieve_get(**kwargs):
    args_ct=len(kwargs.items())
    bflyimageid = kwargs.get('bflyimageid')
    mozu_files_prefix = 'http://cdn-stg-sb.mozu.com/11146-m1/cms/files/'
    mozuimageid = pgsql_get_mozuimageid_bflyimageid(bflyimageid)
    mozuimageurl = "{}{}".format(mozu_files_prefix,mozuimageid)
    print 'bflyimageid={}\nmozuimageid={}'.format(bflyimageid, mozuimageid)
    return (mozuimageurl, bflyimageid,)


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
        bflyimageid = sys.argv[1]
        try:
            destpath = sys.argv[2]
            if path.isfile(destpath):
                pgsql_get_mozuimageurl_bflyimageid(bflyimageid, destpath=destpath)
            elif path.isdir(destpath):
                pgsql_get_mozuimageurl_bflyimageid(bflyimageid, destpath=path.join(destpath, bflyimageid))
        except IndexError:
            destpath = ''
