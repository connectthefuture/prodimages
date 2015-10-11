#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gflags
import httplib2
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run
import os, datetime

##########################Vars
client_id='924881045523-kc7leju7role0too3k4itlo864eprl1u.apps.googleusercontent.com'
client_secret='rqZxYuy0Cht37rJ0GSZ05YoY'
user_agent='Python2.7'
BROWSERdeveloperKey='AIzaSyBHozNPRDnVkdPo_JlP_4TLbNrJIsd3bQ4'
SERVERdeveloperKey='AIzaSyDe68JsIJK5O5Cqd-tAVGqaSeHqcFCNPh8'



batchRunScripts = os.path.join('/usr/local', 'batchRunScripts')
os.chdir(batchRunScripts)

#here = os.path.dirname(os.path.realpath(os.path.curdir))
storage_file = os.path.join(batchRunScripts, 'calendar.dat')

############################
FLAGS = gflags.FLAGS

# The client_id and client_secret are copied from the API Access tab on
# the Google APIs Console
FLOW = OAuth2WebServerFlow(
    client_id=client_id,
    client_secret=client_secret,
    scope='https://www.googleapis.com/auth/calendar',
    user_agent=user_agent)

# To disable the local server feature, uncomment the following line:
FLAGS.auth_local_webserver = False

# If the Credentials don't exist or are invalid, run through the native client
# flow. The Storage object will ensure that if successful the good
# Credentials will get written back to a file.
storage = Storage(storage_file)
credentials = storage.get()
if credentials is None or credentials.invalid == True:
    credentials = run(FLOW, storage)

# Create an httplib2.Http object to handle our HTTP requests and authorize it
# with our good Credentials.
http = httplib2.Http()
http = credentials.authorize(http)

prodcompletebysourcecal = 'pbr49v778pi6n9cqark5rd1dns@group.calendar.google.com'
marketplvendorscmpcal = 'qfr9hv1frv22ovnk5hoptsqj38@group.calendar.google.com'

calendarId = prodcompletebysourcecal
#calendarId = 'https://www.google.com/calendar/feeds/k8oohvl27sq3u0odgafpbmdl6s@group.calendar.google.com/'
# calendarId = 'https://www.google.com/calendar/feeds/k8oohvl27sq3u0odgafpbmdl6s@group.calendar.google.com/private-cfbcfde94d17e48fbf1f824a8536e0ba/basic'

# Build a service object for interacting with the API.
service = build(serviceName='calendar', version='v3', http=http)

# Getting All Event Ids
page_token = None
events_list = []
try:    
    while True:
        events = service.events().list(calendarId=calendarId, pageToken=page_token).execute()
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
        events = service.events().list(calendarId=calendarId, pageToken=page_token).execute()
        for event in events['items']:
            event_id = event['id']
            events_list.append(event_id)
            #print event_id
        page_token = events.get('nextPageToken')
        if not page_token:
            break

###########################
####  END AUTH SECTION
###########################
#############################Get Data to send to API###########################
#from python.gcal_functions import stillcomplete, fashioncomplete, sql_query_production_numbers

def sql_query_production_numbers():
    import sqlalchemy
    import datetime
    from collections import defaultdict
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')
    connection = orcl_engine.connect()

    ### Get Production Complete Totals and Build Dict of key value pairs
    complete_by_vendor = """SELECT POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID as "vendor_name",
                                    COUNT(DISTINCT POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID) AS "style_count",
                                    TO_CHAR(POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT, 'YYYY-MM-DD') as "production_complete_dt"
                                    FROM POMGR.SUPPLIER_INGEST_STYLE
                                    RIGHT JOIN POMGR.SUPPLIER_INGEST_SKU
                                    ON POMGR.SUPPLIER_INGEST_SKU.STYLE_ID = POMGR.SUPPLIER_INGEST_STYLE.ID
                                    LEFT JOIN POMGR.SUPPLIER_INGEST_IMAGE
                                    ON POMGR.SUPPLIER_INGEST_STYLE.ID = POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID
                                    RIGHT JOIN POMGR.PRODUCT_COLOR
                                    ON POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR = POMGR.PRODUCT_COLOR.ID
                                    WHERE POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID LIKE '%%'
                                    AND POMGR.SUPPLIER_INGEST_IMAGE.URL            IS NOT NULL
                                    AND TO_CHAR(POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT, 'YYYY-MM-DD') IS NOT NULL
                                    GROUP BY POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID,
                                      TO_CHAR(POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT, 'YYYY-MM-DD')
                                    ORDER BY 3 DESC"""
    prodcomplete = connection.execute(complete_by_vendor)
    marketpl_prodcomplete_dict = {}
    for row in prodcomplete:
        tmp_dict = {}
        tmp_dict['total'] = row['style_count']
        tmp_dict['vendor_name'] = row['vendor_name']
        marketpl_prodcomplete_dict[row['production_complete_dt']] = tmp_dict

    
    ### Get Complete by inventory Source Totals and Build Dict of key value pairs
    querymake_complete_by_source ='''SELECT "DateComplete", "TotalCompletions", "Asset-Total", "Asset-Apparel", "Asset-Non-Appr", "FullFill-Bluefly", "FF-Vendor-Dropship", "Marketplace" FROM(
    with data as (  
        select   
        max(distinct POMGR.SKU.PRODUCT_COLOR_ID) as "DATA_COLORSTYLE",   
        max(distinct POMGR.SKU.sku_code) as "DATA_SKU_CODE"   
      FROM POMGR.SKU  
      LEFT JOIN POMGR.PRODUCT_COLOR  
        ON POMGR.SKU.PRODUCT_COLOR_ID = POMGR.PRODUCT_COLOR.ID  
      group by POMGR.SKU.PRODUCT_COLOR_ID  
      order by POMGR.SKU.PRODUCT_COLOR_ID desc  
    )  
     
    SELECT  
      TO_CHAR(POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT, 'YYYY-MM-DD') AS "DateComplete",  
      COUNT(distinct POMGR.PRODUCT_COLOR.ID) AS "TotalCompletions",   
       SUM(  
        CASE  
          WHEN ( data.DATA_SKU_CODE LIKE '8%' 
          )  
          THEN 1  
          ELSE 0  
        END) "Asset-Total",  
        SUM(  
        CASE  
          WHEN ( data.DATA_SKU_CODE LIKE '8%' and POMGR.PRODUCT_FOLDER_DENORMALIZED.PATH LIKE '%/%men/apparel/%'  
          )  
          THEN 1  
          ELSE 0  
        END) "Asset-Apparel",  
      SUM(  
        CASE  
          WHEN (SUBSTR(data.DATA_SKU_CODE, 1,1) = '8' and POMGR.PRODUCT_FOLDER_DENORMALIZED.PATH LIKE '%/non apparel/%'  
          )  
          THEN 1  
          ELSE 0  
        END) "Asset-Non-Appr",  
      SUM(  
        CASE  
          WHEN data.DATA_SKU_CODE LIKE '101%'  
          THEN 1  
          ELSE 0  
        END) "FullFill-Bluefly",  
      SUM(  
        CASE  
          WHEN data.DATA_SKU_CODE LIKE '102%'  
          THEN 1  
          ELSE 0  
        END) "FF-Vendor-Dropship",  
      SUM(  
        CASE  
          WHEN data.DATA_SKU_CODE LIKE '103%'  
          THEN 1  
          ELSE 0  
        END) "Marketplace"  
    FROM  
      POMGR.PRODUCT_COLOR  
    LEFT JOIN POMGR.PRODUCT  
    ON  
      POMGR.PRODUCT_COLOR.PRODUCT_ID = POMGR.PRODUCT.ID  
    LEFT JOIN POMGR.PRODUCT_FOLDER  
    ON  
      POMGR.PRODUCT.PRODUCT_FOLDER_ID = POMGR.PRODUCT_FOLDER.ID  
    LEFT JOIN POMGR.PRODUCT_FOLDER_DENORMALIZED  
    ON  
      POMGR.PRODUCT_FOLDER.ID = POMGR.PRODUCT_FOLDER_DENORMALIZED.ID  
    LEFT JOIN data 
    ON  
      data.DATA_COLORSTYLE = POMGR.PRODUCT_COLOR.ID  
    WHERE  
    TO_CHAR(POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT, 'YYYY') = '2014' 
    GROUP BY  
    TO_CHAR(POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT, 'YYYY-MM-DD'), 
    TO_CHAR(POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT, 'YYYY') 
    ORDER BY 
    "DateComplete" DESC,  
    TO_CHAR(POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT, 'YYYY') DESC
    )'''
    complete_by_source = connection.execute(querymake_complete_by_source)
    complete_by_source_dict = {}
    for row in complete_by_source:
        tmp_dict = {}
        tmp_dict['total']       = row['TotalCompletions']
        tmp_dict['total_asset'] = row['Asset-Total']
        tmp_dict['total_ff']    = row['FullFill-Bluefly']
        tmp_dict['total_swids'] = row['FF-Vendor-Dropship']
        tmp_dict['total_mpl']   = row['Marketplace']
        complete_by_source_dict[row['DateComplete']] = tmp_dict

    

    
    connection.close()
    return complete_by_source_dict

#############################END Funcx Section##########################

######RUN######


## Delete all Events by ID prior to reup
for event in events_list:
    service.events().delete(calendarId=calendarId, eventId=event).execute()
    
print "Deleted all Events"    
#calendar_list_entry = service.calendarList().get(calendarId='primary').execute()
#cals = service.calendarList().get(calendarId='john.bragato@gmail.com').execute()

#############################Get Data Functions to Query DB###########################

complete_by_source_dict = sql_query_production_numbers()

##########################################     = stillcomplete   = fashioncomplete()

lotsofdicts = [complete_by_source_dict]
##############################################################################

for iterdict in lotsofdicts:
    count = 0
    for k,value in iterdict.iteritems():
        import datetime, time
        #for value in [v]:
            
        try:
            total       = value['total']
            total_asset = value['total_asset']
            total_ff    = value['total_ff']
            total_swids = value['total_swids']
            total_mpl   = value['total_mpl']
            colorId = '8'
            calendarId = prodcompletebysourcecal
            summary = "Total: {0}".format(total)
            description = """
            Total: {0}
            \tAssets: {1}
            \tFullfill: {2}
            \tSWI: {3}
            \tMarketplace: {4}
            """.format(total,total_asset,total_ff,total_swids,total_mpl)
            location = 'Home'
        except KeyError:
            value['vendor_name']
            total       = value['total']
            vendor_name = value['vendor_name']
            colorId = '8'
            calendarId = marketplvendorscmpcal
            description = """Vendor: {0}\n\tTotalComplete: {1}""".format(vendor_name,total)
            location = 'Home'
            summary = description #"Vendor: {0}".format(vendor_name)

        if type(k) == str:
            k = datetime.datetime.strptime(k,'%Y-%d-%M')
        try:

            event = {
              'summary': summary,
              'description': description,
              'location': location,
              'colorId': colorId,
              'start': {
                'date': "{0:%Y-%m-%d}".format(k.date()),
                'timeZone': 'America/New_York'
              },
              'end': {
                'date': "{0:%Y-%m-%d}".format(k.date()),
                'timeZone': 'America/New_York'
              },
            #  'recurrence': [
            #    'RRULE:FREQ=WEEKLY;UNTIL=20110701T100000-07:00',
            #  ],
#                  'attendees': [
#                    {
#                      'email': 'james.hoetker@bluefly.com',
#                      # Other attendee's data...
#                    },
#                    # ...
#                  ],
            }
            print event
            created_event = service.events().insert(calendarId=calendarId, body=event).execute()
            print created_event['id']
        except OSError:
            print 'ERROR {}'.format(event)
            pass
                