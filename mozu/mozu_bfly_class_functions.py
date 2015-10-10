#!/usr/bin/env python
# coding: utf-8

## Use Classes - Could be in separate file
# from RESTClient import MozuRestClient
def count_total__files_documents(MozuRestClient,mz_imageid):
    mzclient = MozuRestClient(mz_imageid=mz_imageid)
    totalCount = mzclient.get_mz_image()['totalCount']
    print "Total Files in DocumentList: {}".format(totalCount)
    return totalCount


def list_files_documents(MozuRestClient,mz_imageid):
    mzclient = MozuRestClient(mz_imageid=mz_imageid)
    image_data = mzclient.get_mz_image()['items']
    #print image_data
    return image_data


def read_document_content_headers(MozuRestClient,mz_imageid):
    mzclient = MozuRestClient(mz_imageid=mz_imageid)
    image_data = mzclient().get_mz_image_headers()
    print image_data
    return image_data


def update_tags_mz_image(MozuRestClient,mz_imageid,**kwargs):
    tags = kwargs.get('tags','')
    mzclient = MozuRestClient(mz_imageid=mz_imageid,tags=tags)
    update_resp = update_tags_mz_image(MozuRestClient, mz_imageid)
    return update_resp


def upsert_content_mz_image(MozuRestClient,src_filepath=None,mz_imageid=None,**kwargs):
    tags = kwargs.get('tags','')
    mzclient = MozuRestClient(mz_imageid=mz_imageid,src_filepath=src_filepath,tags=tags)
    update_resp = update_tags_mz_image(MozuRestClient, mz_imageid)
    return update_res


def delete_document(MozuRestClient,mz_imageid):
    mzclient = MozuRestClient(mz_imageid=mz_imageid)
    delete_resp = mzclient.delete_mz_image()
    print locals()
    return delete_resp.headers


def upload_new(MozuRestClient,src_filepath,**kwargs):
    tags=kwargs.get('tags','')
    mzclient = MozuRestClient(src_filepath=src_filepath,tags=tags)
    doc_resp = mzclient.create_new_mz_image()
    return doc_resp


if __name__ == '__main__':
    import sys
    import os.path as path
    if path.isfile(sys.argv[1]):
        src_filepath = '/mnt/Post_Complete/Complete_Archive/xTestFiles/xTestMarketplace/999999/360128501.png'



