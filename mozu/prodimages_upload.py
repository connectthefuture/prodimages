#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

def get_psycopg_cursor():
    import os, psycopg2, urlparse
    connurl = 'postgres://cojkwmymqgbslk:0y3KViCM5vkAkiYXvvdcdHfVrT@ec2-54-204-0-120.compute-1.amazonaws.com:5432/dco1s4iscdv2as'
    os.environ["DATABASE_URL"] = connurl
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["DATABASE_URL"])
    conn = psycopg2.connect( database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port)
    cur = conn.cursor()
    return cur

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
        content_response = requests.put(document_content_api, data=file_data, headers=headers, verify=False )
        print "document ID: %s" % document_id
        print "document_payload: %s" % document_payload
        print "Document content upload Response: %s" % content_response.text
        #document_response.raise_for_status()
        return document_id, content_response
        #return bflyimageid, mozuimageid
    else:
        print 'Failed with code --> ', document_response.status_code

def pgsql_insert_bflyimageid_mozuimageid(bflyimageid, mozuimageid, md5checksum=''):
    # HERE IS THE IMPORTANT PART, by specifying a name for the cursor
    # psycopg2 creates a server-side cursor, which prevents all of the
    # records from being downloaded at once from the server
    cur = get_psycopg_cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS images_bfly_mozu (id serial PRIMARY KEY, bflyimageid varchar, mozuimageid varchar, md5checksum varchar, md5timestamp timestamp DEFAULT current_timestamp, UNIQUE(bflyimageid, md5checksum));")
    try:
        cur.execute("INSERT INTO images_bfly_mozu (bflyimageid, mozuimageid, md5checksum) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE mozuimageid = VALUES(mozuimageid), md5checksum = VALUES(md5checksum);", (bflyimageid, mozuimageid, md5checksum))
    except:
        pass

def pgsql_get_mozuimageid_bflyimageid(bflyimageid):
    import requests
    cur = get_psycopg_cursor
    mozuimageid = cur.execute("SELECT mozuimageid FROM images_bfly_mozu WHERE bflyimageid = '%s'", (bflyimageid))
    if mozuimageid:
        return mozuimageid
    else:
        return False

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

def pgsql_get_validate_md5checksum(md5checksum):
    import requests
    cur = get_psycopg_cursor
    bflyimageid = cur.execute("SELECT bflyimageid, mozuimageid FROM images_bfly_mozu WHERE md5checksum = '%s'", (md5checksum))
    if bflyimageid:
        mozu_files_prefix = 'http://cdn-stg-sb.mozu.com/11146-m1/cms/files/'
        mozuimageid = pgsql_get_mozuimageid_bflyimageid(bflyimageid)
        mozuimageurl = "{}{}".format(mozu_files_prefix,mozuimageid)
        return (bflyimageid, mozuimageurl,)
    else:
        return False

def main_upload_post(src_filepath):
    import os.path as path
    mozuimageid, content_response = upload_productimgs_mozu(src_filepath)
    bflyimageid = path.basename(src_filepath)  #.split('.')[0]
    md5checksum = md5_checksumer(src_filepath)
    print 'bflyimageid={}\nmozuimageid={}'.format(bflyimageid, mozuimageid)
    result = pgsql_insert_bflyimageid_mozuimageid(bflyimageid, mozuimageid)
    print result
    return mozuimageid, bflyimageid

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

