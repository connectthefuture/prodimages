# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 11:23:55 2013

@author: jb
"""
def sqlQueryEventsUpcoming():
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
    connection = orcl_engine.connect()
    querymake_eventscal = 'SELECT ATG_SNP.EVENT.ID AS "event_id", ATG_SNP.LK_EVENT_PRODUCT_CATEGORY.NAME AS "category", ATG_SNP.EVENT.EVENT_DESCRIPTION AS "event_title", ATG_SNP.EVENT.START_DATE AS "ev_start", ATG_SNP.EVENT.END_DATE AS "ev_end", ATG_SNP.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID AS "colorstyle", POMGR_SNP.LK_PRODUCT_STATUS.NAME AS "production_status" FROM ATG_SNP.EVENT INNER JOIN ATG_SNP.LK_EVENT_PRODUCT_CATEGORY ON ATG_SNP.EVENT.PRODUCT_CATEGORY_ID = ATG_SNP.LK_EVENT_PRODUCT_CATEGORY.ID RIGHT JOIN ATG_SNP.EVENT_PRODUCT_COLOR ON ATG_SNP.EVENT.ID = ATG_SNP.EVENT_PRODUCT_COLOR.EVENT_ID INNER JOIN ATG_SNP.PRODUCT_COLOR ON ATG_SNP.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID = ATG_SNP.PRODUCT_COLOR.ID INNER JOIN POMGR_SNP.LK_PRODUCT_STATUS ON ATG_SNP.PRODUCT_COLOR.PRODUCTION_STATUS_ID = POMGR_SNP.LK_PRODUCT_STATUS.ID WHERE ATG_SNP.EVENT.START_DATE >= TRUNC(SysDate) ORDER BY ATG_SNP.EVENT.ID DESC, ATG_SNP.EVENT.START_DATE DESC Nulls Last'
    result = connection.execute(querymake_eventscal)
    
    events = {}
    for row in result:
        event = {}        
        event['event_id'] = row['event_id']
        event['category'] = row['category']                
        event['event_title'] = row['event_title']
        event['ev_start'] = row['ev_start']
        event['ev_end'] = row['ev_end']        
        event['colorstyle'] = row['colorstyle']        
        event['production_status'] = row['production_status']  
        events[row['colorstyle']] = event
       
    print events
    connection.close()
    return events

# First retrieve the event from the API.
'''
event = service.events().get(calendarId='primary', eventId='eventId').execute()

event['summary'] = 'Appointment at Somewhere'

updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()

# Print the updated date.
print updated_event['updated']
'''

future_events = sqlQueryEventsUpcoming()

for key,value in future_events.iteritems():
    import datetime, time    
    for kv in iter(value):
        titlekv = value['event_id']
        desckv = value['event_title']
        colorstyle = value['colorstyle']
        status = value['production_status']
        category = value['category']
        lockv = str(category)
        sdatekvraw = '{:%Y,%m,%d,%H,%M,%S,00,00,00}'.format(value['ev_start'])
        edatekvraw = '{:%Y,%m,%d,%H,%M,%S,00,00,00}'.format(value['ev_end'])
        sdatekvsplit = sdatekvraw.split(",")
        edatekvsplit = edatekvraw.split(",")
        sdatekv = map(int,sdatekvsplit)
        edatekv = map(int,edatekvsplit)
        titleid = '{0}_{1}'.format(titlekv,desckv)
        descfull = '{0}_{1}'.format(colorstyle,status)
        descfull = str(descfull)    
        try:
            from GoogleCalendar import *
            gCalMNG = GoogleCalendarMng()
            myname = "john bragato"
            myemail = "john.bragato@gmail.com"
            gCalMNG.connect (myemail, "yankee17")
            calendar = gCalMNG.getCalendar ("Default1")
            gcalevents = calendar.getEvents()
            for event in gcalevents:
                if event.getTitle() == titleid:
                    event.setContent (event.getContent() + "Changes on location")
                    event.setLocation (lockv)
                    event.update()
                    contents = event.getContent()
                    for content in contents:
                        if content.getContent() == descfull:
                            content.setContent(descfull)
                            content.update()
                else:
                    for event in gcalevents:
                        print event.getTitle()
                        print event.getContent()
                        print time.strftime("%Y-%m-%dT%H:%M:%S" , time.localtime(event.getStartTime()))
                        print time.strftime("%Y-%m-%dT%H:%M:%S" , time.localtime(event.getEndTime()))
                    ev = newEvent(myname, myemail, titleid, descfull, lockv, time.mktime(sdatekv), time.mktime(edatekv))
                    print ev
                    calendar.addEvent (ev)
                        
            
            
        except xml.parsers.expat.ExpatError:
            print "FAILED" + key,value
            continue