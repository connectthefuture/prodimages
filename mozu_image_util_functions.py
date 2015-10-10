#!/usr/bin/env python
# coding: utf-8

# Defining a log function decorator to use as @log
def log(original_function, filename=None):
    import logging
    from os import path as path
    if filename is None:
        filename = str("__main__" + "_log.txt")
    logging.basicConfig(filename=filename, level=logging.INFO)
    print "Logging to … {0}".format(path.abspath(filename))
    def new_function(*args, **kwargs):
        result = original_function(*args, **kwargs)
        with open(filename, "ab+") as logfile:
            logfile.write("Function '%s' called with positional arguments %s and keyword arguments %s. The result was %s.\n" % (original_function.__name__, args, kwargs, result))
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
        except:
            return False

# Converts image to jpeg
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
        "-interlace",
        "Plane",
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
def get_exif_all_data(src_filepath):
    import exiftool
    print type(src_filepath), src_filepath
    if src_filepath is not None:
        if src_filepath.split('.')[-1].lower() == 'jpg' or 'png':
            with exiftool.ExifTool() as et:
                metadata = et.get_metadata(src_filepath)  # ['XMP:DateCreated'][:10].replace(':','-')
            return metadata
    else: pass

## Compile Inserts as dict with key == bluefly file name
def compile_todict_for_class_instance_variables(list_of_images,**kwargs):
    instance_properties = {}
    for img in list_of_images:
        bf_imageid = img.split('/')[-1]
        
        try:
            #mozu_image_table = mozu_image_table_instance()
            md5checksum = md5_checksumer(img)
            if not kwargs.get('tags'):
                image_metadata = get_exif_all_data(img)
                tags = image_metadata.values()
            else:
                tags = kwargs.get('tags')
        except TypeError: 
            print 'TYPE Error'
            pass

        instance_properties[img] = dict(bf_imageid  = bf_imageid, 
                                        mz_imageid = kwargs.get('mz_imageid', 'NA'), 
                                        md5checksum = md5checksum,
                                        tags = (list(set(sorted(tags)))))
        return instance_properties

###########################

def main():
    pass


if __name__ == '__main__':
    main()
