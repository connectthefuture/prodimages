#!/usr/bin/env python
# coding: utf-8

# Defining a log function decorator to use as @log
def log(original_function, filename=None):
    from os import path, mkdir
    if filename is None:
        dbgsyncdir = '/root/DropboxSync/bflyProdimagesSync/log'
        if not path.isdir(dbgsyncdir):
            logdir = path.join(path.dirname(__file__), 'log')
        else:
            logdir = dbgsyncdir
        if not path.isdir(logdir): mkdir(logdir)
        filename = path.join(logdir, str(original_function.__name__ + "_log.txt"))
    ####
    import logging
    logging._srcfile = None
    logging.logThreads = 0
    logging.logProcesses = 0
    logging.basicConfig(filename=filename, level=logging.DEBUG) # level=logging.INFO)
    print "Logging to … {0}".format(path.abspath(filename))
    def new_function(*args, **kwargs):
        import datetime, json
        try:
            result = original_function(*args, **kwargs)
            logging.info('Start: {0}'.format(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d--%H:%M.%S')))
            logging.debug( "\n\tFunction \"%s\" called with\n\tkeyword arguments: %s\n\tpositional arguments: %s.\nThe result was %s.\n" % (original_function.__name__, json.dumps(kwargs), args, result))
            logging.info('End: {0}'.format(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d--%H:%M.%S')))
            return result
        except TypeError as e:
            logging.exception('NoneTypeError in Logger\n-might be json issue -\nTraceback:\t{0}\n\nArgs:\t{1}'.format(e, args))
            logging.info('End: {0}'.format(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d--%H:%M.%S')))
            return
    return new_function


### Generic Logger
def mr_logger(src_filepath,*args):
    import datetime
    current_dt = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
    logged_items = []
    if len(args) > 0:
        for arg in args:
            logit = "{}\t{}\n".format(current_dt,arg)
            logged_items.append(logit)
    for i in logged_items:
        with open(src_filepath, 'ab+') as f:
            f.write(i)
    return src_filepath

### Utility Funx - Get File Data
## util func calcs md5 of file
#@log
def md5_checksumer(src_filepath):
    import hashlib
    import os.path as path
    if src_filepath is not None and path.isfile(src_filepath):
        filepath = path.abspath(src_filepath)
        try:
            _file = open(filepath, "rb")
            content = _file.read()
            _file.close()
            md5 = hashlib.md5(content)
            _hash = md5.hexdigest()
            return _hash
        except IndexError:
            print "Not Index Error Checksummer"
            return False

# Converts image to jpeg
#@log
def magick_convert_to_jpeg(img, destdir=None):
    import subprocess
    ext = img.split('.')[-1]
    outfile = img.split('/')[-1].split('.')[0] + ".jpg"
    if not destdir:
        import os.path as path
        destdir = path.abspath(path.dirname(img))
        outfile = path.join(destdir, outfile)
    else:
        import os.path as path
        outfile = path.join(path.abspath(destdir), outfile)
    subprocess.call([
        'convert',
        '-colorspace',
        'RGB',
        "-format",
        ext,
        img,
        "-depth",
        "16",
        "-density",
        "72x72",
        # "-profile",
        # "/usr/local/color_profiles/AdobeRGB1998.icc",
        # "-colorspace",
        # "RGB",
        "-define",
        "jpeg:dct-method\=float",
        "-define",
        "jpeg:sampling-factor\=4:2:2",
        "-filter",
        "LanczosSharp",
        "-compress",
        "JPEG",
        '-quality',
        '90%',
        # "-profile",
        # '/usr/local/color_profiles/sRGB.icm',
        #"-interlace",
        #"Plane",
        "-colorspace",
        'sRGB',
        "-depth",
        "8",
        "-format",
        "jpeg",
        "-strip",
        outfile
        ])
    return outfile

########################
## Extracts the image metadata from file
#@log
def get_exif_all_data(src_filepath):
    import exiftool
    from os import path
    print "ExifExtract: ", type(src_filepath), src_filepath
    if src_filepath is not None:
        try:
            if src_filepath.split('.')[-1].lower() == 'jpg' or 'png':
                with exiftool.ExifTool() as et:
                    metadata = et.get_metadata(path.abspath(src_filepath))  # ['XMP:DateCreated'][:10].replace(':','-')
                return metadata
        except ValueError:
            metadata = {}
            return metadata
    else:
        pass

## Compile Inserts as dict with key == bluefly file name
@log
def compile_todict_for_class_instance_variables(fileslist=None, **kwargs):
    import os.path as path
    instance_properties = {}
    print 'Compile 131\n', fileslist, kwargs
    for img in fileslist:
        if path.isfile(img):
            bf_imageid = path.basename(img).split('.')[0]
            print img, ' <--image'
            # print locals(), "localSSY"
            try:
                # mozu_image_table = mozu_image_table_instance()
                md5checksum = md5_checksumer(img)
                print type(md5checksum)
                if not kwargs.get('tags'):
                    image_metadata = get_exif_all_data(path.abspath(img))
                    # print str(type(image_metadata.values()))
                    # tags = ['TestTag1', str(type(image_metadata.values()))] #image_metadata.values()
                    try:
                        tags = [ "{}={}".format(k,v) for k,v in image_metadata.iteritems() if k.split(':')[-1][4] == 'Date']
                        #image_metadata.values() ['XMP:DateCreated'][:10].replace(':','-')
                    except IndexError:
                        print 'Tags Index--was Attrib Error  key is: ', k
                        tags = []
                else:
                    tags = kwargs.get('tags')
                print type(img), 'Compiler151'
                instance_properties[img] = { "src_filepath": path.abspath(img), "bf_imageid": bf_imageid, "mz_imageid": kwargs.get('mz_imageid', ''), "md5checksum": md5checksum, "tags": tags }
            except OSError:
                print 'Fake OSErr, TYPE Error, Compiler150'
    return instance_properties


@log
def include_keys(dictionary, keys):
    """Filters a dict by only including certain keys only."""
    key_set = set(keys) & set(dictionary.keys())
    return dict([(key, dictionary[key]) for key in key_set])


@log
def merge_properties(obj1, obj2):
    for prop in obj1.__dict__:
        if not callable(obj1.__dict__[prop]):
            value = getattr(obj1,prop)
            if value is not None:
                setattr(obj2, prop, value)
    return obj2


#@log
def parse_pdp_html_get_mozuid_cdnkey(pdpurl):
    from bs4 import BeautifulSoup
    import urllib2
    import json
    if len(pdpurl) == 9 and pdpurl.isdigit():
        pdpurl = 'http://beta.bluefly.com/cache-clear/p/' + pdpurl
    else:
        pass
    page = urllib2.urlopen(pdpurl)
    soup = BeautifulSoup(page.read(), "lxml")
    sources=soup.findAll('script', {"id":"data-mz-preload-pagecontext"} )
    res = []
    for source in sources:
        res.append(source)
    try:
        context_data = json.loads(res[0].text)
        outdict = {}
        mz_image_data = {}
        print context_data
        mz_image_data['mz_imageid']      = context_data['cmsContext']['site']['id']
        mz_image_data['bf_imageid']      = context_data['productCode']
        mz_image_data['cdnCacheBustKey'] = context_data['cdnCacheBustKey']
        outdict[context_data['productCode']] = mz_image_data
        return outdict
    except IndexError:
        print 'IndexError: Key not found in json results at\n\turl {}'.format(pdpurl)


def insert_kwargs_to_oracle(**kwargs):
    from db import mozu_image_table_instance
    from RESTClient import __mozu_image_table_valid_keys__
    mozu_image_table = mozu_image_table_instance()
    table_args = include_keys(kwargs, __mozu_image_table_valid_keys__)
    insert_db = mozu_image_table.insert(values=dict(**table_args))
    update_db = mozu_image_table.update(values=dict(**table_args), whereclause=mozu_image_table.c.bf_imageid == table_args['bf_imageid'])
    insert_db.execute()


def netsrv101_path_maker(*args,**kwargs):
    from os import path
    netsrv101_mnt = '/mnt/images'
    ext = kwargs.get('ext', '.png')
    files_list = []
    if type(args) == 'tuple':
        args = args[1]
    for f in args:
        print f, type(f), len(f), type(args), len(args)
        src = path.join(netsrv101_mnt, f[:4], f + ext).replace('\n', '').replace('.png.png','.png').replace('.jpg.jpg','.jpg')
        files_list.append(src)
    if len(files_list) == 1:
        return files_list[0]
    else:
        return files_list

###########################
def main():
    pass


if __name__ == '__main__':
    import sys
    try:
        print sys.argv
        if sys.argv[1] and len(sys.argv[1:]) == 2:
            magick_convert_to_jpeg(sys.argv[1], destdir=sys.argv[2])
        elif len(sys.argv[1:]) == 1:
            magick_convert_to_jpeg(sys.argv[1])
    except IndexError:
        print locals()
    main()
