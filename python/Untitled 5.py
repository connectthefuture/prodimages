#!/usr/bin/python
import os, collections
dir_pushstill 	        = os.path.abspath("/mnt/Post_Ready/aPhotoPush")
dir_homedir 	        = os.path.expanduser('~') 
dir_zimages 	        = os.path.abspath("/mnt/Post_Ready/zImages_1")


#for root, subFolders, fileNames in os.walk(dir_zimages):
#    outfileName = os.path.join(dir_homedir, 'walkedFolderOut.csv')
#    with open(outfileName, 'w') as folderOut:
#        for folder in subFolders:
#            print "%s has subdir %s" % (root,folder)
#        for filen in fileNames:
#            filePath = os.path.join(root, filen)
#            with open( filePath, 'r' ) as f:
#                toWrite = f.read()
#                folderOut.write("The file %s contains %s" % (filePath, toWrite))
#                folderOut.write(toWrite)
                
                
                




#import os
#import sys
#
#fileList = []
#fileSize = 0
#folderCount = 0
#rootdir = sys.argv[1]
#
#for root, subFolders, files in os.walk(rootdir):
#    folderCount += len(subFolders)
#    for file in files:
#        f = os.path.join(root,file)
#        fileSize = fileSize + os.path.getsize(f)
#        #print(f)
#        fileList.append(f)
#
#print("Total Size is {0} bytes".format(fileSize))
#print("Total Files ", len(fileList))
#print("Total Folders ", folderCount)                
import sqlalchemy
orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
connection = orcl_engine.connect()
def recursiveFileList(dir='.'):
    d = collections.defaultdict(int)
    d
    for rootdir, subdir, fileNames in os.walk(dir):
        #print rootdir, subdir, fileNames
        filePath = {}
        filePath['rootDir'] = rootdir
        filePath['subDir'] = subdir 
        filePath['fname'] = fileNames
        d['fileDict'] = filePath
    return d
#argDir = dir_pushstill
#argDir = sys.argv[0]

#def recursiveFileList(dir='.'):
#    d = collections.defaultdict(int)
#    for rootdir, subdir, fileNames in os.walk(dir):
#        for f in fileNames:
#            filePath = fileNAmes[f]
#            d[filePath] += 1
#            print [d]
#    return d
#
defd = recursiveFileList(dir_pushstill)