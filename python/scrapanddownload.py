#!/usr/bin/env python
import os,re,sys,urllib


link_testreq = 'https://www.yousendit.com/dl?phi_action=app/orchestrateDownload&rurl=https%253A%252F%252Fwww.yousendit.com%252Ftransfer.php%253Faction%253Dbatch_download%2526send_id%253D2064268784%2526email%253D0813d1d13bbc4778ff7be299531aa0b4&s=19105&cid=tx-02002208350200000000'
#link_testreq = sys.argv[1]
#link_testreq='http://theberry.com/2011/02/07/daily-awww-theres-just-something-about-kittens-36-photos'
domain = 'https://www.yousendit.com'
#domain = sys.argv[2]
########## REGEX PATTERN DEFINITIONS COMPILed
pattern_url = r'/^(((http|https|ftp):\/\/)?([[a-zA-Z0-9]\-\.])+(\.)([[a-zA-Z0-9]]){2,4}([[a-zA-Z0-9]\/+=%&_\.~?\-]*))*$/'
regex_url = re.compile(r'/^(((http|https|ftp):\/\/)?([[a-zA-Z0-9]\-\.])+(\.)([[a-zA-Z0-9]]){2,4}([[a-zA-Z0-9]\/+=%&_\.~?\-]*))*$/')


def has_href_but_no_src(tag):
    return tag.has_key('href') and not tag.has_key('src')

##############################
###########
#### 1 ####
###########   Download URL doc/file -- Uses urllib2
###########   URL LIB 2  ###
###  DOES NOT SAVE FILE  -- Read HTML From URL Return unparsed HTML
###
def url2_download_read_http(targeturl):
    from time import time
    import urllib2, subprocess
    url_start = time()
    targetreq = urllib2.Request(targeturl)
    targetreq.add_unredirected_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:20.0) Gecko/20100101 Firefox/20.0')
    targetreq.add_unredirected_header('Content-Type', 'text/html;charset=utf-8')
    downloadfile = urllib2.urlopen(targetreq).read()
    url_end = time()
    print "Download Time -> %s"  % (url_end - url_start)
    return downloadfile

##################
###########
#### 2 ####
###########   
########### Parse HTML File with Beautifulsoup Module Return Links
###

def html_parse_links(htmlpage, domain):
    #domain = 'https://www.yousendit.com'
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(htmlpage)
    links = []
    for link in soup.find_all('a'):
        try:
            hrefstr = link.get('href')
            filenm = link.get('title')
            #filenm = soup.select('a[href*="."]')
            lastp = str(hrefstr)
            if hrefstr:
                #dload = str(domain + "/" + lastp + "/" + filenm)
                dload = str(domain + "/" + lastp + "/" + filenm)
                links.append(dload)
            if filenm:
                print filenm
        except TypeError:
            print "Unicode Obj Error"
        except UnicodeEncodeError:
            print "Unicode ASCII Codec Error"
    return links


##################
###########
#### 3 ####
###########   Download URL as file Uses urllib ###
###########   URL LIB 1  ###
###  Will SAVE FILE  to var - downloaddir-- 
###
def url_download_file_http(url):
    from time import time
    import urllib, subprocess
    try:
        downloaddir = os.path.join(os.path.expanduser('~'), 'script_dowloads')
        try:
            os.mkdir(downloaddir)
        except OSError:
            print "Directory Exists"
        filename = url.split('/')[-1]
        filepath =  os.path.join(downloaddir, filename)
        url_start = time()
        try:
            os.chdir(downloaddir)
            downloadfile = urllib.urlretrieve(url, filename)
            url_end = time()
            print "File %s Download Time -> %s" % (downloadfile, url_end - url_start)
        except IOError:
            print "IO Error No File or Dir to save {0}".format(filepath)
        except OSError:
            print "OS Error"
    except AttributeError:
        print "Attribute Error - Type doesnt have a property requested"
        return downloadfile
    


    
for link in (html_parse_links(url2_download_read_http(link_testreq), domain)):
    url_download_file_http(link)
