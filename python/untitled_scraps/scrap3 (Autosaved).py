import os,re,sys,requests
from bs4 import BeautifulSoup

#url = sys.argv[1]
url = 'https://www.dropbox.com/sh/f4mic906etxjktd/7nUIcN-0JA'

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


len(jpglist)







#########    Extracts all images from a 
#######
# get_links.py
# https://pythonadventures.wordpress.com/2011/03/10/extract-all-links-from-a-web-page/
import re
import sys
import urllib
import urlparse
from bs4 import BeautifulSoup
import clipboard

class MyOpener(urllib.FancyURLopener): 
    version = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15'
    def process(url): 
        myopener = MyOpener() #page = urllib.urlopen(url) page = myopener.open(url)
        text = page.read() page.close()
        soup = BeautifulSoup(text) 
        for tag in soup.findAll('a', href=True):
            tag['href'] = urlparse.urljoin(url, tag['href'])
            print tag['href'] 
    # process(url)
    def main(): clipText = clipboard.get() 
        print clipText process(clipText)
    # main()
    if __name__ == "__main__":
        main()


##### Get HTML from URL and make Soup
#1B
def soup_from_url(targeturl):
    from bs4 import BeautifulSoup
    import requests
    r = requests.get(targeturl)
    soup = BeautifulSoup(r.text)
    return soup

##### Return Links from Soup
#1C
def soup_get_links(soup):
    from bs4 import BeautifulSoup
    ###  soup is now Full HTML of target -- Below creates/returns list of unique links
    linklist = []
    for link in soup.find_all('a'):
        linklist.append(link.get('href'))
        sorted(linklist)
    ## Return list of unique links
    return list(set(linklist))

### Combined consolidated func run like --> linklist = soup_get_links((soup_from_url(targeturl)))
####################################################################
##### 
#1D
###  COMBINED: Get All href Links from Beautiful Soup and Requests -- downloads URL as html and returns Unique Links to files in text formatted by BSoup
def url_get_links(targeturl):
    import os,re,sys,requests
    from bs4 import BeautifulSoup
    r = requests.get(targeturl)
    soup = BeautifulSoup(r.text)
    ###  soup is now Full HTML of target -- Below creates/returns list of unique links
    linklist = []
    for link in soup.select('a[href$="jpg"]'):
        linklist.append(link)
        sorted(linklist)
    ## Return list of unique links
    return list(set(linklist))

def url_download_file_http(url):
    from time import time
    import urllib, subprocess
    try:
        downloaddir = os.path.join(os.path.expanduser('~'), 'script_dowloads')
        if not downloaddir:
            os.mkdir(downloaddir)
        filename = url.split('/')[-1]
        filepath =  os.path.join(downloaddir, filename)
        filepath =  os.path.join(filepath, '.file')
        url_start = time()
        downloadfile = urllib.urlretrieve(url, filepath)
        url_end = time()
        print "Download Time -> %s"  % (url_end - url_start)
    except OSError:
        print "OS Error"
    except AttributeError:
        print "Attribute Error - Type doesnt have a property requested"
    return downloadfile



"""
Beautiful Soup examples Select specific tags using Anchors-- ^ $ *


"""
soup.select('a[href="http://example.com/elsie"]')
## [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]
#
soup.select('a[href^="http://example.com/"]')
## [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
##  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
##  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
#
soup.select('a[href$="tillie"]')
## [<a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
#
soup.select('a[href*=".com/el"]')
## [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]





###################################---------------##########################


"""
DefaultDicts & OrderedDicts
"""
#### Default Dict Examples
## 1 ## Mimicking DefaultDict using regular dict __builtin__

inputlist = sys.arv[0]

d = {}
for k, v in inputlist:
    d.setdefault(k, []).append(v)

## 2 # Create DefaultDict us List where key has only One Value (the last value)

inputlist = sys.arv[0]

d = defaultdict(list)
for k, v in inputlist:
    d[k].append(v)

## 3 # Create DefaultDict using Set where values with same key are combined/Grouped so key can have multiple values
inputlistofsets = sys.arv[0]

d = defaultdict(set)
for k, v in inputsetlist:
    d[k].add(v)

### Return dict items
d.items()


#### Ordered Dict Examples with classes

# ### # regular unsorted dictionary
d = {'banana': 3, 'apple':4, 'pear': 1, 'orange': 2}

# ### # dictionary sorted by key
OrderedDict(sorted(d.items(), key=lambda t: t[0]))
# >>> # OrderedDict([('apple', 4), ('banana', 3), ('orange', 2), ('pear', 1)])

# ### # dictionary sorted by value
OrderedDict(sorted(d.items(), key=lambda t: t[1]))
# >>> # OrderedDict([('pear', 1), ('orange', 2), ('banana', 3), ('apple', 4)])

# ### # dictionary sorted by length of the key string
OrderedDict(sorted(d.items(), key=lambda t: len(t[0])))
# >>> # OrderedDict([('pear', 1), ('apple', 4), ('orange', 2), ('banana', 3)])

### If new entry overwrites old entry, new entry appended to end, unsorted
class LastUpdatedOrderedDict(OrderedDict):
    'Store items in the order the keys were last added'

    def __setitem__(self, key, value):
        if key in self:
            del self[key]
        OrderedDict.__setitem__(self, key, value)

## Lets Counter keep track of Inserts to Dict
class OrderedCounter(Counter, OrderedDict):
     'Counter that remembers the order elements are first encountered'

     def __repr__(self):
         return '%s(%r)' % (self.__class__.__name__, OrderedDict(self))

     def __reduce__(self):
         return self.__class__, (OrderedDict(self),)