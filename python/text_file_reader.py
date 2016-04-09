#!/usr/bin/env python
# -*- coding: utf-8 -*-


def fmain(fpath,options):
    lnlist = []
    #print dir(options), options
    if options == 'line':
        lines = fpath.read().replace('\r',' ')
    elif options == 'split':
        lines = [ l for l in fpath.read().split('\r') if l is not None ]
    else: #options ==   :
        lines = fpath
    print options, '<---- Options'
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
    default='split', choices=['split', 'line', 'replace', 'delete'], help='Choice of Script Actions. Defaults to [split]')

if __name__ == '__main__':
    args = parser.parse_args()
    # print dir(parser.parse_args())
    parsedargs=parser.parse_args()
    res = fmain(parsedargs.file,parsedargs.options)
    print('\n\n--- START ---\n\n')
    print res
    print('\n\n---- END ----\n\n')
