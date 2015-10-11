import csv
import os
import sys,re


homedir = os.path.expanduser("~")
csvfile = os.path.join(homedir, "2013-03-25_write.csv")

print csvfile

#pathtocsv = os.path.join(os.path.expanduser('~'), csvfile)


#with open(csvfile, 'rb') as f:
#    readfile = csv.reader(f, delimiter=",")
#    for row in readfile: 
#        print row

pattern_url = r'/^(((http|https|ftp):\/\/)?([[a-zA-Z0-9]\-\.])+(\.)([[a-zA-Z0-9]]){2,4}([[a-zA-Z0-9]\/+=%&_\.~?\-]*))*$/'





pattern_exiftag = r'([A-Z]\w+?:[A-Za-z]\w+?)'

#pattern_exifval = r'([A-Za-z0-9]*?\s*?\W+?)'

pattern_exifval = r'([A-Z0-9]\w+?\s?[A-Za-z]+\')'
regex_exif = re.compile(pattern_exiftag + "=" + pattern_exifval)
pattern = re.compile(r'(\d+?[/|-]+?\d+?[/|-]+?\d+?)')

f = open(csvfile, 'rb')

string = re.findall(pattern, f.read())
sorted(string)
print list(string)
#for f in listdir(dir_homedir):
#     fpath = os.path.abspath(f)
#     re.findall(pattern, fpath)




querystr = 'http://www.bluefly.com/_/N-1aaq/Ntt-{style}/Nrk-all/Nrr-all/Nrt-{style}/Ntk-all/Ntx-mode+matchallpartial/search.fly?init=y'.format(style=colorstyle)


startDateFrom=&startDateTo=&colorGroup=&searchBrand=&eventId=&productStatus=&merchantStatus=&inventory=&active=&store=&styleNumbers=324162301&vendorStyleNumbers=&shortName=&poHdrs=&searchCategory=&jdaCategory=&Submit=Search&exportToExcel=false&exportImages=false&solrQuery=&currentPage=0


import asyncore, socket

class HTTPClient(asyncore.dispatcher):

    def __init__(self, host, path):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect( (host, 80) )
        self.buffer = 'GET %s HTTP/1.0\r\n\r\n' % path

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def handle_read(self):
        print self.recv(8192)

    def writable(self):
        return (len(self.buffer) > 0)

    def handle_write(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]


#client = HTTPClient('www.python.org', '/')
#asyncore.loop()


import asyncore
import socket

class EchoHandler(asyncore.dispatcher_with_send):

    def handle_read(self):
        data = self.recv(8192)
        if data:
            self.send(data)

class EchoServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print 'Incoming connection from %s' % repr(addr)
            handler = EchoHandler(sock)

#server = EchoServer('localhost', 8080)
#asyncore.loop()


class http_request_handler(asynchat.async_chat):

    def __init__(self, sock, addr, sessions, log):
        asynchat.async_chat.__init__(self, sock=sock)
        self.addr = addr
        self.sessions = sessions
        self.ibuffer = []
        self.obuffer = ""
        self.set_terminator("\r\n\r\n")
        self.reading_headers = True
        self.handling = False
        self.cgi_data = None
        self.log = log

    def collect_incoming_data(self, data):
        """Buffer the data"""
        self.ibuffer.append(data)

    def found_terminator(self):
        if self.reading_headers:
            self.reading_headers = False
            self.parse_headers("".join(self.ibuffer))
            self.ibuffer = []
            if self.op.upper() == "POST":
                clen = self.headers.getheader("content-length")
                self.set_terminator(int(clen))
            else:
                self.handling = True
                self.set_terminator(None)
                self.handle_request()
        elif not self.handling:
            self.set_terminator(None) # browsers sometimes over-send
            self.cgi_data = parse(self.headers, "".join(self.ibuffer))
            self.handling = True
            self.ibuffer = []
            self.handle_request()
            



def sqlQueryReturnStylesbyPO(str(ponum)):
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
    connection = orcl_engine.connect()
    querymake_ponum_to_colorstyle="SELECT POMGR_SNP.PRODUCT_COLOR.ID AS colorstyle, POMGR_SNP.PO_LINE.PO_HDR_ID AS po_hdr FROM POMGR_SNP.PRODUCT_COLOR INNER JOIN POMGR_SNP.PO_LINE ON POMGR_SNP.PRODUCT_COLOR.ID = POMGR_SNP.PO_LINE.PRODUCT_COLOR_ID WHERE POMGR_SNP.PO_LINE.PO_HDR_ID = '" + ponum + "'"
    result = connection.execute(querymake_ponum_to_colorstyle)
    colorstyle_po_ret = {}
    for row in result:
        ret = {}
        ret['colorstyle'] = row['colorstyle']
        colorstyle_po_ret[row['po_hdr']] = ret
    connection.close()
    return ccolorstyle_po_ret

def url2_download_read_http(targeturl):
    from time import time
    import urllib2, subprocess
    url_start = time()
    targetreq = urllib2.Request(targeturl)
    downloadfile = urllib2.urlopen(targetreq).read()
    url_end = time()
    print "Download Time -> %s"  % (url_end - url_start)
    return downloadfile

class DropboxDownloadPageURLs():
    
    import urllib,os,time,subprocess,requests
    from bs4 import BeautifulSoup
    
    def __init__(self,dropboxsharedurl):
    
    
#### Get URL parse for image links return Unique Image Link List
def html_parse_dropbox_frlink(dropboxsharedurl):
    import os,re,sys,requests
    from bs4 import BeautifulSoup

    url = sys.argv[1]

    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    souplist = []
    for link in soup.find_all('a'):
        print(link.get('href'))
        souplist.append(link)

    jpglist = []
    for link in souplist:
        found = link.get('href')
        jpglist.append(found)
    imglinks = unique(jpglist)
    return imglinks

        
