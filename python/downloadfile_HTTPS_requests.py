#!/usr/bin/env python
def dloader(url,stylenum,imgnum):
	import os, sys, requests, re
	regex=re.compile(r'^(http://.*?)\?dl\=\d{1,2}.*?$')
	urlget = url
	localpath = os.path.join('/Users/johnb/Pictures', stylenum+ '_'+imgnum+'.jpg')
	import subprocess
	subprocess.call(['wget', url, '-o',localpath])
	if regex.findall(urlget):
		regexfnd=regex.findall(urlget)
		print regexfnd 
		res = requests.get(urlget, stream=True, timeout=5).content
		with __builtin__.open(localpath, 'wb') as f:
		    f.write(res.content)
		    f.close()
	else: pass

