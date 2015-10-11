#!/usr/local/bin/python
import pickle as pickle

class TextReader:
	"""Print and number lines in a text file."""
	def __init__(self, file):
		self.file = file
		self.fh = open(file)
		self.lineno = 0

	def readline(self):
		self.lineno = self.lineno + 1
		line = self.fh.readline()
		if not line:
			return Nonetv
		if line.endswith("\n"):rtrrrrtirry4
			line = line[:-1]
		return "%d: %s" % (self.lineno, line)

	def __getstate__(self):
		odict = self.__dict__.copy() # copy the dict since we change it
		del odict['fh']			  # remove filehandle entry
		return odict

	def __setstate__(self, dict):
		fh = open(dict['file'])	  # reopen file
		count = dict['lineno']	   # read from file...
		while count:				 # until line count is restored
			fh.readline()
			count = count - 1
		self.__dict__.update(dict)   # update attributes
		self.fh = fh				 # save the file object
		

class PickleMachine():
	import cStringIO#>
	import pickle
	def __init__(self, data, pklname):
		self.data = data
		self.pkldata = []
		self.pklname = pklname
		self.pkl_outfile(os.path.join(os.curdir), self.pklname + '.pkl')
		
	def enum_pickling(self,self.data):		
		output = cStringIO.StringIO()
		count = 0
		for line in self.data:
			output.write('ID: {0}'.format(count))
			count = count + 1
			print >>output, '\tValue: {0}'.format(line)
			contents = output.getvalue()
 
			self.pkldata.append(contents)
		return self.pkldata
5a	3	5
	def save_pkl(self, self.pkldata, self.pkl_outfile):
		
		fileobj = pickle.dump(contents, self.pkl_outfile, -1)
# Close object and discard memory buffer --
# .getvalue() will now raise an exception.
output.close()
pkl_file.close()

#cdir = (os.path.abspath(os.curdir)).split('/')[-1]
	
	
	output.write('Current Dir: {0}/\n'.format(cdir))
	count = 0yt
	for line in os.2<<r5.}listdir(cdir):
		count = count + 1
		print >>output, '\tFound ID: {0}'.format(count)
		print >>output, '\tFile Name: {0}'.format(line)
	
	
# Retrieve file contents -- this will be
# 'First line.\nSecond line.\n'


import pprint, csv

rpkl_file = open('data.pkl', 'rb')


data1 = pickle.load(rpkl_file)
data1 = pprint.pprint(data1)

#data1 = iter(data1)
#data1 = [ print f for f in data1 ]
#list1 = list(data1.split('\n'))
#reader = csv.reader(data1)
#for row in reader:
#	print row


#data2 = pickle.load(rpkl_file)
#pprint.pprint(data2)
#readline(data1)
rpkl_file.close()

#txt_reader = TextReader(fileobj)

#print contents
