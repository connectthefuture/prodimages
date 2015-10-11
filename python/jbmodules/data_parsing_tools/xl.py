#!/usr/bin/env python

import csv,xlrd,sys
book = xlrd.open_workbook('/Users/johnb/Desktop/SampleInProgressReport.xls')##sys.argv[1])
sh = book.sheet_by_index(0)

convWriter = csv.writer(sys.stdout,delimiter=',', dialect='excel')
numcols=sh.ncols

for rx in range(sh.nrows):
	print "NEWROW"
	for cx in range(sh.ncols):
		#print rx, cx
		rowhead = sh.cell_value(rowx=0,colx=cx)
		rowval = sh.cell_value(rowx=rx,colx=cx)
		#convWriter.writerow(rowval)
		print rowhead,rowval
