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


def post_to_api(data=None, host='prodimages.ny.bluefly.com/', api_path='api/v1/', api_endpoint='looklet-shot-list/', method=None):
    import json, requests
    url = 'http://' + host + api_path + api_endpoint
    headers = {'Content-Type': 'application/json'}
    res = requests.post(url, headers=headers, data=data)
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
                response = post_to_api(data=jsondata, api_endpoint='looklet-shot-list/', method='POST')
                if response.status_code == 200:
                    pass
                else:
                    print response.status_code, ' ERROR', response.text
                #print jsondata
            except KeyError:
                print 'KeyError', k, v, key,


if __name__ == '__main__':
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