#!/usr/bin/env python

import os,sys,subprocess

#print os.environ


#var="exiftool -if '$jpgfromraw' -b -jpgfromraw -w %d%f_%ue.jpg -execute -if '$previewimage' -b -previewimage -w %d%f_%ue.jpg -execute -tagsfromfile @ -srcfile %d%f_%ue.jpg -overwrite_original -common_args --ext jpg DIR"


#exifcmd = list(var.split(' '))


rawimgdir=sys.argv[1]

subprocess.call([
        
         'exiftool',
         '-if',
         '$jpgfromraw',
         '-b',
         '-jpgfromraw',
         '-w',
         '%d%f_%ue.jpg',
         '-execute',
         '-if',
         '$previewimage',
         '-b',
         '-previewimage',
         '-w',
         '%d%f_%ue.jpg',
         '-execute',
         '-tagsfromfile',
         '@',
         '-srcfile',
         '%d%f_%ue.jpg',
         '-overwrite_original',
         '-common_args',
         '-ext',
         'CR2',
         rawimgdir])