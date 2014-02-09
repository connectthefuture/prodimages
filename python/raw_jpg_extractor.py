#!/usr/bin/env python

import os,sys,subprocess,shutil

#print os.environ


#var="exiftool -if '$jpgfromraw' -b -jpgfromraw -w %d%f_%ue.jpg -execute -if '$previewimage' -b -previewimage -w %d%f_%ue.jpg -execute -tagsfromfile @ -srcfile %d%f_%ue.jpg -overwrite_original -common_args --ext jpg DIR"


#exifcmd = list(var.split(' '))


rawimgdir=sys.argv[1]
#rawimgdir = os.path.abspath(os.path.dirname(rawimgdir))
outdir = os.path.join(rawimgdir,'../../OUTPUT')
try:
    if os.path.isdir(outdir):
        shutil.makedirs(outdir)
except:
    pass#print "EXCEPTION DIR"


subprocess.call([
        
         'exiftool',
         '-if',
         '$jpgfromraw',
         '-b',
         '-jpgfromraw',
         '-w',
         '%d/../../OUTPUT/%f_%ue.jpg',
         '-execute',
         '-if',
         '$previewimage',
         '-b',
         '-previewimage',
         '-w',
         '%d/../../OUTPUT/%f_%ue.jpg',
         '-execute',
         '-tagsfromfile',
         '@',
         '-srcfile',
         '%d/../../OUTPUT/%f_%ue.jpg',
         '-overwrite_original',
         '-common_args',
         '-ext',
         'CR2',
         rawimgdir])

