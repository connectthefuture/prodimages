
def url_get_links(targeturl):
    import os,re,sys,requests
    from bs4 import BeautifulSoup
    r = requests.get(targeturl)
    soup = BeautifulSoup(r.text)
    ###  soup is now Full HTML of target -- Below creates/returns list of unique links
    linklist = []
    for link in soup.find_all('a'):
        linklist.append(link.get('href'))
        sorted(linklist)
    ## Return list of unique links
    return list(set(linklist))


def url_download_fileslist_dbx(imglinkslist):
    import urllib,os,time,subprocess
    downloaddir = os.path.join(os.path.expanduser('~'), 'script_dowloads')
    for link in imglinkslist:
        try:
            filename = str(link.split('/')[-1])
            filepath =  os.path.join(downloaddir, filename)
            os.chdir(downloaddir)
            #url_start = time()
            downloadfile = urllib.urlretrieve(link, filepath)
            #url_end = time()
            #print "File %s Download Time -> %s" % (downloadfile, url_end - url_start)
        except AttributeError:
            print "Attribute Error -- None Type"
        except IOError:
            print "IO Error No File or Dir to save {0}".format(filepath)
        except OSError:
            print "OS Error {0}".format(filepath)
            return downloadfile


def soup_get_links_jpgs(soup):
    from bs4 import BeautifulSoup
    linklist = []
    for link in soup.select('a[href$="jpg"]'):
        linklist.append(link.get('href'))
        sorted(linklist)
    ## Return list of unique links to jpg Files
    return list(set(linklist))

    
def soup_from_url(targeturl):
    from bs4 import BeautifulSoup
    import requests
    r = requests.get(targeturl)
    soup = BeautifulSoup(r.text)
    return soup    

def soup_get_links_dboxthumbs(soup):
    from bs4 import BeautifulSoup
    linklist = []
    for link in soup.select('a[href*="jpg"]'):
        linklist.append(link.get('href'))
        sorted(linklist)
    ## Return list of unique links to jpg Files
    return list(set(linklist))


#print imglinkslist
#target_url_list = []
#for link in url_get_links(imglinkslist):
#    import os,re,sys,requests
#    from bs4 import BeautifulSoup
#    r = requests.get(link)
#    soup = BeautifulSoup(r.text)
#    for link in soup.select('a[href$="jpg"]'):
#        target_url_list.append(link.get('href'))
#        sorted(linklist)
#ll = list(['https://www.dropbox.com/sh/f4mic906etxjktd/ZoIiM2TkUF/0605024.jpg', 'https://www.dropbox.com/sh/f4mic906etxjktd/9Yq-1EGMkr/0606260.jpg'])
#for singleurl in ll:
#    from bs4 import BeautifulSoup
#    import requests
#    try:    
#        singlesoup = soup_from_url(singleurl)
#        htmlstr = str(singlesoup.select('img[src]'))
#        freshsoup = BeautifulSoup(htmlstr)
#        print freshsoup.get('a[href^="https://dl.dropbox"]')
#        print freshsoup.prettify()
#    except requests.exceptions.MissingSchema:
#        print "Invalid URL {0}".format(singleurl)

#print target_url_list

def final_img_get(targeturl):
    newsoup = soup_from_url(str(targeturl))
    finalimgs = soup_get_links_dboxthumbs(newsoup)
    finalimg = finalimgs.pop()
    return finalimg
    
########################################### RUN ######################

#testurl = 'https://www.dropbox.com/sh/f4mic906etxjktd/7nUIcN-0JA'
testurl = 'https://www.dropbox.com/sh/fkr4510o0mpdeyf/AADD9qKHIO2XNOup_ry3dQg9a?dl=0'
imglinkslist = url_get_links(testurl)

dload_list = []    

for finalurl in imglinkslist:
    import requests
    try:
        hirez_imageurl = final_img_get(finalurl)
        dload_list.append(hirez_imageurl)
    except requests.exceptions.MissingSchema:
        print "Bad Schema--Next"
    except IndexError: 
        print "End of List"
print dload_list
#print newsoup.select
#def soup_get_links_dboxfullsize(target_url_list):
#    from bs4 import BeautifulSoup
#    linklist = []
#    for link in soup.select('a[href$="http://www.dropbox.com"]'):
#        linklist.append(link.get('href'))
#        sorted(linklist)

#url_download_fileslist_dbx(imglinkslist)