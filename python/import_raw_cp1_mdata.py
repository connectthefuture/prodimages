#!/usr/bin/env python

def get_exif_all_data(image_filepath):
    import exiftool
    with exiftool.ExifTool() as et:
        metadata = et.get_metadata(image_filepath)
        #['XMP:DateCreated'][:10].replace(':','-')
    return metadata
    

def capture_one_colorconv(colortagindex):
    capture_one_colortag = ''
    if colortagindex       == 0:
        capture_one_colortag = 'None'
    elif colortagindex     == 1:
        capture_one_colortag = 'Issues-RED'
    elif colortagindex     == 2:    
        capture_one_colortag = 'Special-Blue'
    elif colortagindex     == 3:    
        capture_one_colortag = 'PreSelect-YELLOW'
    elif colortagindex     == 4:
        capture_one_colortag = 'Select-GREEN'
    return capture_one_colortag


#print os.environ

def recursive_dirlist_GET_COS(rootdir):
    import os,re
    regex =  re.compile(r'.*?\.cos$')
    walkedlistCOS = []
    for dirname, subdirnames, filenames in os.walk(rootdir):
        # append path of all filenames to walkedlistCOS
        for filename in filenames:
            filepath = os.path.abspath(os.path.join(dirname, filename))
            if os.path.isfile(filepath) and regex.findall(filepath):
                walkedlistCOS.append(filepath)
    walkedset = list(set(sorted(walkedlist)))
    return walkedsetCOS


def recursive_dirlist_CR2(rootdir):
    import os,re
    regex =  re.compile(r'.*?\.CR2$')
    walkedlistCR2 = []
    for dirname, subdirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            filepath = os.path.abspath(os.path.join(dirname, filename))
            if os.path.isfile(filepath) and regex.findall(filepath):
                walkedlistCR2.append(filepath)
    walkedset = list(set(sorted(walkedlist)))
    return walkedsetCR2
        
#var="exiftool -if '$jpgfromraw' -b -jpgfromraw -w %d%f_%ue.jpg -execute -if '$previewimage' -b -previewimage -w %d%f_%ue.jpg -execute -tagsfromfile @ -srcfile %d%f_%ue.jpg -overwrite_original -common_args --ext jpg DIR"

def capture1_preandselect(filepath):
    import os
    if os.path.isfile(filepath):
        directory               = os.path.dirname(filepath)
        filename                = os.path.basename(filepath)
        ### RAW image metadata
        mdata                   = get_exif_all_data(filepath)
        raw_file_keywords       = mdata.get('Keywords')
        ### cp1 XML data
        capture1settings        = "{0}/CaptureOne/Settings50/{1}.cos".format(directory,filename)
        capture1data            = get_exif_all_data(capture1settings)
        cp1indx                 = capture1data.get('XML:Color_tag_index')
        capture_one_colortag    = capture_one_colorconv(cp1indx)
        capture_one_rating      = capture1data.get('XML:Rating')
        ret_dict = {}
        if int(cp1indx) == 0:
            pass
        elif int(cp1indx) >= 1 or int(capture_one_rating) >= 1:
            cp1indx
            #extract_preselect_jpg_fr_RAW(filepath)
            #print "{1}: {0}\t\n\vRating {2}".format(filepath, capture_one_colortag, capture_one_rating)
            ret_dict['colorstyle']            = filepath.split('/')[-1][:9]
            ret_dict['file_path']             = filepath
            ret_dict['alt']                   = filepath.split('/')[-1].split('_')[1]
            ret_dict['shot_number']           = filepath.split('/')[-1].split('_')[2].split('.')[0]
            ret_dict['cp1_colortag']          = capture_one_colortag
            ret_dict['cp1_settings_filepath'] = capture1settings
            ret_dict['cp1_rating']            = capture_one_rating
            ret_dict['cp1_other_data']        = raw_file_keywords
    return ret_dict

#exifcmd = list(var.split(' '))

############################################ RUN ############################################ RUN ############################################ RUN ######################
import os, re, sys, sqlalchemy, datetime



todaysdate = str(datetime.date.today())
#todaysdate = '2014-01-27'
todaysfolder = "{0}{1}{2}_BC_SET_B".format(todaysdate[5:7],todaysdate[8:10],todaysdate[2:4])
todaysParent = "{0}_{1}".format(todaysdate[5:7],todaysdate[:4])

eFashion_root = '/mnt/Post_Ready/eFashionPush'
aPhoto_root = '/mnt/Post_Ready/aPhotoPush'

#rootdir = sys.argv[1]
#walkedout = recursive_dirlist(rootdir)

#regex = re.compile(r'.*?/[0-9]{9}_[1].*?\.[jpgJPGCR2]{3}$')
#regex_raw = re.compile(r'.*?/RAW/.+?/[0-9]{9}_[1].*?\.[jpgJPGCR2]{3}$')
#regex_raw = re.compile(r'.*?/RAW/.+?/[0-9]{9}_[1].*?\.[CR2]{3}$')
regex_raw = re.compile(r'.*?/RAW.*?/.+?/[0-9]{9}.*?\.[CR2]{3}$')

regex_still = re.compile(r'.*?/aPhotoPush/.+?/[0-9]{9}_[1].*?\.[jpgJPG]{3}$')
#regex = re.compile(r'.+?\.[jpgJPG]{3}$')
basedir = os.path.join('/mnt/Production_Raw/PHOTO_STUDIO_OUTPUT/ON_FIGURE/' + todaysParent, todaysfolder)



try:
    rootdir = sys.argv[1]
except IndexError:
    rootdir = os.path.join(basedir,'RAW')

print rootdir
rawfiles = recursive_dirlist_CR2(rootdir)

raw_settings_dict = {}
for f in rawfiles:
    try:
        cp1xmldata = capture1_preandselect(f)
        if cp1xmldata:
            raw_settings_dict[f] = cp1xmldata
    except:
        pass
#raw_selected_yellowgreen = {}
#for k,v in raw_settings_dict.iteritems():
#    if v:
#        print "Key: {0}\n\tValues: {1}".format(k,v)
#    
    
for k,v in raw_settings_dict.iteritems():
    if v['cp1_colortag']:
        try:
            ##mysql_engine = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@prodimages.ny.bluefly.com:3301/data_imagepaths')
            mysql_engine = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@prodimages.ny.bluefly.com:3301/www_django')
            connection = mysql_engine.connect()
            ## Test File path String to Determine which Table needs to be Updated Then Insert SQL statement
            sqlinsert_choose_test = v['file_path']
            regex_productionraw = re.compile(r'^/.*?/RAW.*?/.+?/[0-9]{9}_[1-9]_[0-9]{1,4}\.[a-zA-Z2]{3}$')
            #regex_mediarepo = re.compile(r'^.+?MEDIAREPO.+?\.[NnjpgJPG]$')

            ## ProdRaw Metadata Extracted and added to DB
            if re.findall(regex_productionraw, sqlinsert_choose_test):
                connection.execute("""
                                    INSERT INTO production_raw_cp1_data (colorstyle, file_path, alt, shot_number, cp1_colortag, cp1_settings_filepath, cp1_rating, cp1_other_data) 
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s )""", v['colorstyle'], v['file_path'], v['alt'], v['shot_number'], v['cp1_colortag'], v['cp1_settings_filepath'],  v['cp1_rating'], v['cp1_other_data'])
                print "Successful Insert production_raw_cp1_data --> {0}".format(k)
            
            else:
                print "Database Table not Found for Inserting {0}".format(k)
        #except OSError:
        except sqlalchemy.exc.IntegrityError:
            print "Duplicate Entry {0}".format(k)
            pass
        
        
