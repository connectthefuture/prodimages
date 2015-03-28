#!/usr/bin/env python
import os, sys, re, csv

def readxl_outputdict(workbk=None):         
    import csv,xlrd,sys
#    workbk = sys.argv[1]
    book = xlrd.open_workbook(workbk)##sys.argv[1])
    sh = book.sheet_by_index(0)

    #convWriter = csv.writer(sys.stdout,delimiter=',', dialect='excel')
    numcols=sh.ncols
    outdict = {}
    for rx in xrange(sh.nrows):
        rowdict = {}    
        for cx in xrange(sh.ncols):
            rowhead = sh.cell_value(rowx=0,colx=cx)
            rowval = sh.cell_value(rowx=rx,colx=cx)
            if rowval is not '':
                print rowval
                rowdict[rowhead] = rowval
                outdict[rx] = rowdict
    return outdict


def compile_outdict_by_rowkeys(outdict):
    from collections import defaultdict
    d = defaultdict(list)
    for r in outdict.items():
        dd = defaultdict(dict)
        for val in r[1].items():
            try:
                print r[0],val[0],val[1]
                dd[val[0]]=val[1]
                d[r[0]] = dd
                #csv_write_datedOutfile(lines.encode('ascii', 'replace'))
            except AttributeError:
                pass
    return d


def send_post_bulkdataload_tool(xlspath):  #, POSTURL=None):
    import pycurl,json,re,xlrd
    data = readxl_outputdict(workbk=None)
    data = compile_outdict_by_rowkeys(data)
    ## Create send data
    #data = json.dumps({
    #'style' : colorstyle,
    #'version' : version
    #})
    POSTURL_Referer = 	'http://tools.l3.bluefly.com/product/bulk-data-change' 
    POSTURL = '/ajax/doUploadForBulkDataChange'
    
#        regex = re.compile(r'.+?Mobile.+?')
#        if re.findall(regex, POSTURL):
#            data = "style={0}".format(colorstyle)
#            # Replace Previous Line with uncommenting next line when versioning is added to mobile
#            # Currently only need to POST Colorstyle to PHP script       
#            ## data = "style={0}&version={1}".format(colorstyle, version)
#        else:
#            data = "style={0}&version={1}".format(colorstyle, version)
    
    ## SET REQUEST HEADERS    
    head_accept             = 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    head_acceptencoding     = 'Accept-Encoding: gzip,deflate'
    head_contentdisposition = 'Content-Disposition: form-data; name="fileToUpload"; filename="bulkloadtotoolshvault.xlsx"'
    head_contenttype        = 'Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    head_content_len        = "Content-length: {0}".format(str(len(data)))
    head_cookie             = 'Cookie: SSID=BgAQbB0AAAAAAADzlwdTMQgCBPOXB1MyAAAAAAAAAAAAN4ZzUwBeJw; SSRT=N4ZzUwA; SSPV=AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA; __utma=9200358.393565536.1393006580.1400006069.1400079932.43; __utmz=9200358.1393006580.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); bn_u=6925017064556400858; _br_uid_2=uid%3D7816138366854%3Av%3D10.5%3Ats%3D1393006580468%3Ahc%3D217; bn_cd=d%26g%26s; mbcc=23D92A53-9C16-51FA-AD48-D0680E7C36EB; mbdc=23E447C1.A789.5218.B243.2411D90E3D50; bnTrail=%5B%22http%3A%2F%2Fwww.bluefly.com%2Fnew_arrivals%3Fso%3Dnew%26vl%3Dl%26ppp%3D96%26cp%3D1%26sosc%3Dtrue%22%2C%22http%3A%2F%2Fwww.bluefly.com%2F%22%2C%22http%3A%2F%2Fwww.bluefly.com%2Fjewelry-watches%2Ffashion-jewelry%2Fdesigner-diamonds%3Fso%3Drel%26oq%3Ddiamonds%22%2C%22http%3A%2F%2Fwww.bluefly.com%2Fsearch%2F%3Fq%3DSwimwear%22%2C%22http%3A%2F%2Fwww.bluefly.com%22%5D; a1000c1s1=user&john.bragato@bluefly.com&location&0&id&&public&0&web&0&cs&w2-1401599121-62f2bf9dec211691eabcf4215c1e1843a3bd021b; __cht=RIuvdsvP0OQ6ixUWI07NESHCC2; __chab=1; __chabt=1396400152802; SSLB=0; SSSC=1.G5982917699985082417.50|0.0; TLTHID=318A2436DB7910DB04BBD4D36AA2045B; TLTSID=ED57B3E6DAC410DA0614CBCB7DB58A13; __utmc=9200358; ci_session=BGRWOgY3VmoDKgQlCGEBMQ87UTlXIFZxA2ABKgFwAT4APwFmUgkDaQNmWS1QbARxA2tXNgJjU2hXcQw9XWxUZgM2DGYHNFNjUWcAMQcxBzMENlZjBmBWaANiBDcIbgE2DzJRYVdmVmQDZwFhAWEBbwBjAT1SMwM1AzZZLVBsBHEDa1c0AmFTaFdxDDddeFRfA2QMMAdhU3dRZAB6B3AHJgQ%2BVnMGO1ZhA2UEbAh5ATEPMlExVyxWMwMzAWEBLQFlAGEBJlJnAzEDM1ktUGwEcQNrVzQCYVNoV3EMK117VGUDdwwLB2RTYlFkAGcHdwcmBD5WcwY7VmUDYQRsCHkBTQ9kUXlXa1ZuA2kBOAEsAWIAfgE4UnYDKANPWW5QNARrAz9XcQI%2BUyFXOwxlXShUSQNrDCAHYFNpUSEARAdiB2cEJVZPBlJWcAMJBHYIagEwDyVRNVc5ViIDdwEvATkBZQBmASpSbQNzAzhZPlBkBDgDc1dpAjBTIVcnDAFdaVRjA3EMPQdzU2xRdQBwByEHPwR2VjoGMFZgA2sEdAhqATQPO1EzVzNWNQM9AWgBMAFhAHIBM1IlAzoDNFk1UHUEVwMiV2ACI1MbVxcMfF0zVHMDPwxnBz9TJ1EyAD8HMgcmBD5WcwY7VmkDawR0CBcBbw9sUWpXbFZWA2wBNAFmAXUAawF7UmwDMQMyWTVQdQQzA2VXNQJhU2NXZAxmXTlUOAMxDHYHPlN4'
    head_host               = 'Host: tools.l3.bluefly.com'
    head_referer            = 'Referer: {0}'.format(POSTURL_Referer)
    head_useragent          = 'User-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:20.0) Gecko/20100101 Firefox/20.0'
    
    c = pycurl.Curl()
    c.setopt(c.URL, POSTURL)
    c.setopt(pycurl.HEADER, 0)
    #c.setopt(pycurl.INFOTYPE_HEADER_OUT, 1)
    #c.setopt(pycurl.RETURNTRANSFER, 1)
    c.setopt(pycurl.FORBID_REUSE, 1)
    c.setopt(pycurl.FRESH_CONNECT, 1)
    c.setopt(pycurl.POSTFIELDS, data)
    c.setopt(pycurl.HTTPHEADER, [head_accept, 
                                 head_acceptencoding,
                                 head_contentdisposition, 
                                 head_contenttype, 
                                 head_content_len,
                                 head_cookie,
                                 head_host,
                                 head_referer,
                                 head_useragent])
    #c.setopt(c.POSTFIELDS, POSTDATA)
    c.setopt(c.VERBOSE, True)
    c.perform()
    c.close()
    #print "Successfully Sent Bulkloader --> Style: {0} Ver: {1}".format(colorstyle, version)
    #head_authtoken = "Authorization: tok:{0}".format(token)
    #head_content_len= "Content-length: {0}".format(str(len(POSTDATA)))
    #head_accept = 'Accept: application/json'
    #head_contenttype = 'Content-Type: application/json'
        


############################################
def main():
    import sys,os
    xlspath = sys.argv[1]
    workbk = xlspath

    send_post_bulkdataload_tool(xlspath)    # POSTURL=None)
    #outdict = readxl_outputdict(workbk)
    #compiled_rows = compile_outdict_by_rowkeys(outdict)

    #for k,v in compiled_rows.iteritems():
    #    for val in v:
    #        print k,val,v[val]
############################################

if __name__ == '__main__': 
    main()
