#!/usr/bin/env python
# coding: utf-8

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
def compile_data_db_import(list_of_images,**kwargs):
    images_insert_dict = {}
    for img in list_of_images:
        bf_imageid = img.split('/')[-1]
        
        try:
            mozu_image_table = mozu_image_table_instance()
            md5checksum = md5_checksumer(img)
            image_metadata = get_exif_all_data(img)
        except TypeError: 
            print 'TYPE Error'
            pass

        images_insert_dict[img] = dict(bf_imageid  = bf_imageid, 
                                                mz_imageid  = kwargs.get('mz_imageid', 'NA'), 
                                                md5checksum = md5checksum)
                                                #image_metadata = image_metadata)
        #print 'METADATA --> ', image_metadata
    return images_insert_dict

### Generic Logger
def mr_logger(filepath,*args):
    import datetime
    current_dt = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
    logged_items = []
    if len(args) > 0:
        for arg in args:
            logit = "{}\t{}\n".format(current_dt,arg)
            logged_items.append(logit)
    for i in logged_items:
        with open(filepath, 'ab+') as f:
            f.write(i)
    return filepath

###########################
def main():
    pass


if __name__ == '__main__':
    main()