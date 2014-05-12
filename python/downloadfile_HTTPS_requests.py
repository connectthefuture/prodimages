#!/usr/bin/env python
import os, sys, requests

urlget = sys.argv[1]
localpath = sys.argv[2]
 
res = requests.get(urlget, stream=True, timeout=1)
with open(localpath, 'ab+') as f:
    f.write(res.content)
    f.close()
