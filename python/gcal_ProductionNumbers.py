#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 20:58:41 2013

@author: JCut
"""
#!/usr/bin/env python

def sql_query_production_numbers():
    import sqlalchemy
    from collections import defaultdict
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@192.168.30.165:1531/bfyprd12')
    connection = orcl_engine.connect()
    ### Get Production Complete Totals and Build Dict of key value pairs
    querymake_prodnumbers = '''SELECT COUNT(DISTINCT POMGR.PRODUCT_COLOR.ID) as completion_total, POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT as prod_complete_dt
    FROM POMGR.PRODUCT_COLOR
    WHERE POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT >= TRUNC(SysDate - 1)
    GROUP BY POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT
    ORDER BY POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT DESC'''
    prodcomplete = connection.execute(querymake_prodnumbers)
    prodcomplete_dict = {}
    for row in prodcomplete:
            prodcomplete_dict['prod_complete_dt'] = row['prod_complete_dt']
            prodcomplete_dict['completion_total'] = row['completion_total']
    ### Get Retouching Complete Totals and Build Dict of key value pairs
    querymake_retouchnumbers = '''SELECT COUNT(DISTINCT POMGR.PRODUCT_COLOR.ID) as retouch_total, POMGR.PRODUCT_COLOR.IMAGE_READY_DT as retouch_complete_dt
    FROM POMGR.PRODUCT_COLOR
    WHERE POMGR.PRODUCT_COLOR.IMAGE_READY_DT >= TRUNC(SysDate - 1)
    GROUP BY POMGR.PRODUCT_COLOR.IMAGE_READY_DT
    ORDER BY POMGR.PRODUCT_COLOR.IMAGE_READY_DT DESC'''
    retouchcomplete = connection.execute(querymake_retouchnumbers)
    retouchcomplete_dict = {}
    for row in retouchcomplete:
            retouchcomplete_dict['retouch_complete_dt'] = row['retouch_complete_dt']
            retouchcomplete_dict['retouch_total'] = row['retouch_total']
    ### Get Copy Complete Totals and Build Dict of key value pairs
    querymake_copynumbers = '''SELECT COUNT(DISTINCT POMGR.PRODUCT_COLOR.ID) as copy_total, POMGR.PRODUCT_COLOR.COPY_READY_DT as copy_complete_dt
    FROM POMGR.PRODUCT_COLOR
    WHERE POMGR.PRODUCT_COLOR.COPY_READY_DT >= TRUNC(SysDate - 1)
    GROUP BY POMGR.PRODUCT_COLOR.COPY_READY_DT
    ORDER BY POMGR.PRODUCT_COLOR.COPY_READY_DT DESC'''
    copycomplete = connection.execute(querymake_copynumbers)
    copycomplete_dict = {}
    for row in copycomplete:
            copycomplete_dict['copy_complete_dt'] = row['copy_complete_dt']
            copycomplete_dict['copy_total'] = row['copy_total']
    connection.close()
    return prodcomplete_dict, retouchcomplete_dict, copycomplete_dict

#future_events = sqlQueryEventsUpcoming()
#for key,value in future_events.iteritems():
    #for kv in [value]:

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
    return walkedlist


def gcal_insert_bc_event(titleid, descfull, lockv, sdatekv, edatekv):
    from GoogleCalendar import GoogleCalendarMng, newEvent
    import GoogleCalendar
    try:
        #from GoogleCalendar import *
        gCalMNG = GoogleCalendarMng()
        myname = "john bragato"
        myemail = "john.bragato@gmail.com"
        gCalMNG.connect (myemail, "yankee17")
        calendar = gCalMNG.getCalendar ("Default1")
        gcalevents = calendar.getEvents()
        print len(gcalevents)
        gcaleventslist = []
        for event in gcalevents:
            gcalevent = event.getTitle()
            if gcalevent == titleid:
                continue
            else:
                print event.getContent()
                #print time.strftime("%Y-%m-%dT%H:%M:%S" , time.localtime(event.getStartTime()))
                #print time.strftime("%Y-%m-%dT%H:%M:%S" , time.localtime(event.getEndTime()))
        ev = newEvent(myname, myemail, titleid, descfull, lockv, time.mktime(sdatekv), time.mktime(edatekv))
        print ev
        calendar.addEvent (ev)
    except xml.parsers.expat.ExpatError:
    #except:
        print "FAILED"

##
def gcal_login_jb(myemail='john.bragato@gmail.com', password='yankee17'):
    from GoogleCalendar import GoogleCalendarMng
    import xml
    gCalMNG = GoogleCalendarMng()
    myemail = myemail
    gCalMNG.connect(myemail, password)
    return gCalMNG
##
##
def get_event_data(event):
    eventid = event.getID()
    content = event.getContent()
    title = event.getTitle()
    editing_url = event.getEditURL()
    #print eventid, title, editing_url
    title_4digit = title.strip(r'')
    #title_4digit = bfly_eventnum[:4]
    #if title_4digit.isdigit():
    return editing_url, title_4digit, title, content
##
def if_exists_event(gCalMNG, titleid):
    import xml
    calendar = gCalMNG.getCalendar(calendar_name)
    events = calendar.getEvents()
    for event in events:
        #try:
        if event.getTitle().split(' ')[1] == titleid.split(' ')[1]:
            print type(event.getTitle())
            print event.getTitle().split(' ')[1]
            result = True
            print "True {0}".format(titleid)
            return result
        else:
            print event.getTitle().split(' ')[1]
            result = False
            print "False {0}".format(titleid)
            print titleid.split(' ')[1]
            #print type(result)
            return result
##
def delete_gcalendar_event(titleid, calendar_name='Default1', myemail='john.bragato@gmail.com', password='yankee17'):
    from GoogleCalendar import GoogleCalendarMng
    import xml
    gCalMNG = GoogleCalendarMng()
    myname = myemail.split('@')[0]
    myemail = myemail
    gCalMNG.connect(myemail, password)
    calendar = gCalMNG.getCalendar(calendar_name)
    events = calendar.getEvents()
    for event in events:
        if event.getTitle() == titleid:
            event.delete()
            return "Deleted {0}".format(titleid)


###
#
# First retrieve the event from the API.
#event = service.events().get(calendarId='primary', eventId='eventId').execute()

#event['summary'] = 'Appointment at Somewhere'

#updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()

# Print the updated date.
#print updated_event['updated']


#
prodcomplete_dict, retouchcomplete_dict, copycomplete_dict = sql_query_production_numbers()

print prodcomplete_dict

#count = 0
#for k,v in future_events.iteritems():
#    import datetime, time
#    for value in [v]:
#        titlekv = str(value['event_id'])
#        desckv = str(value['event_title'])
#        desckv = desckv.replace('&', 'And')
#        desckv = desckv.replace('%', ' Percent')
#        colorstyles = future_styles.get(value['event_id'])
#        colorstyles = sorted(colorstyles)
#        still_complete = []
#        fashion_complete = []
#        
#        
#        for colorstyle in colorstyles:
#            if colorstyle[1] == 'Production Complete':
#                complete.append(colorstyle)
#            elif colorstyle[1] == 'Production Incomplete':
#                incomplete.append(colorstyle)
#        incomplete_styles = "{0} Incomplete Styles = {1}".format(len(incomplete),incomplete)
#        complete_styles = "{0} Complete Styles = {1}".format(len(complete),complete)
#        colorstyles_statuses = "{0}\n{1}".format(incomplete_styles,complete_styles)
#
#        count_complete = len(complete)
#        count_incomplete = len(incomplete)
#        count_total = count_complete + count_incomplete
#
#        progress = count_complete/count_total*100
#
#
#        sdatekvraw = '{:%Y,%m,%d,%H,%M,%S,00,00,00}'.format(value['ev_start'])
#        edatekvraw = '{:%Y,%m,%d,%H,%M,%S,00,00,00}'.format(value['ev_end'])
#        sdatekvsplit = sdatekvraw.split(",")
#        edatekvsplit = edatekvraw.split(",")
#        sdatekv = map(int,sdatekvsplit)
#        edatekv = map(int,edatekvsplit)
#        titleid = 'Event {0} -- {1}'.format(titlekv,desckv)
#        descfull = '{0} {1} in Event {2}:\n {3}\n'.format(len(colorstyles), prod_category, titlekv, colorstyles_statuses)
#        descfull = str(descfull)
#        #print titleid, descfull, edatekv, prod_category, lockv
#        count += 1
#        #print count
#
#        try:
#        #gcal_insert_bc_event(titleid, descfull, lockv, sdatekv, edatekv)
#            gCalMNG = gcal_login_jb()
#            #calendar = gCalMNG.getCalendar("Default1")
#            gcalevents = gCalMNG.getCalendar("ProductionNumbers").getEvents()
#            print len(gcalevents)
#            gcaleventslist = []
#            for event in gcalevents:
#                gcalevent = event.getTitle()
#                if gcalevent == titleid:
#                    continue
#                else:
#                    print event.getContent()
#                    #print time.strftime("%Y-%m-%dT%H:%M:%S" , time.localtime(event.getStartTime()))
#                    #print time.strftime("%Y-%m-%dT%H:%M:%S" , time.localtime(event.getEndTime()))
#            ev = newEvent(myname, myemail, titleid, descfull, lockv, time.mktime(sdatekv), time.mktime(edatekv))
#            print ev
#            calendar.addEvent (ev)
#        except xml.parsers.expat.ExpatError:
#        #except:
#            print "FAILED" #+ k,v
#        #    continue