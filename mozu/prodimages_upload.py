#!/usr/bin/env python
# -*- coding: utf-8 -*-

def get_psycopg_cursor():
    import os, psycopg2, urlparse
    connurl = 'postgres://cojkwmymqgbslk:0y3KViCM5vkAkiYXvvdcdHfVrT@ec2-54-204-0-120.compute-1.amazonaws.com:5432/dco1s4iscdv2as'
    os.environ["DATABASE_URL"] = connurl
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["DATABASE_URL"])
    conn = psycopg2.connect( database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port)
    return conn

# make initial table and update timestamp on modify as function and trigger of the function on the table
def init_pg_mktble_fnc_trig():
    import psycopg2
    createtbl = "CREATE TABLE IF NOT EXISTS images_bfly_mozu (id serial PRIMARY KEY, bflyimageid varchar NOT NULL, mozuimageid varchar NOT NULL, md5checksum varchar, updated_at TIMESTAMP NOT NULL DEFAULT 'now'::timestamp, seq_update_ct int NOT NULL DEFAULT 1, UNIQUE(bflyimageid, md5checksum));"
    # Auto Mod time Now Func and trig
    createfunc_nowonupdate = "CREATE OR REPLACE FUNCTION update_updated_at_column() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN NEW.updated_at = NOW(); RETURN NEW; END; $$;"
    createtrig_nowonupdate = "CREATE SEQUENCE seq_update_ct INCREMENT BY 1 MINVALUE 1; CREATE TRIGGER images_bfly_mozu_updated_at_modtime BEFORE UPDATE ON images_bfly_mozu FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();"
    # Auto incr after modify
    # createfunc_incronupdate = "CREATE SEQUENCE seq_update_ct INCREMENT BY 1 MINVALUE 1;"
    createfunc_incronupdate = "CREATE OR REPLACE FUNCTION incr_updated_ct() RETURNS trigger AS $BODY$ BEGIN NEW.updated_ct := nextval('seq_update_ct'); RETURN NEW; END; $BODY$ LANGUAGE 'plpgsql';"
    createtrig_incronupdate = "CREATE TRIGGER images_bfly_mozu_incr_updated_ct BEFORE UPDATE ON images_bfly_mozu FOR EACH ROW EXECUTE PROCEDURE incr_updated_ct();"
    ## Below used if Table exists -- which it obviously should since I just called the mktble above
    createfuncalter_incronupdate = "ALTER TABLE images_bfly_mozu ALTER seq_update_ct SET DEFAULT nextval('seq_update_ct'); "

    conn = get_psycopg_cursor()
    cur = conn.cursor()
    cur.execute(createtbl)
    conn.commit()

    try:

        cur.execute(createfunc_nowonupdate)
        cur.execute(createtrig_nowonupdate)
        #conn.commit()
        cur.execute(createtrig_incronupdate)
        cur.execute(createfunc_incronupdate)
        #conn.commit()
    except psycopg2.ProgrammingError:
        print 'Passing Psycopg2 ProgErr...'
        pass

    cur.execute(createfuncalter_incronupdate)
    conn.commit()
    conn.close()

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
    # TODO add Validation(regex) to prevent unwanted updates
    ##
    print "Auth Response: %s" % auth_response.status_code
    auth_response.raise_for_status()
    auth = auth_response.json()
    print "Auth Ticket: %s" % auth["accessToken"]
    return auth["accessToken"]

# Upload
def upload_productimgs_mozu(src_filepath):
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
        print 'Bluefly Filename Already in Mozu, if you are trying to update the image, this is not the way.'
        ## TODO: 1)  On duplicate file in mozu, check PGSQL by Filename and compare stored MD5 with current MD5.
        ## TODO: 1A) If same MD5 skip and return MOZUID, else if different.....
        ## TODO  2)  Update Mozu stored image using main_update_put(src_filepath), sending to an "update" endpoint(need to get uri)
        ## TODO: 3)  Update PGSQL MOZUID + MD5
        ## TODO: 4)  Bust image cache on updates in MOZU by forcing MEDIA_VERSION to increment -- Need API endpoint to PM or its going to be super hackey.
        pass
    else:
        print 'Failed with code --> ', document_response.status_code

####################
### postgres Funcs
# Store Key in pgsql
def pgsql_insert_bflyimageid_mozuimageid(bflyimageid, mozuimageid, md5checksum=''):
    # HERE IS THE IMPORTANT PART, by specifying a name for the cursor
    # psycopg2 creates a server-side cursor, which prevents all of the
    # records from being downloaded at once from the server
    try:
        conn = get_psycopg_cursor()
        cur = conn.cursor()
        cur.execute("INSERT INTO images_bfly_mozu (bflyimageid, mozuimageid, md5checksum) VALUES (%s, %s, %s) ;", (bflyimageid, mozuimageid, md5checksum))
        conn.commit()
        conn.close()
    except IndexError:
        pass

# UPdate
def pgsql_update_bflyimageid_mozuimageid(bflyimageid, mozuimageid, md5checksum=''):
    # HERE IS THE IMPORTANT PART, by specifying a name for the cursor
    # psycopg2 creates a server-side cursor, which prevents all of the
    # records from being downloaded at once from the server
    try:
        conn = get_psycopg_cursor()
        cur = conn.cursor()
        cur.execute("UPDATE images_bfly_mozu SET mozuimageid=%s, SET md5checksum=%s WHERE bflyimageid=%s;", (mozuimageid, md5checksum, bflyimageid))
        conn.commit()
        conn.close()
    except IndexError:
        pass

# Get mozu img ID from bfly file id
def pgsql_get_mozuimageid_bflyimageid(bflyimageid):
    conn = get_psycopg_cursor()
    cur = conn.cursor()
    mozuimageid = cur.execute("SELECT mozuimageid FROM images_bfly_mozu WHERE bflyimageid = '%s'", (bflyimageid))
    if mozuimageid:
        return mozuimageid
    else:
        return False

# Get mozu img url
def pgsql_get_mozuimageurl_bflyimageid(bflyimageid, destpath=None):
    import requests
    mozu_files_prefix = 'http://cdn-stg-sb.mozu.com/11146-m1/cms/files/'
    mozuimageid = pgsql_get_mozuimageid_bflyimageid(bflyimageid)
    mozuimageurl = "{}{}".format(mozu_files_prefix,mozuimageid)
    res = requests.get(mozuimageurl)
    if res.status_code >= 400:
        return False
    elif not destpath:
        return res
    else:
        with open(destpath) as f:
            f.write(res.content)
        return destpath

# Validate new file before insert or perform update function on failed validation, due to duplicate key in DB
def pgsql_get_validate_md5checksum(md5checksum, bflyimageid=None):
    import requests
    cur, conn = get_psycopg_cursor()
    if bflyimageid is not None:
        cur.execute("SELECT bflyimageid FROM images_bfly_mozu WHERE md5checksum = '%s' AND bflyimageid = '%s'", (md5checksum, bflyimageid))
        bflyimageid = cur.fetchall()
    else:
        cur.execute("SELECT bflyimageid FROM images_bfly_mozu WHERE md5checksum = '%s'", (md5checksum))
        bflyimageid = cur.fetchall()
        ## If Value >1
    conn.commit()
    conn.close()
    if bflyimageid:
        mozu_files_prefix = 'http://cdn-stg-sb.mozu.com/11146-m1/cms/files/'
        mozuimageid = pgsql_get_mozuimageid_bflyimageid(bflyimageid)
        mozuimageurl = "{}{}".format(mozu_files_prefix,mozuimageid)
        return (bflyimageid, mozuimageurl,)
    else:
        return False

### Main Combined Post or Get -- TODO: --> main_update_put(src_filepath)
# full uploading cmdline shell script, file as sys argv
def main_upload_post(src_filepath):
    import os.path as path
    try:
        mozuimageid, content_response = upload_productimgs_mozu(src_filepath)
        bflyimageid = path.basename(src_filepath)  #.split('.')[0]
        md5checksum = md5_checksumer(src_filepath)
        init_pg_mktble_fnc_trig()
        pgsql_insert_bflyimageid_mozuimageid(bflyimageid, mozuimageid, md5checksum)
        print 'bflyimageid={}\nmozuimageid={}\nmd5checksum={}'.format(bflyimageid, mozuimageid, md5checksum)
        return mozuimageid, bflyimageid
    except TypeError:
        print '\n\t...', src_filepath, ' None TypeError'
        pass

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
    #src_filepath = '/Users/johnb/Desktop/misc_tests/orig/354394801_5.jpg'
    ext = '.jpg'
    #src_filepath = '/Users/johnb/Desktop/misc_tests/croppedtest/out/362203805.png'
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

