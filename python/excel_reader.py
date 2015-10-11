#!/usr/bin/env python
import csv
import xlrd
import sys
import os

homedir = os.path.expanduser("~")
csvfile = os.path.join(homedir, "zimages1_photoselects.csv")
outfile = os.path.join(homedir, "outfile.csv")

xlfile = open((os.path.join(homedir, "compiledutf.csv")), 'rb')


book = xlrd.open_workbook(xlfile)
sh = book.sheet_by_index(0)

convWriter = csv.writer(sys.stdout)

for rowx in range(sh.ncols):
	convWriter.writerow(xlfile)
