from pillow import Image

class ImageFile(Image):
    def __init__(self):
	    self.__main__
	    self.Image()
	#if type(address) == type(0): 
		
    def _special(self, methodname, args):
        if methodname == '.methods':
            if not hasattr(self, '_methods'):
			    self._methods = tuple(self._listmethods())
            return self._methods
        raise NameError, "unrecognized special method name %s" % repr(methodname)
    
    def _listmethods(self, cl=None):
        if not cl: cl = self.__class__
        names = cl.__dict__.keys()
        names = filter(lambda x: x[0] != '_', names)
        names.sort()
        for base in cl.__bases__:
            basenames = self._listmethods(base)
            basenames = filter(lambda x, names=names: x not in names, basenames)
            names[len(names):] = basenames
		#return names

    def writeXmp(self,xmpkey,xmpvalue):
        import pyexiv2
        metadata = pyexiv2.ImageMetadata(self)
        metadata[xmpkey] = xmpvalue
        
    def writeIptc(self,iptckey,iptcvalue):
        import pyexiv2
    	 metadata = pyexiv2.ImageMetadata(self)
        metadata[iptckey] = iptcvalue
    
    def readIptc(self):
        import pyexiv2    
        metadata = pyexiv2.ImageMetadata(self)
        mdataprint = metadata.read()
        print metadata  
	
    def metadata_get_exif(self):
        ret = {}
        from PIL import Image
        from PIL.ExifTags import TAGS
        i = Image.open(self)
        info = i._getexif()
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value
        return ret

if __name__ == "__main__":
    #app = web.application(urls, globals())
    pass

class download(url):
    import urllib, urllib2, requests
    def GET(self, url):
    
    #path = url 
        #header('Content-type','images/jpeg')
        #header('Content-transfer-encoding','binary') 
        #header('Content-Disposition', 'attachment;filename="fname.ext"')
        return open(url, 'rb').read()

