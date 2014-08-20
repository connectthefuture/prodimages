#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import os,sys

def find_duplicate_imgs(dname):
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

dname = sys.argv[1]
def main():
    duplicates = find_duplicate_imgs(dname)
    return duplicates

if __name__ == '__main__':
    unique_files, dups = main()
    unique_files.values()