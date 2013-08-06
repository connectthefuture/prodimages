#!/usr/bin/env python

def sqlQueryEventsUpcoming():
    import sqlalchemy
    from collections import defaultdict
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@192.168.30.165:1531/bfyprd12')
    connection = orcl_engine.connect()
    querymake_eventscal = '''SELECT DISTINCT
      POMGR.EVENT.ID                             AS event_id,
      POMGR.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID AS colorstyle,
      POMGR.LK_EVENT_PRODUCT_CATEGORY.NAME       AS prod_category,
      POMGR.EVENT.EVENT_DESCRIPTION              AS event_title,
      POMGR.EVENT.START_DATE                     AS ev_start,
      POMGR.EVENT.END_DATE                       AS ev_end,
      POMGR.LK_PRODUCT_STATUS.NAME               AS production_status,
      POMGR.EVENT.CATEGORY                       AS category_id
    FROM
      POMGR.EVENT_PRODUCT_COLOR
    LEFT JOIN POMGR.EVENT
    ON
      POMGR.EVENT_PRODUCT_COLOR.EVENT_ID = POMGR.EVENT.ID
    INNER JOIN POMGR.LK_EVENT_PRODUCT_CATEGORY
    ON
      POMGR.EVENT.PRODUCT_CATEGORY_ID = POMGR.LK_EVENT_PRODUCT_CATEGORY.ID
    LEFT JOIN POMGR.PRODUCT_COLOR
    ON
      POMGR.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID = POMGR.PRODUCT_COLOR.ID
    LEFT JOIN POMGR.LK_PRODUCT_STATUS
    ON
      POMGR.PRODUCT_COLOR.PRODUCTION_STATUS_ID = POMGR.LK_PRODUCT_STATUS.ID
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
####
    events = {}
    styles = defaultdict(list)
    for row in result:
        event = {}
        event['event_id'] = row['event_id']
        event['prod_category'] = row['prod_category']
        event['event_title'] = row['event_title']
        event['category_id'] = row['category_id']
        event['ev_start'] = row['ev_start']
        event['ev_end'] = row['ev_end']
        event['production_status'] = row['production_status']
        status = str(row['production_status'])
        colorstyle = str(row['colorstyle'])
        stylestatus = (colorstyle,status)
        styles[row['event_id']].append(stylestatus)
        events[row['event_id']] = event
    connection.close()
    return events, styles
##
def if_exists_gcalendar_event(titleid,
                              calendar_name='Default1',
                              myemail='john.bragato@gmail.com',
                              password='yankee17'):
    from GoogleCalendar import GoogleCalendarMng
    import xml
    gCalMNG = GoogleCalendarMng()
    myname = myemail.split('@')[0]
    myemail = myemail
    gCalMNG.connect(myemail, password)
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
def if_exists_event(gCalMNG, event_id):
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
#        if event.getTitle().split(' ')[1] == titleid.split(' ')[1]:
        if event.getTitle() == titleid:
            event.delete()
            return "Deleted {0}".format(titleid)
###
def gcal_insert_bc_event(titleid, descfull, lockv, sdatekv,
                             edatekv, calendar_name='Default1',
                             myemail='john.bragato@gmail.com',
                             password='yankee17'):
    import GoogleCalendar, xml
    from GoogleCalendar import GoogleCalendarMng, newEvent
    try:
        from GoogleCalendar import GoogleCalendarMng
        gCalMNG = GoogleCalendarMng()
        myname = myemail.split('@')[0]
        myemail = myemail
        gCalMNG.connect(myemail, password)
        calendar = gCalMNG.getCalendar(calendar_name)
        events = calendar.getEvents()
        for event in events:
            if event.getTitle() == titleid:
                break
            else:
                event.getContent()
                #print event.getContent()
        ev = newEvent(myname, myemail, titleid, descfull, lockv, time.mktime(sdatekv), time.mktime(edatekv))
        print ev
        calendar.addEvent(ev)
    except xml.parsers.expat.ExpatError:
        print "FAILED {0}".format(titleid)
#
#
def update_gcalendar_event_location(titleid, calendar_name='Default1', current_location='Current Location', updated_location='Updated Location', myemail='john.bragato@gmail.com', password='yankee17'):
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
            event.setContent(event.getContent() + "Changes on location")
            if updated_location:
                event.setLocation(updated_location)
            event.update()
#
#
def update_gcalendar_event_titleid(titleid, calendar_name='Default1', updated_titleid='Updated Event', myemail='john.bragato@gmail.com', password='yankee17'):
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
            event.setTitle(updated_titleid)
            event.update()
#
#
def add_gcalendar_comment(titleid, calendar_name='Default1', comment='No Comments', myemail='john.bragato@gmail.com', password='yankee17'):
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
            event.newComment(comment)
#
#
def update_gcalendar_comment(titleid, calendar_name="Default1", current_comment='No Comments', updated_comment='No Comment Updates', myemail='john.bragato@gmail.com', password='yankee17'):
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
            comments = event.getComments()
        for comment in comments:
            if comment.getContent() == current_comment:
                comment.setContent(updated_comment)
                comment.update()
#
#
def delete_gcalendar_comment(titleid, calendar_name='Default1', current_comment='No Comments', myemail='john.bragato@gmail.com', password='yankee17'):
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
            comments = event.getComments()
            for comment in comments:
                if comment.getContent() == current_comment:
                    comment.delete()
##RUN##
future_events, future_styles = sqlQueryEventsUpcoming()

default_cal = gcal_login_jb().getCalendars()[1]
events = default_cal.getEvents()
try:
    for event in events:
        delete_gcalendar_event(event)
except:
    print "Nothing to Delete"

count = 0
gcal_inserts = []
for k,v in future_events.iteritems():
    import datetime, time, xml
    from collections import defaultdict
    for value in [v]:
        titlekv = str(value['event_id'])
        desckv = str(value['event_title'])
        desckv = desckv.replace('&', 'And')
        desckv = desckv.replace('%', ' Percent')
        colorstyles = future_styles.get(value['event_id'])
        colorstyles.sort
        incomplete = []
        complete = []
        for colorstyle in colorstyles:
                if colorstyle[1] == 'Production Complete':
                        complete.append(colorstyle)
                        complete.sort
                elif colorstyle[1] == 'Production Incomplete':
                        incomplete.append(colorstyle)
                        incomplete.sort
        incomplete_styles = "{0} Incomplete Styles --> {1}".format(len(incomplete),incomplete)
        complete_styles = "{0} Complete Styles --> {1}".format(len(complete),complete)
        colorstyles_statuses = "{0}\n{1}".format(incomplete_styles,complete_styles)
        if len(incomplete) == 0:
            event_complete_flag = True
        else:
            event_complete_flag = False
        status = value['production_status']
        prod_category = str(value['prod_category'])
        category_id = str(value['category_id'])
        pmurl = "http://pm.bluefly.corp/manager/event/editevent.html?id="
        pmimgs = "http://pm.bluefly.corp/manager/event/viewproductimages.html?id="
        bcurl = "http://www.belleandclive.com/browse/sales/details.jsp?categoryId="
        pmurl = pmurl + titlekv
        pmimgs = pmimgs + titlekv
        bcurl = pmurl + titlekv
        try:
            if colorstyles == None:
                lockv = str(pmurl)
            else:
                lockv = str(pmimgs)
        except TypeError:
            lockv = str(bcurl)
        sdatekvraw = '{:%Y,%m,%d,%H,%M,%S,00,00,00}'.format(value['ev_start'])
        edatekvraw = '{:%Y,%m,%d,%H,%M,%S,00,00,00}'.format(value['ev_end'])
        sdatekvsplit = sdatekvraw.split(",")
        edatekvsplit = edatekvraw.split(",")
        sdatekv = map(int,sdatekvsplit)
        edatekv = map(int,edatekvsplit)
        titleid = 'Event {0} -- {1}'.format(titlekv,desckv)
        descfull = '{0} {1} in Event {2}:\n{3}\n'.format(len(colorstyles), prod_category, titlekv, incomplete_styles)
        descfull = str(descfull)
        titleid = str(titleid)
        try:
            default_cal = gcal_login_jb().getCalendars()[1]
            events = default_cal.getEvents()
            inserts_dict = defaultdict(list)
            event_data_dict = defaultdict(list)
            for event in events:
                editing_url, title_4digit, title, content = get_event_data(event)
                event_data = (editing_url, title_4digit, title, content,)
                event_data_dict[title].append(event_data)
                inserts = (titleid, descfull, lockv, sdatekv, edatekv,)
                inserts_dict[title].append(inserts)
                count += 1
				#print count
			#print data_inserts_dict
            for k,v in event_data_dict.iteritems():
                match = inserts_dict.get(k)
                print "Successful Match {0},{1}".format(k,match)
                try:
                    delete_gcalendar_event(k)
                    print "Deleted {0}".format(k)
                except:
                    print "Failed Deletion {0}".format(k)
#print "Failed {0},{1}".format(k,val[1][0])
        except AttributeError:
            pass

for k,[v] in inserts_dict.iteritems():
    try:
        titleid = k
        descfull = [v][1]
        lockv = [v][2]
        sdatekv = [v][3]
        edatekv = [v][4]
        print titleid, descfull, lockv, sdatekv, edatekv
        gcal_insert_bc_event(titleid, descfull, lockv, sdatekv, edatekv, calendar_name='Default1', myemail='john.bragato@gmail.com', password='yankee17')
    except:
        print "Failed {}{}{}{}{}".format(titleid, descfull, lockv, sdatekv, edatekv)
##
##

#        while if_exists_gcalendar_event(titleid, calendar_name='Default1') == True:
##            try:
#            print "Deleting {0}".format(titleid)
#            delete_gcalendar_event(titleid, calendar_name='Default1',
#                                   myemail='john.bragato@gmail.com',
#                                   password='yankee17')
##            except:
##                pass
#        gcal_insert_bc_event(titleid, descfull, lockv, sdatekv,
#                             edatekv, calendar_name='Default1',
#                             myemail='john.bragato@gmail.com',
#                             password='yankee17')
