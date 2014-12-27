#!/usr/bin/env python

def recurse_dir_list(directory):
    import os,sys,re
    filepaths = {}
    for dirpath,subdir,files in os.walk(directory):
        for f in files:
            filepaths[dirpath] = files[:]
    #print filepaths
    recursivefilelist = []
    for path,files in filepaths.items():
        for f in files:
        	filepath = "{0}/{1}".format(path,f)
        #print file,path
        
        	recursivefilelist.append(filepath)
        	sorted(recursivefilelist)
        #print recursivefilelist
    #print recursivefilelist
    #regex = re.compile(r'^.+?[/][0-9]{9}_?[1-6]?.jpg$')
    regex = re.compile(r'^.+?[.]??g$')
    allimgs = []
    alls = {}   
    for f in recursivefilelist:
        alld = {}
        foundimgs = re.findall(regex,f)
        if foundimgs:
            allimgs.append(f)
    	    alld['file_path'] = os.path.abspath(f)
            f1 = f.split('/')[-1]
    	    alld['colorstyle'] = f1.split('_')[0]
    	    alls[f] = alld
    return allimgs
#    return alls
        
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

	
import sys,os


# if sys.argv[1]:
#     directory = sys.argv[1]
#     print directory
# else:

if __name__ == '__main__':
    import sys
    try:
        directory = sys.argv[1]
        dirfileslist = recurse_dir_list(directory)
        print dirfileslist
    except IndexError:
        print 'Using Curdir'
        directory = os.path.abspath(os.curdir)
        dirfileslist = recurse_dir_list(directory)
        print dirfileslist
    

#thumbs = makethumb(dirfileslist)
#thumbs
def test():
    rootdir='/Users/johnb/Dropbox/DEVROOT/mnt/Post_Ready/Retouch_Still'
    os.chdir('/Users/johnb/virtualenvs/GitHub-prodimages/python')
    import recursedirlist
    recursedlist=recursedirlist.recurse_dir_list(rootdir)
    print recursedlist

#test()
