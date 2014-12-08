#!/usr/bin/env python
# -*- coding: utf-8 -*-

def normalize_json_tounicode(filename):
    from kitchen.text.converters import getwriter, to_unicode
    import json
    from collections import defaultdict
    from os import path
    data = []
    if type(filename) == str:
        if path.isfile(filename):
            jsondata = json.load(open(filename))
            print 'FILE'
            for row in jsondata:
                datarow = {}
                for k,v in row.items():
                    if type(v) == unicode:
                        v = to_unicode(v)
                    if type(k) == unicode:
                        k = to_unicode(k)
                    if type(v) == int:
                        v = str(v)
                        v = to_unicode(v)
                    if type(k) == int:
                        k = str(k)
                        k = to_unicode(k)
                    #print type(v), type(k)
                    datarow[k] = v 
                #data[to_unicode(row[k])] = datarow
                data.append(datarow)
        else:
            jsondata = json.dumps(filename)
            print 'STR'
    elif type(filename) == dict:
        jsondata = filename
        datarow =  {} ##defaultdict(list) 
        for k,v in jsondata.iteritems():
            if type(v) == unicode:
                v = to_unicode(v)
            if type(k) == unicode:
                k = to_unicode(k)
            if type(v) == int:
                v = str(v)
                v = to_unicode(v)
            if type(k) == int:
                k = str(k)
                k = to_unicode(k)
            #print type(v), type(k)
            #datarow[k].append(v) 
            datarow[k] = v 
        #data[to_unicode(row[k])] = datarow
        data.append(datarow)
        print 'ELSE', type(filename)
    
    return data


def normalize_json_tobytes(filename):
    from kitchen.text.converters import getwriter, to_bytes
    import json
    from collections import defaultdict
    from os import path
    data = []
    if type(filename) == str:
        if path.isfile(filename):
            jsondata = json.load(open(filename))
            print 'FILE'
            for row in jsondata:
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
                #data[to_bytes(row[k])] = datarow
                data.append(datarow)
        else:
            jsondata = json.dumps(filename)
            print 'STR'
    elif type(filename) == dict:
        jsondata = filename
        datarow =  {} ##defaultdict(list) ##{}
        for k,v in jsondata.iteritems():
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
            #datarow[k].append(v) 
            datarow[k] = v 
        #data[to_bytes(row[k])] = datarow
        data.append(datarow)
        print 'ELSE', type(filename)
    
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
            if res.status_code < 400:
                print 'POST request succeeded to -->', url 
            else:
                print 'POST request Failed to -->', url , ' with Code ', res.status_code                
            return res
        except:
            print 'POST failed, Trying to PUT to -->', url 
            try:
                res = requests.put(url, headers=headers, data=data)
                if res.status_code < 400:
                    print 'Try 2 PUT request succeeded to -->', url
                else:
                    print 'PUT request Failed to -->', url , ' with Code ', res.status_code     
                return res
            except:
                print '2nd Transmit Attempt using PUT failed to -->', url 
                return False
    elif method and data:
        res = requests.request(method, url, headers=headers, data=data)
        if res.status_code < 400:
            print 'Sent Custom ', method, ' Request to --> ', url
        else:
            print 'Failed Custom ', method, ' Request to --> ', url
        return res
    elif not data:
        print 'No data payload included in request issuing GET for --> ' , url
        res = requests.get(url, headers=headers, params=params)
        if res.status_code < 400:
            return res


def iterate_post_data_kv(data):
    from collections import defaultdict
    import json
    if type(data) == dict:
        for key,val in data.iteritems():
            for k,v in val.iteritems():
                try:
                    #jsondata = json.dumps({key: {k: v} })
                    jsondata = json.dumps({k: v})
                    response = post_to_api(data=json.loads(jsondata), api_endpoint='looklet-shot-list/')
                    if response.status_code == 200:
                        pass
                    else:
                        print response.status_code, ' ERROR', response.text, '\n\t', jsondata
                    #print jsondata
                except KeyError:
                    print 'KeyError', k, v, key,
    elif type(data) == list:        
        for val in data:
            dd = defaultdict(list)
            [ dd[k].append(v) for k,v in val.iteritems() if val[k] ] 
            try:
                #jsondata = json.dumps({key: {k: v} })
                jsondata = json.dumps(dd)
                response = post_to_api(data=json.loads(jsondata), api_endpoint='looklet-shot-list/')
                if response.status_code == 200:
                    pass
                else:
                    print response.status_code, ' ERROR', response.text, '\n\t', jsondata
                #print jsondata
            except KeyError:
                print 'KeyError', k, v,
    return


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
    data=normalize_json_tobytes(filename)
    #print json.dumps(data.items())
    result = iterate_post_data_kv(data)
    print result


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