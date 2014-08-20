#!/usr/bin/env python
# -*- coding: utf-8 -*-

def find_duplicate_imgs(dname):
    import hashlib
    import os
    
    hash_table = {}
    dups = []

    for img in os.listdir(dname):
        #print img
        img_path = os.path.join(dname, img)
        _file = open(img_path, "rb")
        content = _file.read()
        _file.close()
        md5 = hashlib.md5(content)
        _hash = md5.hexdigest()

        if _hash in hash_table.keys():
            dups.append(img)
        else:
            hash_table[_hash] = img
    return hash_table, dups
            
############################################
############ RUN ###########################
############################################

import os,sys

dname = sys.argv[1]
def main():
    unique_files, duplicates = find_duplicate_imgs(dname)
    unique_files = unique_files.values()
    return unique_files, duplicates 

if __name__ == '__main__':
    result = main()
    print result