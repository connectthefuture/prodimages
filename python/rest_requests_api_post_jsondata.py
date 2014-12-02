#!/usr/bin/env python
# -*- coding: utf-8 -*-

def normalize_unicode_json_tobytes(filename):
    from kitchen.text.converters import getwriter, to_bytes, to_unicode
    import json
    json_data = json.load(open(filename))
    data = {}
    for row in json_data:
        datarow = {}
        for k,v in row.items():
            if type(v) == unicode:
                v = to_bytes(v)
            if type(k) == unicode:
                k = to_bytes(k)
            if type(v) == int:
                v = str(v)
                v = to_bytes(v)
            if type(k) == int:
                k = str(k)
                k = to_bytes(k)
            #print type(v), type(k)
            datarow[k] = v 
        data[to_bytes(row[k])] = datarow
    return data


def post_to_api(data=None, params=None, method=None, api_endpoint=None, host='prodimages.ny.bluefly.com/', api_path='api/v1/'):
    import json, requests
    url = 'http://' + host + api_path + api_endpoint
    headers = {'Content-Type': 'application/json; charset=utf-8', 
                    'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; en-US; rv:33.0) Gecko/20100101 Firefox/33.0'
                    }
                    ## 'User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'
    if data and not method and not params:
        try:
            res = requests.post(url, headers=headers, data=data)
            print 'POST request succeeded to -->', url 
            return res
        except:
            print 'POST failed, Trying to PUT to -->', url 
            try:
                res = requests.put(url, headers=headers, data=data)
                print 'Try 2 PUT request succeeded to -->', url
                return res
            except:
                print '2nd Transmit Attempt using PUT failed to -->', url 
                return False
    elif method and data:
        res = requests.request(method, url, headers=headers, data=data)
        print 'Sent Custom ', method, ' Request to --> ', url
        return res
    elif not data:
        print 'No data payload included in request issuing GET for --> ' , url
        res = requests.get(url, headers=headers, params=params)
        return res

########     RUN      ##########
def main(filename=None):
    import __builtin__, json, yaml, re, datetime, sys
    from os import path
    today = datetime.date.strftime(datetime.date.today(), '%Y-%m-%d')
    if not filename:
        try:
            filename = sys.argv[1]
            if path.isfile(filename):
                pass
            else:
                filename='/var/www/srv/media/feeds/{0}_LookletShotListImportJSON.json'.format(today)
        except:
            filename='/var/www/srv/media/feeds/{0}_LookletShotListImportJSON.json'.format(today)
    #print filename
    filename='/Users/johnb/Nitrous/relic7.owncloud.arvixe.com/bflySync/{0}_LookletShotListImportJSON.json'.format(today)
    data=normalize_unicode_json_tobytes(filename)
    #print json.dumps(data.items())
    for key,val in data.iteritems():
        for k,v in val.iteritems():
            try:
                #jsondata = json.dumps({key: {k: v} })
                jsondata = json.dumps({k: v})
                response = post_to_api(data=json.loads(jsondata), api_endpoint='looklet-shot-list/')
                if response.status_code == 200:
                    pass
                else:
                    print response.status_code, ' ERROR', response.text
                #print jsondata
            except KeyError:
                print 'KeyError', k, v, key,


if __name__ == '__main__':
    import __builtin__, json, yaml, re, datetime, sys
    from os import path
    today = datetime.date.strftime(datetime.date.today(), '%Y-%m-%d')
    #filename='/Users/johnb/Nitrous/relic7.owncloud.arvixe.com/bflySync/{0}_LookletShotListImportJSON.json'.format(today)
    main()
    
    
#import __builtin__, json,yaml,re
#def json_file_parse(filename):
#    data = []
#    with __builtin__.open(filename, 'r') as jsonfile:
#        for line in jsonfile:
#            try:
#                line = line.lstrip()
#                data.append(json.loads(line))
#            except IOError:
#                print line
#                pass
#    return data

#s = re.sub('([{,])([^{:\s"]*):', lambda m: '%s"%s":'%(m.group(1),m.group(2)),s)