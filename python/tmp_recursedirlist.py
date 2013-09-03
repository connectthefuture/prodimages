#!/usr/bin/env python

def recurse_dir_list(directory):
    import os,sys,re
    filepaths = {}
    for dirpath,subdir,files in os.walk(directory):
        for f in files:
            filepaths[dirpath] = files[:]

    recursivefilelist = []
    for path,files in filepaths.items():
        for f in files:
        	filepath = "{0}/{1}".format(path,f)
        	recursivefilelist.append(filepath)
        	sorted(recursivefilelist)

    regex = re.compile(r'^.+?[.].+?$')
    alljpgs = []
    for f in recursivefilelist:    
        foundjpgs = re.findall(regex,f)
        if foundjpgs:
            alljpgs.append(f)
    return alljpgs

# def get_exif(fn):
#     from PIL import Image
#     from PIL.ExifTags import TAGS
#     i = Image.open(fn)
#     info = i._getexif()
#     ret = {}
#     for tag, value in info.items():
#         decoded = TAGS.get(tag, tag)
#         ret[decoded] = value
#     return ret


def make_thumb(fileslist):
	for f in fileslist:
		from PIL import Image
		size = 400, 480
		file, ext = os.path.splitext(f)
		print f
		try:
			im = Image.open(f)
			print im.getbbox()
			print im.getcolors()
			im.thumbnail(size, Image.ANTIALIAS)
			im.save(file + ".thumbnail", "JPEG")
		except:
			print 'failed {0}'.format(f)
			continue

def parsesoup(html, *atrs):
    from bs4 import BeautifulSoup
    import requests
    html = requests.get(url)
    soup= BeautifulSoup(html)
    body = soup.find(*atrs)
    return body

def get_attribs(url, *atrs):
    try:    
        from bs4 import BeautifulSoup
        import requests
        html = requests.get(url)
        soup = BeautifulSoup(html.text)
        if len(atrs) != 2:
            print len(atrs)
            print atrs
        else:
            print atrs[0]
            for link in soup.find_all(atrs[0]):
                if link.get(atrs[1]):
                    print(link.get(atrs[1]))
    except TypeError:
        print 'Error'


import os,sys

try:
	if sys.argv[1]:
		inputdir = sys.argv[1]
except:
	inputdir = os.path.abspath('/Volumes')

dirfileslist = recurse_dir_list(inputdir)
thumbs = make_thumb(dirfileslist)
thumbs
	

    
#parsesoup(htmlpage, 'div', {'id':'body'})

class Soup:
    def __init__(self, var):
        self.v = var


class PhotoDateDict:
    
    def __init__(self, iterable):
        self.items_list = []
        self.__update(iterable)

    def update(self, iterable):
        for item in iterable:
            self.items_list.append(item)
    
    def recurse_dir_list(self,directory):
        import os,sys,re
        filepaths = {}
        for dirpath,subdir,files in os.walk(directory):
            for f in files:
                filepaths[dirpath] = files[:]

        recursivefilelist = []
        for path,files in filepaths.items():
            for f in files:
                filepath = "{0}/{1}".format(path,f)
                recursivefilelist.append(filepath)
                sorted(recursivefilelist)

        regex = re.compile(r'^.+?[.].+?$')
        alljpgs = []
        for f in recursivefilelist:    
            foundjpgs = re.findall(regex,f)
            if foundjpgs:
                alljpgs.append(f)
        return alljpgs    
    
    def get_exif(f):
        from PIL import Image
        from PIL.ExifTags import TAGS
        i = Image.open(f)
        info = i._getexif()
        exifdict = {}
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            exifdict[decoded] = value
        return exifdict
    
    def get_photodate_dict():
        dtodict = {}
        for f in rcrsedir:
            dtod = {}
            try:
                
                dto = get_exif(f)['DateTimeOriginal'][0:10]            
                dtod['Colorstyle'] = f.splittext()[1]
                dtod['Photo_Date'] = dto
                dtod['Filepath'] = f
                
                dtodict[f] = dtod
                
            except AttributeError:
                print 'End -- None Type'
            except IOError:
                print 'IO Identity Error'
            except KeyError:
                print "No Date Time Field"


                def get_exif(f):
                        from PIL import Image
                        from PIL.ExifTags import TAGS
                        i = Image.open(f)
                        info = i._getexif()
                        exifdict = {}
                        for tag, value in info.items():
                            decoded = TAGS.get(tag, tag)
                            exifdict[decoded] = value
                        return exifdict
def get_photodate_dict(directory):
    dtodict = {}
    for f in directory:
        dtod = {}
        try:
            dto = get_exif(f)['DateTimeOriginal'][0:10]            
            fn.split('/')[-1]
            #dtod['Ext'] = fn.split('.')[0]
            dtod['Colorstyle'] = fn.split('_')[0]
            dtod['Alt'] = fn.split('_')[-1]
            dtod['Photo_Date'] = dto
            dtod['Filepath'] = f
            dtodict[f] = dtod
                   
        except AttributeError:
            print 'End -- None Type'
        except IOError:
            print 'IO Identity Error'
        except KeyError:
            print "No Date Time Field"
        return dtodict

#'2012:02:09'
rcrseapps = recurse_dir_list(dir_homedir)


url = 'http://en.wikipedia.org/wiki/List_of_HTTP_header_fields'

print get_attribs(url, 'a', 'href')

def recurse_dir_list(directory):
    import os,sys,re
    filepaths = {}
    for dirpath,subdir,files in os.walk(directory):
        for f in files:
            filepaths[dirpath] = files[:]
    recursivefilelist = []
    for path,files in filepaths.items():
        for f in files:
            filepath = "{0}/{1}".format(path,f)
            recursivefilelist.append(filepath)
            recursivefilelist = sorted(recursivefilelist)
        return recursivefilelist
            
def filterjpgs(fileslist):
    regex = re.compile(r'^.+?[.].+?$')
    alljpgs = []
    for f in fileslist:    
        foundjpgs = re.findall(regex,f)
        if foundjpgs:
            alljpgs.append(f)
    return alljpgs