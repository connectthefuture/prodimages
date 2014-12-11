#!/usr/bin/env python
# -*- coding: utf-8 -*-

def find_duplicate_imgs(dname):
    import hashlib
    import os, __builtin__
    
    hash_table = {}
    dups = []
    dname = os.path.abspath(dname)
    os.chdir(os.path.abspath(dname))
    #print os.listdir(dname)
    for img in os.listdir(dname):
        print img
        img_path = os.path.join(dname, img)
        try:
            _file = __builtin__.open(img_path, "rb")
            content = _file.read()
            _file.close()
            md5 = hashlib.md5(content)
            _hash = md5.hexdigest()

            if _hash in hash_table.keys():
                dups.append(img)
            else:
                hash_table[_hash] = img
        except:
            pass
    return hash_table, dups
            
############################################
############ RUN ###########################
############################################

import os,sys

dname = sys.argv[1]
def main():
    md5checksum_pairs, duplicates = find_duplicate_imgs(dname)
    unique_files = md5checksum_pairs.values()
    return unique_files, duplicates, md5checksum_pairs

if __name__ == '__main__':
    unique_files, duplicates, md5checksum_pairs = main()
    print unique_files, duplicates, md5checksum_pairs