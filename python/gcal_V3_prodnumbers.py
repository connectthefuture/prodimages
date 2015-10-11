#!/usr/bin/env python
# -*- coding: utf-8 -*-


def getServiceEvents():
    # import gflags
    from os import chdir, path
    from jbmodules.http_tools.auth.Google.googleapi_service import instantiate_google_calendar_service

    ##########################Vars
    
    prodnumberscal = 'k8oohvl27sq3u0odgafpbmdl6s@group.calendar.google.com'
    #prodnumberscal = 'https://www.google.com/calendar/feeds/k8oohvl27sq3u0odgafpbmdl6s@group.calendar.google.com/'
    # prodnumberscal = 'https://www.google.com/calendar/feeds/k8oohvl27sq3u0odgafpbmdl6s@group.calendar.google.com/private-cfbcfde94d17e48fbf1f824a8536e0ba/basic'

    # Build a service object for interacting with the API.
    service = instantiate_google_calendar_service()
    #service = create_googleapi_service(scope='calendar', version='v3')
    #build(serviceName='calendar', version='v3', http=http)

    # Getting All Event Ids
    page_token = None
    events_list = []
    try:
        while True:
            events = service.events().list(calendarId=prodnumberscal, pageToken=page_token).execute()
            for event in events['items']:
                event_id = event['id']
                events_list.append(event_id)
                #print event_id
            page_token = events.get('nextPageToken')
            if not page_token:
                break
    except:
        page_token = None
        while True:
            events = service.events().list(calendarId=prodnumberscal, pageToken=page_token).execute()
            for event in events['items']:
                event_id = event['id']
                events_list.append(event_id)
                #print event_id
            page_token = events.get('nextPageToken')
            if not page_token:
                break

    return service, events_list


###########################
####  END AUTH SECTION
###########################
#############################Get Data to send to API###########################
#from python.gcal_functions import stillcomplete, fashioncomplete, sql_query_production_numbers

## Walk Root Directory and Return List or all Files in all Subdirs too
def recursive_dirlist(rootdir):
    import os
    walkedlist = []
    for dirname, subdirnames, filenames in os.walk(rootdir):
        # append path of all filenames to walkedlist
        for filename in filenames:
            file_path = os.path.abspath(os.path.join(dirname, filename))
            if os.path.isfile(file_path):
                walkedlist.append(file_path)
                # Advanced usage:
                # editing the 'dirnames' list will stop os.walk() from recursing into there.
                #if '.git' in dirnames:
                # don't go into any .git directories.
                #    dirnames.remove('.git')
    walkedset = list(set(sorted(walkedlist)))
    return walkedset


###############
def insert_mysql_numbers(roletotalsdict):
    import sqlalchemy
    marketplace = ''
    for k,v in roletotalsdict.iteritems():
        try:
            marketplace = v['marketplace']
        except:
            v['marketplace'] = ''
            pass
        try:
            ##mysql_engine = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@prodimages.ny.bluefly.com:3301/data_imagepaths')
            mysql_engine = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@prodimages.ny.bluefly.com:3301/data_reporting')
            connection = mysql_engine.connect()
            ## Test File path String to Determine which Table needs to be Updated Then Insert SQL statement
            sqlinsert_choose_test = v['role']

            ## ProdRaw Metadata Extracted and added to DB
            if sqlinsert_choose_test:
                connection.execute("""
                                    INSERT INTO production_numbers (complete_dt, role, total, marketplace)
                                    VALUES (%s, %s, %s, %s)
                                    ON DUPLICATE KEY UPDATE
                                    marketplace  = VALUES(marketplace);
                                    """, k, v['role'], v['total'], v['marketplace'])
                print "Successful Insert production_numbers --> {0}".format(k)

            else:
                print "Database Entry NOT VALID for Inserting {0}".format(k)
        #except OSError:
        except sqlalchemy.exc.IntegrityError:
            print "Duplicate Entry {0}".format(k)
            pass


###############

def sql_query_production_numbers():
    import sqlalchemy
    import datetime
    from collections import defaultdict
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')
    connection = orcl_engine.connect()

    ### Get Production Complete Totals and Build Dict of key value pairs
    querymake_prodnumbers = """SELECT distinct COUNT(DISTINCT POMGR.PRODUCT_COLOR.ID) as completion_total,
    POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT as prod_complete_dt
    FROM POMGR.PRODUCT_COLOR
    INNER JOIN POMGR.SKU
    ON
      POMGR.SKU.PRODUCT_COLOR_ID = POMGR.PRODUCT_COLOR.ID
    WHERE
      POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT >= TRUNC(sysdate - 30)
        and substr(pomgr.sku.sku_code,1,1) = '8'
    GROUP BY
        POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT
    ORDER BY POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT DESC"""
    prodcomplete = connection.execute(querymake_prodnumbers)
    prodcomplete_dict = {}
    for row in prodcomplete:
        tmp_dict = {}
        tmp_dict['total'] = row['completion_total']
        tmp_dict['role'] = 'Production'
        prodcomplete_dict[row['prod_complete_dt']] = tmp_dict

    ### Get Image_Completion Complete Totals and Build Dict of key value pairs
    querymake_retouchnumbers = """SELECT COUNT(DISTINCT POMGR.PRODUCT_COLOR.ID) as retouch_total, POMGR.PRODUCT_COLOR.IMAGE_READY_DT as retouch_complete_dt
    FROM POMGR.PRODUCT_COLOR
    INNER JOIN POMGR.SKU
    ON
      POMGR.SKU.PRODUCT_COLOR_ID = POMGR.PRODUCT_COLOR.ID
    WHERE
      POMGR.PRODUCT_COLOR.IMAGE_READY_DT >= TRUNC(SysDate - 30)
    and substr(pomgr.sku.sku_code,1,1) = '8'
    GROUP BY
      POMGR.PRODUCT_COLOR.IMAGE_READY_DT
    ORDER BY POMGR.PRODUCT_COLOR.IMAGE_READY_DT DESC"""
    retouchcomplete = connection.execute(querymake_retouchnumbers)
    retouchcomplete_dict = {}
    for row in retouchcomplete:
        tmp_dict = {}
        tmp_dict['total'] = row['retouch_total']
        tmp_dict['role'] = 'Image_Completion'
        retouchcomplete_dict[row['retouch_complete_dt']] = tmp_dict

    ### Get Copy Complete Totals and Build Dict of key value pairs
    querymake_copynumbers = """SELECT COUNT(DISTINCT POMGR.PRODUCT_COLOR.ID) as copy_total, to_date(POMGR.PRODUCT_COLOR.COPY_READY_DT, 'YYYY-MM-DD') as copy_complete_dt
    FROM POMGR.PRODUCT_COLOR
    INNER JOIN POMGR.SKU
    ON
      POMGR.SKU.PRODUCT_COLOR_ID = POMGR.PRODUCT_COLOR.ID
    WHERE  POMGR.PRODUCT_COLOR.COPY_READY_DT >= TRUNC(SysDate - 30)
        and substr(pomgr.sku.sku_code,1,1) = '8'
    GROUP BY to_date(POMGR.PRODUCT_COLOR.COPY_READY_DT, 'YYYY-MM-DD')
    ORDER BY to_date(POMGR.PRODUCT_COLOR.COPY_READY_DT, 'YYYY-MM-DD') DESC"""
    copycomplete = connection.execute(querymake_copynumbers)
    copycomplete_tmpdict = {}
    for row in copycomplete:
        tmp_dict = {}
        tmp_dict['total'] = row['copy_total']
        tmp_dict['role'] = 'Copy'
        copycomplete_tmpdict[row['copy_complete_dt']] = tmp_dict

    ## Super Coersion of nums and year due to time stamp occasionally on copy dates
    copycomplete_dict = {}
    for k,v in copycomplete_tmpdict.iteritems():
        tmp_dict = {}
        tmp_dict['total'] = v['total']
        tmp_dict['role'] = v['role']
        dt = str(datetime.datetime.strptime(str(k), "%Y-%m-%d %H:%M:%S"))
        dtsplit = dt.replace('00','', 2)
        dtsplit = "20{2:.2}-{1:.2}-{0:.2} 00:00:00".format(dtsplit[:2],dtsplit[3:5],dtsplit[6:8])
        dtsplit = datetime.datetime.strptime(dtsplit, "%Y-%m-%d %H:%M:%S")
        copycomplete_dict[dtsplit] = tmp_dict

    ### Get Sample Received Totals and Build Dict of key value pairs
    querymake_sample_received = """SELECT COUNT(DISTINCT POMGR.PRODUCT_COLOR.ID) as sample_total,
    to_date(POMGR.SAMPLE_TRACKING.CREATE_DT, 'YYYY-MM-DD') AS sample_dt
    FROM POMGR.PRODUCT_COLOR
    LEFT JOIN POMGR.SAMPLE ON POMGR.PRODUCT_COLOR.ID = POMGR.SAMPLE.PRODUCT_COLOR_ID
    LEFT JOIN POMGR.SAMPLE_TRACKING ON POMGR.SAMPLE.ID = POMGR.SAMPLE_TRACKING.SAMPLE_ID
    LEFT JOIN POMGR.LK_SAMPLE_STATUS ON POMGR.SAMPLE_TRACKING.STATUS_ID = POMGR.LK_SAMPLE_STATUS.ID
    WHERE (POMGR.SAMPLE_TRACKING.CREATE_DT >= TRUNC(SysDate - 30)
    AND POMGR.LK_SAMPLE_STATUS.NAME = 'Scanned In at BF-QL')
    GROUP BY to_date(POMGR.SAMPLE_TRACKING.CREATE_DT, 'YYYY-MM-DD')
    ORDER BY to_date(POMGR.SAMPLE_TRACKING.CREATE_DT, 'YYYY-MM-DD') DESC"""
    samples_received = connection.execute(querymake_sample_received)
    samples_received_tmpdict = {}
    for row in samples_received:
        tmp_dict = {}
        tmp_dict['total'] = row['sample_total']
        tmp_dict['role'] = 'Samples_Received'
        samples_received_tmpdict[row['sample_dt']] = tmp_dict

    ## Super Coersion of nums and year due to time stamp occasionally on copy dates
    samples_received_dict = {}
    for k,v in samples_received_tmpdict.iteritems():
        tmp_dict = {}
        tmp_dict['total'] = v['total']
        tmp_dict['role'] = v['role']
        dtpresplit = str(datetime.datetime.strptime(str(k), '%Y-%m-%d %H:%M:%S'))
        dtsplit = dtpresplit.replace('00','', 2)
        dtsplit = "20{2:.2}-{1:.2}-{0:.2} 00:00:00".format(dtsplit[:2],dtsplit[3:5],dtsplit[6:8])
        dtsplit = datetime.datetime.strptime(dtsplit, '%Y-%m-%d %H:%M:%S')
        samples_received_dict[dtsplit] = tmp_dict

    connection.close()
    return prodcomplete_dict, retouchcomplete_dict, copycomplete_dict, samples_received_dict



def fashioncomplete():
    import datetime, re
    from collections import defaultdict
    ######  Recursively search Photo Folders and get counts of shots by date
    ## rootdir_fashion = '/mnt/Post_Ready/Retouch_Fashion'
    rootdir_fashion = '/mnt/Post_Ready/eFashionPush'
    #####  Walk rootdir tree compile dict of Walked Directory
    walkedout_fashion = recursive_dirlist(rootdir_fashion)
    #### Parse Walked Directory Paths Output stylestringssdict
    stylestringsdict_fashion = walkeddir_parse_stylestrings_out(walkedout_fashion)
    ### Get and Collect Counts of fashion and still sets by date
    fashiond = defaultdict(list)
    for row in stylestringsdict_fashion.itervalues():
        try:
            file_path = row['file_path']
            photo_date = row['photo_date']
            dt = photo_date
            dt = "{} 00:00:00".format(dt)
            dt = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
            #### 5 digit date
            if type(dt) == datetime.datetime:
                photo_date = dt
                fashiond[photo_date].append(file_path)
        except:
            pass

    ## Count the Grouped Files
    # fashioncomplete_dict = defaultdict(int)
    # for k in fashiond:
    #     fashioncomplete_dict[k] +=1
    fashioncomplete_dict = {}
    for k,v in fashiond.iteritems():
        tmp_dict = {}
        tmp_dict['role'] = 'Fashion'
        tmp_dict['total'] = len(v)
        fashioncomplete_dict[k] = tmp_dict
        #    fashioncomplete_dict['Role'] = 'Fashion_Photo'
        #    fashioncomplete_dict['shot_count'] = len(v)
    return fashioncomplete_dict


def lookletcomplete():
    import datetime, re
    from collections import defaultdict
    ######  Recursively search Photo Folders and get counts of shots by date
    regex_photolooklet = re.compile(r'^/.+?/Post_Ready/.+?Push/.*?[L]{2}/.*?[0-9]{9}_[1-6]\.[jpgJPG]{3}$')
    regex_postreadylooklet = re.compile(r'^/Retouch_.+?/.*?[L]{2}/.*?[0-9]{9}_[1-6]\.[jpgJPG]{3}$')
    ## rootdir_looklet = '/mnt/Post_Ready/Retouch_Still'
    rootdir_looklet = '/mnt/Post_Ready/aPhotoPush'
    #####  Walk rootdir tree compile dict of Walked Directory
    walkedout_looklet = recursive_dirlist(rootdir_looklet)
    #### Parse Walked Directory Paths Output stylestringssdict
    stylestringsdict_looklet = walkeddir_parse_stylestrings_out(walkedout_looklet)
    ### Get and Collect Counts of looklet and still sets by date
    lookletd = defaultdict(list)
    for row in stylestringsdict_looklet.itervalues():
        file_path = row['file_path']
        if regex_photolooklet.findall(file_path):
            try:
                file_path = row['file_path']
                photo_date = row['photo_date']
                dt = photo_date
                dt = "{} 00:00:00".format(dt)
                dt = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
                #### 5 digit date
                if type(dt) == datetime.datetime:
                    photo_date = dt
                    lookletd[photo_date].append(file_path)
                    #        else:
                    #            dt = ''
                    #            dt = "2000-01-01 00:00:00".format(dt)
                    #            dt = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
                    #            photo_date = dt
                    #            lookletd[photo_date].append(file_path)
            except:
                pass
        else:
            pass

    ## Count the Grouped Files
    # lookletcomplete_dict = defaultdict(int)
    # for k in lookletd:
    #     lookletcomplete_dict[k] +=1
    lookletcomplete_dict = {}
    for k,v in lookletd.iteritems():
        tmp_dict = {}
        tmp_dict['role'] = 'Looklet'
        tmp_dict['total'] = len(v)
        lookletcomplete_dict[k] = tmp_dict
        #    lookletcomplete_dict['Role'] = 'Fashion_Photo'
        #    lookletcomplete_dict['shot_count'] = len(v)
    return lookletcomplete_dict

def stillcomplete():
    import datetime, re
    from collections import defaultdict
    ######  Recursively search Photo Folders and get counts of shots by date
    regex_photostill = re.compile(r'^/.+?/Post_Ready/.+?Push/.*?[^L]{2}/.*?[0-9]{9}_[1-6]\.[jpgJPG]{3}$')
    regex_postreadystill = re.compile(r'^/Retouch_.+?/.*?[^L]{2}/.*?[0-9]{9}_[1-6]\.[jpgJPG]{3}$')
    ## rootdir_still = '/mnt/Post_Ready/Retouch_Still'
    rootdir_still = '/mnt/Post_Ready/aPhotoPush'
    #####  Walk rootdir tree compile dict of Walked Directory
    walkedout_still = recursive_dirlist(rootdir_still)
    #### Parse Walked Still Directory Paths Output stylestringssdict
    stylestringsdict_still = walkeddir_parse_stylestrings_out(walkedout_still)
    ### Now the still sets counts by date
    stilld = defaultdict(list)
    for row in stylestringsdict_still.itervalues():
        file_path = row['file_path']
        if regex_photostill.findall(file_path):
            try:
                file_path = row['file_path']
                photo_date = row['photo_date']
                dt = photo_date
                dt = "{} 00:00:00".format(dt)
                dt = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
                #### 5 digit date
                if type(dt) == datetime.datetime:
                    photo_date = dt
                    stilld[photo_date].append(file_path)
                    #        else:
                    #            dt = ''
                    #            dt = "2000-01-01 00:00:00".format(dt)
                    #            dt = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
                    #            photo_date = dt
                    #            stilld[photo_date].append(file_path)
            except:
                pass
        else:
            pass
    ## Count the Grouped Files
    stillcomplete_dict = {}
    for k,v in stilld.iteritems():
        tmp_dict = {}
        tmp_dict['role'] = 'Still'
        tmp_dict['total'] = len(v)
        stillcomplete_dict[k] = tmp_dict
        #    stillcomplete_dict['Role'] = 'Still_Photo'
        #    fashioncomplete_dict['shot_count'] = len(v)
    return stillcomplete_dict


## Extract All Metadata from Image File as Dict using PIL
def get_exif(file_path):
    from PIL import Image
    from PIL.ExifTags import TAGS
    exifdata = {}
    im = Image.open(file_path)
    info = im._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        exifdata[decoded] = value
    return exifdata


###
## Convert Walked Dir List To Lines with path,photo_date,stylenum,alt. Depends on above "get_exif" function
def walkeddir_parse_stylestrings_out(walkeddir_list):
    import re,os
    ########  Regex only finds _1.jpg files
    regex = re.compile(r'.*?[0-9]{9}_1\.[jpgJPG]{3}$')
    regex_date = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2}')
    stylestrings = []
    stylestringsdict = {}
    for line in walkeddir_list:
        stylestringsdict_tmp = {}
        if re.findall(regex,line):
            try:
                file_path = line
                filename = file_path.split('/')[-1]
                colorstyle = filename.split('_')[0]
                alt_ext = file_path.split('_')[-1]
                alt = alt_ext.split('.')[0]
                ext = alt_ext.split('.')[-1]
                try:
                    path_date = file_path.split('/')[4][:6]
                    path_date = "20{2:.2}-{0:.2}-{1:.2}".format(path_date[:2], path_date[2:4], path_date[4:6])
                    if re.findall(regex_date, path_date):
                        photo_date = path_date
                    else:
                        try:
                            photo_date = get_exif(file_path)['DateTimeOriginal'][:10]
                        except KeyError:
                            try:
                                photo_date = get_exif(file_path)['DateTime'][:10]
                            except KeyError:
                                photo_date = '0000-00-00'
                except AttributeError:
                    photo_date = '0000-00-00'
                photo_date = str(photo_date)
                photo_date = photo_date.replace(':','-')
                stylestringsdict_tmp['colorstyle'] = colorstyle
                stylestringsdict_tmp['photo_date'] = photo_date
                stylestringsdict_tmp['file_path'] = file_path
                stylestringsdict_tmp['alt'] = alt
                stylestringsdict[file_path] = stylestringsdict_tmp
                file_path_reletive = file_path.replace('/mnt/Post_Ready/zImages_1/', '/zImages/')
                file_path_reletive = file_path.replace('JPG', 'jpg')
                ## Format CSV Rows
                row = "{0},{1},{2},{3}".format(colorstyle,photo_date,file_path_reletive,alt)
                #print row
                stylestrings.append(row)
            except IOError:
                print "IOError on {0}".format(line)
                #except AttributeError:
                #    print "AttributeError on {0}".format(line)
    return stylestringsdict

#############################END Funcx Section##########################

######RUN######

## Delete all Events by ID prior to reup
def main():
    prodnumberscal = 'k8oohvl27sq3u0odgafpbmdl6s@group.calendar.google.com'
    service, events_list = getServiceEvents()
    for event in events_list:
        service.events().delete(calendarId=prodnumberscal, eventId=event).execute()
    print "Deleted all Events"
    #calendar_list_entry = service.calendarList().get(calendarId='primary').execute()
    #cals = service.calendarList().get(calendarId='john.bragato@gmail.com').execute()
    #############################Get Data Functions to Query DB###########################
    prodcomplete_dict, retouchcomplete_dict, copycomplete_dict, samples_received_dict = sql_query_production_numbers()
    stillcomplete_dict     = stillcomplete()
    lookletcomplete_dict   = lookletcomplete()
    lotsofdicts = [prodcomplete_dict, retouchcomplete_dict, copycomplete_dict, samples_received_dict, stillcomplete_dict, lookletcomplete_dict]
    ##############################################################################
    for iterdict in lotsofdicts:
        ## first insert data to db then post to gcal
        insert_mysql_numbers(iterdict)
        #
        count = 0
        try:
            for k,v in iterdict.iteritems():
                import datetime, time
                for value in [v]:
                    try:
                        titlekv = str(v['role'])
                    except:
                        titlekv = 'Studio_Shots'
                    try:
                        desckv = str(v['total'])
                        desckv = desckv.replace('&', 'And')
                        desckv = desckv.replace('%', ' Percent')
                        titleid = '{0} - {1}'.format(desckv,titlekv)
                        descfull = '{0} Total for {1} is {2}\n'.format(titlekv, str(k)[:10], desckv)
                        descfull = str(descfull)
                        count += 1
                        lockv = v['role']
                        if lockv == 'Production':
                            colorId = '9'
                        elif lockv == 'Copy':
                            colorId = '8'
                        elif lockv == 'Image_Completion':
                            colorId = '7'
                        elif lockv == 'Looklet':
                            colorId = '6'
                            print descfull
                        elif lockv == 'Still':
                            colorId = '5'
                        elif lockv == 'Samples_Received':
                            colorId = '4'
                        event = {
                          'summary': titleid,
                          'description': descfull,
                          'location': lockv,
                          'colorId': colorId,
                          'start': {
                            'date': "{0:%Y-%m-%d}".format(k.date()),
                            'timeZone': 'America/New_York'
                          },
                          'end': {
                            'date': "{0:%Y-%m-%d}".format(k.date()),
                            'timeZone': 'America/New_York'
                          },
                        }
                        created_event = service.events().insert(calendarId=prodnumberscal, body=event).execute()
                        print created_event['id']
                    except OSError:
                        print 'ERROR {}'.format(event)
                        pass
        except AttributeError:
            pass
        except:
            pass


if __name__ == '__main__':
    main()