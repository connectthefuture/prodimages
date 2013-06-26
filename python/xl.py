#!/usr/bin/python

import csv,xlrd,sys
book = xlrd.open_workbook(sys.argv[1])
sh = book.sheet_by_index(0)

convWriter = csv.writer(sys.stdout,delimiter=',')
for rx in range(sh.nrows):
		convWriter.writerow((sh.cell_value(rowx=rx,colx=1),sh.cell_value(rowx=rx,colx=2)))
