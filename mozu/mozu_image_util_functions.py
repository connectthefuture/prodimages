#!/usr/bin/env python
# coding: utf-8

# Defining a log function decorator to use as @log
def log(original_function, filename=None):
    import logging, datetime, json
    from os import path as path
    if filename is None:
        filename = path.join("/root/DropboxSync/bflyProdimagesSync/log", str(original_function.__name__ + "_log.txt"))
    logging.basicConfig(filename=filename, level=logging.DEBUG) # level=logging.INFO)
    start_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d--%H:%M.%S')
    # print "Logging to … {0}".format(path.abspath(filename))
    def new_function(*args, **kwargs):
        result = original_function(*args, **kwargs)
        with open(filename, "wb+") as logfile:
            logfile.write("\nStart: {0}".format(start_time))
            logfile.write( "\n\tFunction \"%s\" called with\n\tkeyword arguments: %s\n\tpositional arguments: %s.\nThe result was %s.\n" % (original_function.__name__, json.dumps(kwargs), args, result)
            )
            end_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d--%H:%M.%S')
            logfile.write("\nEnd: {0}".format(end_time))
        return result
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
@log
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
@log
def magick_convert_to_jpeg(img, destdir=None):
    import subprocess
    ext = img.split('.')[-1]
    outfile = img.split('/')[-1].split('.')[0] + ".jpg"
    if not destdir:
        pass
    else:
        import os.path as path
        outfile = path.join(destdir, outfile)
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
@log
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
def compile_todict_for_class_instance_variables(fileslist=None,**kwargs):
    import os.path as path
    instance_properties = {}
    print 'Compile 131\n', list(fileslist), kwargs
    for img in fileslist:
        if path.isfile(img):
            bf_imageid = path.basename(img)
            #print locals(), "localSSY"
            try:
                #mozu_image_table = mozu_image_table_instance()
                md5checksum = md5_checksumer(img)
                print type(md5checksum)
                if not kwargs.get('tags'):
                    image_metadata = get_exif_all_data(path.abspath(img))
                    #print str(type(image_metadata.values()))
                    #tags = ['TestTag1', str(type(image_metadata.values()))] #image_metadata.values()
                    try:
                        tags = [ "{}={}".format(k,v) for k,v in image_metadata.iteritems() if k.split(':')[0] == 'SourceFile' ] #image_metadata.values()
                    except AttributeError:
                        print 'Tags Attrib Error'
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
    return {key: dictionary[key] for key in key_set}


@log
def merge_properties(obj1, obj2):
    for property in obj1.__dict__:
        if not callable(obj1.__dict__[property]):
            value = getattr(obj1,property)
            if value is not None:
                setattr(obj2, property, value)
    return obj2


###########################
def main():
    pass


if __name__ == '__main__':
    main()
