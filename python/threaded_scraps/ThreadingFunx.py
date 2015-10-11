import Queue
from threading import Thread
import urllib, re
import os,sys,re

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


def threadfunc(filename):
	#regex = r'<title>.+?</title>'
	regex = r'.+?'
	pattern = re.compile(regex)
	#print sys.argv[0]
	try:
		item = filename
		if not filename:
			if url:	
				htmltext = urllib.urlopen(url).read()
				item = htmltext	
		results = re.findall(regex, item)
		print results
	except :
		#print sys.stderr
		pass

#symbolslist = open(symbols.txt).read()
#symbolslist = symbolslist.replace(" ", "").split(',')

	#print htmltext[0:100]
##create array with split
#urls ="http://yahoo.com http://google.com http://wikipedia.com http://cnn.com".split()
directory = os.path.abspath('sceneimages')
dirwalked = recurse_dir_list(directory)

threadlist = []
for	f in dirwalked:
	threaditer = Thread(target=threadfunc, args=(f))
	threaditer.start()
	threadlist.append(threaditer)

## joins sub threads to main Thread	
for thread in threadlist:
	thread.join()
	
print threadlist
print thread
