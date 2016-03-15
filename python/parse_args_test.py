#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
#
# Define and Instantiate parser Base
parser = argparse.ArgumentParser(description='Initial primary script description and title') #,add_help=False)
#
######### Style
parser.add_argument('--style',
    action='store_true', help='Valid 9 Digit Bluefly Style' )
#
######### Styles List 1 or more
parser.add_argument('styles_list',
    action='append', nargs='+', help='Valid 9 Digit Bluefly Style Numbers. Each style must be separated by a space.' )
#
######### Vendor
parser.add_argument('--vendor','-vend' ,
    action='store_true', help='VendorID or Name, fuzzy searches are valid' )
#
######## Days-Since
parser.add_argument('--days-since', '-days',
    action='store', type=int, help='Number of days to include in script and related queries')
#
######## Adding Remaining Args Not Specified in Parser
parser.add_argument('args',
    nargs=argparse.REMAINDER)
#
######## Outfile - write
parser.add_argument('--outfile',
    type=argparse.FileType('w'), help='The Output Destination Absolute Filepath. Filename only is acceptable if output is to current directory')
#
####### Output Format if Image File
parser.add_argument('--format', '-fmt',
    action='store', help='The Desired Image format for Output. Options: png, jpeg, tiff, gif')
#
###### Cmdline arg as Choice for Scripts Actions. What do you want it to do.
parser.add_argument('--options', '-o',
    default='new', choices=['new', 'update', 'reload', 'delete'], help='Choice of Script Actions')
#
###### Verbose Flag
parser.add_argument('-v', '--verbose',
    action='store_true', help='verbose output' )



##new parser, for script file calling this as parent
#import argparse
#import argparse_parent_base

#parser = argparse.ArgumentParser(parents=[argparse_parent_base.parser])
#parser.add_argument('--local-arg', action="store_true", default=False)


def main():
    pass




if __name__ == '__main__':
    print parser.parse_args()
    main()
