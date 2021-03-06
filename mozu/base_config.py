#!/usr/bin/env python
# coding: utf-8

## Checks bash env for Debug and Testing Settings for globals()
from os import environ
globals()['PRD_ENV'] = 0  # 1=True, 0=False
if environ.get('PYDEBUG'): import pdb; pdb.set_trace()
# if environ.get('DEBUG'): globals()['DEBUG'] = 1
if environ.get('PRD_ENV'): globals()['PRD_ENV'] = 1
else: globals()['PRD_ENV'] = 0
### End Env

## STAGING CONFIGS ##
SITE_STG       = "14456"
DB_URI_STG     = 'oracle+cx_oracle://MZIMG:p1zza4me@qarac201-vip.qa.bluefly.com:1521/bfyqa1201'
MOZU_BASE_STG  = "staging-sb.mozu.com"
TENANT_STG      = '11146'
MOZU_MASTER_CATID_STG = "1"
__MOZU_AUTH_URL_STG__ = "https://home.staging.mozu.com/api/platform/applications/authtickets"
__STG_AUTH__   = {'applicationId': 'bluefly.product_images.1.0.0.release',
                 'sharedSecret': '53de2fb67cb04a95af323693caa48ddb'}

## PROD CONFIGS ##
SITE_PRD      = "16829"
DB_URI_PRD    = 'oracle+cx_oracle://MZIMG:m0zu1mages@borac102-vip.l3.bluefly.com:1521/bfyprd12'
MOZU_BASE_PRD = "mozu.com"
__MOZU_AUTH_URL_PRD__ = "https://home.mozu.com/api/platform/applications/authtickets"
TENANT_PRD    = '12106'
MOZU_MASTER_CATID_PRD = "2"
__PRD_AUTH__  = {'applicationId': 'bluefly.ImageSync.1.0.0.Release',
                'sharedSecret': '0b8eb07f0e654f2eb9d972276e0005d1'}

## STANDARD CONFIGS -- Used in both STG and PRD ##
MOZU_PROTOCOL  = "https"
MOZU_LIST_FQN  = 'files@mozu'
MOZU_DOCUMENT_TYPE_FQN =  'image@mozu'

#################################################
### ALL Variable Configs can be set above for ###
#################################################
def set_environment():
    from os import environ
    # Set Standard Env vars
    environ['MOZU_PROTOCOL'] = MOZU_PROTOCOL
    environ['MOZU_LIST_FQN'] = MOZU_LIST_FQN
    environ['MOZU_DOCUMENT_TYPE_FQN'] = MOZU_DOCUMENT_TYPE_FQN
    if globals()['PRD_ENV'] == 0:
        ## USING PRD Database in Debug, rest are STG
        environ['SQLALCHEMY_DATABASE_URI'] = DB_URI_STG
        environ['MOZU_TENANT_NAME'] = TENANT_STG
        environ['MOZU_SITE_NAME'] = SITE_STG
        environ['MOZU_BASE_URL'] = MOZU_BASE_STG
        environ['MOZU_AUTH_URL'] = __MOZU_AUTH_URL_STG__
        environ['MOZU_MASTER_CATALOG_ID'] = MOZU_MASTER_CATID_STG
        print 'SET ENV 1\tSTAGING ENV CONFIG SET \t{}\n'.format(environ.get('PRD_ENV'))
    elif globals()['PRD_ENV'] == 1:
        environ['SQLALCHEMY_DATABASE_URI'] = DB_URI_PRD
        environ['MOZU_TENANT_NAME'] = TENANT_PRD
        environ['MOZU_SITE_NAME'] = SITE_PRD
        environ['MOZU_BASE_URL'] = MOZU_BASE_PRD
        environ['MOZU_AUTH_URL'] = __MOZU_AUTH_URL_PRD__
        environ['MOZU_MASTER_CATALOG_ID'] = MOZU_MASTER_CATID_PRD
        print 'SET ENV 2\tPRODUCTION ENV CONFIG SET \t\v{}\t***RUNNING IN PRODUCTION***\n\n\n\t***RUNNING IN PRODUCTION***\n\n\n\t***RUNNING IN PRODUCTION***\n\n\nPRD_ENV Is Set to 1\n'.format(environ.get('PRD_ENV'))
    else:
        environ['SQLALCHEMY_DATABASE_URI'] = DB_URI_STG
        environ['MOZU_TENANT_NAME'] = TENANT_STG
        environ['MOZU_SITE_NAME'] = SITE_STG
        environ['MOZU_BASE_URL'] = MOZU_BASE_STG
        environ['MOZU_AUTH_URL'] = __MOZU_AUTH_URL_STG__
        environ['MOZU_MASTER_CATALOG_ID'] = MOZU_MASTER_CATID_STG
        print 'SET ENV 3\tSTAGING ENV CONFIG ASSUMED PROD env var not Set Correctly {} \n'.format(environ.get('PRD_ENV'))
    #print 'LOCAL ENV SET for MOZU:\n\n ', dict(environ)
    return

def get_mozu_client_authtoken():
    import requests, json
    set_environment()
    _auth_headers = {'Content-type': 'application/json', 'Accept-Encoding': 'gzip, deflate'}
    if globals()['PRD_ENV'] == 0:
        _auth_request = __STG_AUTH__
        _auth_url     = __MOZU_AUTH_URL_STG__

    elif globals()['PRD_ENV'] == 1:
        _auth_request = __PRD_AUTH__
        _auth_url     = __MOZU_AUTH_URL_PRD__
        #_auth_headers_prod_addition = {'x-vol-tenant': TENANT_PRD, 'x-vol-master-catalog': MOZU_MASTER_CATID_PRD }
        #_auth_headers = dict(list(_auth_headers.items()) + list(_auth_headers_prod_addition.items()))
        #print environ
    else:
        _auth_request = __STG_AUTH__
        _auth_url     = __MOZU_AUTH_URL_STG__
    _auth_response = requests.post(_auth_url, data=json.dumps(_auth_request), headers=_auth_headers, verify=False)
    print "Auth Response: {0}".format(_auth_response.status_code)
    print _auth_response.text
    print _auth_response.headers
    print '\n\n', _auth_request, _auth_headers, '\t', _auth_url
    #print '\n', environ.items(), '\n'
    _auth_response.raise_for_status()
    _auth = _auth_response.json()
    # print "Auth Ticket: {0}".format(_auth["accessToken"])
    return _auth["accessToken"] #, _auth_response.status_code



def authenticate():
    auth = get_mozu_client_authtoken()
    return auth


if __name__ == '__main__':
    set_environment()
