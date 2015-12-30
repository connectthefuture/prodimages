# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 11:23:55 2013

@author: jb
"""
def sqlQueryEventsUpcoming():
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')
    connection = orcl_engine.connect()
    querymake_eventscal = '''SELECT DISTINCT
      POMGR.EVENT.ID                             AS event_id,
      POMGR.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID AS "colorstyle",
      POMGR.LK_EVENT_PRODUCT_CATEGORY.NAME       AS "prod_category",
      POMGR.EVENT.EVENT_DESCRIPTION              AS event_title,
      POMGR.EVENT.START_DATE                     AS ev_start,
      POMGR.EVENT.END_DATE                       AS ev_end,
      POMGR.LK_PRODUCT_STATUS.NAME               AS "production_status",
      POMGR.EVENT.CATEGORY                       AS "categoryid"
    FROM
      POMGR.EVENT_PRODUCT_COLOR
    LEFT JOIN POMGR.PRODUCT_COLOR
    ON
      POMGR.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID = POMGR.PRODUCT_COLOR.PRODUCT_ID
    LEFT JOIN POMGR.LK_PRODUCT_STATUS
    ON
      POMGR.PRODUCT_COLOR.PRODUCTION_STATUS_ID = POMGR.LK_PRODUCT_STATUS.ID
    LEFT JOIN POMGR.EVENT
    ON
      POMGR.EVENT_PRODUCT_COLOR.EVENT_ID = POMGR.EVENT.ID
    LEFT JOIN POMGR.LK_EVENT_PRODUCT_CATEGORY
    ON
      POMGR.EVENT.PRODUCT_CATEGORY_ID = POMGR.LK_EVENT_PRODUCT_CATEGORY.ID
    WHERE
      POMGR.EVENT.START_DATE >= TRUNC(SysDate)
    GROUP BY
      POMGR.EVENT.ID,
      POMGR.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID,
      POMGR.LK_EVENT_PRODUCT_CATEGORY.NAME,
      POMGR.EVENT.EVENT_DESCRIPTION,
      POMGR.EVENT.START_DATE,
      POMGR.EVENT.END_DATE,
      POMGR.LK_PRODUCT_STATUS.NAME,
      POMGR.EVENT.CATEGORY'''
    result = connection.execute(querymake_eventscal)
    
    events = {}
    for row in result:
        event = {}        
        event['event_id'] = row['event_id']
        event['prod_category'] = row['prod_category']                
        event['event_title'] = row['event_title']
        event['category_id'] = row['category_id']
        event['ev_start'] = row['ev_start']
        event['ev_end'] = row['ev_end']        
        event['colorstyle'] = row['colorstyle']        
        event['production_status'] = row['production_status']  
        events[row['colorstyle']] = event
        
    #print events
    connection.close()
    return events

# First retrieve the event from the API.
#event = service.events().get(calendarId='primary', eventId='eventId').execute()

#event['summary'] = 'Appointment at Somewhere'

#updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()

# Print the updated date.
#print updated_event['updated']


future_events = sqlQueryEventsUpcoming()
for key,value in future_events.iteritems():
    for kv in [value]:
        print kv, [value]
#for key,value in future_events.iteritems():
#    import datetime, time    
#    for kv in [value]:
#        titlekv = value['event_id']
#        desckv = value['event_title']
#        colorstyle = value['colorstyle']
#        status = value['production_status']
#        category = value['category']
#                
#        lockv = str(category)
#        sdatekvraw = '{:%Y,%m,%d,%H,%M,%S,00,00,00}'.format(value['ev_start'])
#        edatekvraw = '{:%Y,%m,%d,%H,%M,%S,00,00,00}'.format(value['ev_end'])
#        sdatekvsplit = sdatekvraw.split(",")
#        edatekvsplit = edatekvraw.split(",")
#        sdatekv = map(int,sdatekvsplit)
#        edatekv = map(int,edatekvsplit)
#        titleid = '{0}_{1}'.format(titlekv,desckv)
#        descfull = '{0}_{1}'.format(colorstyle,status)
#        descfull = str(descfull)    
#    try:
#        
#        from GoogleCalendar import *
#        gCalMNG = GoogleCalendarMng()
#        myname = "john bragato"
#        myemail = "john.bragato@gmail.com"
#        gCalMNG.connect (myemail, "yankee17")
#        calendar = gCalMNG.getCalendar ("Default1")
#        gcalevents = calendar.getEvents()
#        print len(gcalevents)
#        
#        for event in gcalevents:
#            print event.getTitle()
#            print event.getContent()
#            print time.strftime("%Y-%m-%dT%H:%M:%S" , time.localtime(event.getStartTime()))
#            print time.strftime("%Y-%m-%dT%H:%M:%S" , time.localtime(event.getEndTime()))
#        ev = newEvent(myname, myemail, titleid, descfull, lockv, time.mktime(sdatekv), time.mktime(edatekv))
#        print ev
#        calendar.addEvent (ev)
#    except xml.parsers.expat.ExpatError:
#        print "FAILED" + key,value
#        continue