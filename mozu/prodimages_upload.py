#!/usr/bin/env python
# -*- coding: utf-8 -*-


def upload_productimgs_mozu(src_filepath):
    import requests
    import json
    import os.path as path
    #  "http://requestb.in/q66719q6" #
    auth_url = "https://home.staging.mozu.com/api/platform/applications/authtickets"
    tenant_url = "https://t11146.staging-sb.mozu.com/"

    headers = {'Content-type': 'application/json',
               'Accept-Encoding': 'gzip, deflate'}

    auth_request = {'applicationId' : 'bluefly.product_images.1.0.0.release',
                    'sharedSecret' : '53de2fb67cb04a95af323693caa48ddb'}

    auth_response = requests.post(auth_url,
                                  data=json.dumps(auth_request),
                                  headers=headers,
                                  verify=False
                                )

    filename = path.basename(src_filepath).split('.')[0]
    ext      = filename.split('.')[-1]
    mimetype = "image/{}".format(ext.lower().replace('jpg','jpeg'))


    print "Auth Response: %s" % auth_response.status_code
    auth_response.raise_for_status()
    auth = auth_response.json()
    print "Auth Ticket: %s" % auth["accessToken"]

    document_data_api = tenant_url + "/api/content/documentlists/files@mozu/documents"
    document_payload = {'listFQN' : 'files@mozu', 'documentTypeFQN' : 'image@mozu', 'name' : filename, 'extension' : ext}

    headers = {'Content-type': 'application/json',
               'x-vol-app-claims' : auth["accessToken"],
               'x-vol-tenant' : '11146',
               'x-vol-master-catalog' : '1'
               }

    document_response = requests.post(document_data_api,
                                      data=json.dumps(document_payload),
                                      headers=headers,
                                      verify=False
                                      )

    document_response.raise_for_status()

    document = document_response.json()
    document_id = document["id"]

    print "document Id: %s" % document_id
    print "document_payload: %s" % document_payload

    document_content_api = tenant_url + "/api/content/documentlists/files@mozu/documents/" + document_id + "/content"
    #files = {'media': open(src_filepath, 'rb')}
    file_data = open(src_filepath, 'rb').read()

    headers["Content-type"] = mimetype
    print "locals", locals()
    content_response = requests.put(document_content_api,
                                    data=file_data,
                                    headers=headers,
                                    verify=False
                                    )
    # TODO: store response fileID(blob) in db? [and/or] POST id to mozu as product attribute
    print "Document content upload Response: %s" % content_response.status_code
    document_response.raise_for_status()
    return content_response


if __name__ == '__main__':
    import sys
    src_filepath = sys.argv[1]
    upload_productimgs_mozu(src_filepath)

