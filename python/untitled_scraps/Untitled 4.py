#import command
## returns 2 length tuple with 1st being unix int exit code, 2nd part of tuple is string of output
	
def exif_tag_template(exiftag, exifval, f):
	from string import Template
	exiftmpl = Template('exiftool -r -fast2 -"$exiftag=$exifval" $filename')
	exiftmpl = exiftmpl.substitute(exiftag=exiftag, exifval=exifval, filename=f)
	return exiftmpl


#cmd = "exiftool -r -fast2 -'" + exif
#(status, output) = command.getstatusoutput(cmd)
f= '/mnt/img.jpg'
exiftag = 'IPTC:Source'
exifval = 'sourceattribsVal'
exiftmpl = exif_tag_template(exiftag,exifval, f)
print exiftmpl
