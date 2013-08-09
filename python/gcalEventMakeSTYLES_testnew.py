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


# First retrieve the event from the API.
#event = service.events().get(calendarId='primary', eventId='eventId').execute()

#event['summary'] = 'Appointment at Somewhere'

#updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()

# Print the updated date.
#print updated_event['updated']

#years_dict = dict()
#
#for line in list:
#    if line[0] in years_dict:
#        # append the new number to the existing array at this slot
#        years_dict[line[0]].append(line[1])
#    else:
#        # create a new array in this slot
#        years_dict[line[0]] = [line[1]]

#from collections import defaultdict
#styles = defaultdict(list)
#
future_events, future_styles = sqlQueryEventsUpcoming()
#for key,value in future_styles.iteritems():
#    #for kv in [value]:
#    #d[value['event_id']].append(key)
#    print "Event {0} has {1} Styles".format(key,len(value))

#print d

count = 0
for k,v in future_events.iteritems():
    import datetime, time
    for value in [v]:
        titlekv = str(value['event_id'])
        desckv = str(value['event_title'])
        desckv = desckv.replace('&', 'And')
        desckv = desckv.replace('%', ' Percent')
        colorstyles = future_styles.get(value['event_id'])
        colorstyles = sorted(colorstyles)
        incomplete = []
        complete = []
        for colorstyle in colorstyles:
            if colorstyle[1] == 'Production Complete':
                complete.append(colorstyle)
            elif colorstyle[1] == 'Production Incomplete':
                incomplete.append(colorstyle)
        incomplete_styles = "{0} Incomplete Styles = {1}".format(len(incomplete),incomplete)
        complete_styles = "{0} Complete Styles = {1}".format(len(complete),complete)
        colorstyles_statuses = "{0}\n{1}".format(incomplete_styles,complete_styles)
        count_complete = len(complete)
        count_complete += .00
        count_incomplete = len(incomplete)
        count_incomplete += .00
        count_total = count_complete + count_incomplete
        progress = "{:.0%}".format(count_complete/count_total)
        if len(incomplete) == 0:
            event_complete_flag = True
        else:
            event_complete_flag = False

        status = value['production_status']
        prod_category = str(value['prod_category'])
        category_id = value['category_id']

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
        titleid = 'Event {0} - {2} Complete - {1}'.format(titlekv,desckv,str(progress))
        descfull = '{0} {1} in Event {2}:\n {3}\n'.format(len(colorstyles), prod_category, titlekv, colorstyles_statuses)
        descfull = str(descfull)
        #print titleid, descfull, edatekv, prod_category, lockv
        count += 1
        #print count

        try:
        #gcal_insert_bc_event(titleid, descfull, lockv, sdatekv, edatekv)
            from GoogleCalendar import *
            gCalMNG = GoogleCalendarMng()
            myname = "john bragato"
            myemail = "john.bragato@gmail.com"
            gCalMNG.connect(myemail, "yankee17")
            calendar = gCalMNG.getCalendar("Default1")
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
            #print ev
            calendar.addEvent(ev)
        except xml.parsers.expat.ExpatError:
        #except:
            print "FAILED" #+ k,v
        #    continue
