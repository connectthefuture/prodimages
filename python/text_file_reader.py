#!/usr/bin/env python
# -*- coding: utf-8 -*-


def fmain(fpath):
    lnlist = []
    print dir(fpath)
    lines = [ l for l in fpath.read().split('\r') ]
    return lines

def main(url):
    import requests
    resp = requests.get(url)
    if resp.apparent_encoding == 'ascii':
        lines_list = resp.content.split('\r')


####################################
# Define and Instantiate parser Base
import argparse
#####
parser = argparse.ArgumentParser(description='Initial primary script description and title') #,add_help=False)
#
###### Cmdline arg as Choice for Scripts Actions. What do you want it to do.
parser.add_argument('--file', '-f',
    type=argparse.FileType('r'), help='Provide the full path to the file to be read')
##
######## Outfile - write
parser.add_argument('--outfile', '-O',
    type=argparse.FileType('w'), help='The Output destination absolute filepath. Reletive filepaths are only acceptable if output is to current directory')
#
parser.add_argument('--options', '-o',
    default='split', choices=['split', 'line', 'replace', 'delete'], help='Choice of Script Actions')

if __name__ == '__main__':
    args = parser.parse_args()
    print dir(parser.parse_args())
    parsedargs=parser.parse_args()
    res = fmain(parsedargs.file)
    print('\n\n\n\n\n---- END ------\n\n\n\n')
    print res
