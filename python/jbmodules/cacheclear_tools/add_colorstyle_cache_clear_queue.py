#!/usr/bin/env python
# -*- coding: utf-8 -*-

def post_or_put_style_to_api(colorstyle, api_url=None, AuthToken=None):
    import requests, json
    import http.client, urllib.parse
    if not api_url:
        api_url = 'http://prodimages.ny.bluefly.com/image-update/'
    update_styles = list(set(sorted(update_styles)))
    for colorstyle in update_styles:
        data = {'colorstyle': colorstyle}
        #params = urllib.parse.urlencode(data)
        params = json.dumps(data)
        auth = {'Authorization': 'Token ' + AuthToken}
        content_type = {'content-type': 'application/json'}
        headers = json.dumps(auth,content_type)
        # conn = http.client.HTTPConnection(api_url, 80)
        # conn.request("PUT", "/", BODY)
        #response = conn.getresponse()
        try:
            response = requests.post(api_url, headers=headers, params=params)
            print response.status, response.method, data
            #print(resp.status, response.reason)
        except:
            try:
                response = requests.put(api_url, headers=headers, params=params)
                print response.status, response.method, data
            except:
                curlauth = 'Authorization: Token ' + AuthToken
                curldata = 'colorstyle=' + colorstyle
                # try:
                #     subprocess.call([ 'curl', '-u', 'james:hoetker', '-d', curldata, '-H', curlauth, '-X', 'PUT', api_url])
                # except:
                #     subprocess.call([ 'curl', '-u', 'james:hoetker' '-d', curldata, '-H', curlauth, api_url])


if __name__ == '__main__':
    import os,sys
    try:
        colorstyle = sys.argv[1]
        post_or_put_style_to_api(colorstyle, api_url=None, AuthToken=None)
    except IndexError:
        print 'Enter a style numbert to add to clear queue'
