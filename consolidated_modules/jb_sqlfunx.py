# -*- coding: utf-8 -*-
"""
Created on WED JUL 24 11:23:55 2013

@author: jb
"""
def get_catid_from_eventid(eventid):
    if len(eventid) == 4:
        import sqlalchemy
        orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@192.168.30.165:1531/bfyprd12')
        connection = orcl_engine.connect()
        eventid = str(eventid)
        eventid_tocatid_query = "SELECT DISTINCT POMGR.EVENT.CATEGORY FROM POMGR.EVENT WHERE POMGR.EVENT.ID = '" + eventid + "'"
    #print eventid_tocatid_query
        for row in connection.execute(eventid_tocatid_query):
            catid = row['category']
    else:
        catid = eventid
    if catid:
        return catid
    else:
        print "Event {0} has not been pushed to ATG yet".format(eventid)


def sqlQueryEventsUpcoming():
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@192.168.30.165:1531/bfyprd12')
    connection = orcl_engine.connect()
    querymake_eventscal = 'select distinct POMGR.event.id as "event_id", POMGR.event.start_date as "ev_start", POMGR.event.end_date as "ev_end", POMGR.event.event_description as "event_title" from POMGR.event where POMGR.event.start_date >= trunc(sysdate) order by start_date desc'
    result = connection.execute(querymake_eventscal)
    events = {}
    for row in result:
        event = {}
        event['event_id'] = row['event_id']
        event['ev_start'] = row['ev_start']
        event['ev_end'] = row['ev_end']
        event['event_title'] = row['event_title']
        events[row['event_id']] = event

    print events
    connection.close()
    return events


def sqlQueryEventsStylesUpcoming():
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@192.168.30.165:1531/bfyprd12')
    connection = orcl_engine.connect()
    querymake_eventscal = 'SELECT POMGR.EVENT.ID AS "event_id", POMGR.LK_EVENT_PRODUCT_CATEGORY.NAME AS "category", POMGR.EVENT.EVENT_DESCRIPTION AS "event_title", POMGR.EVENT.START_DATE AS "ev_start", POMGR.EVENT.END_DATE AS "ev_end", POMGR.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID AS "colorstyle", POMGR_SNP.LK_PRODUCT_STATUS.NAME AS "production_status" FROM POMGR.EVENT INNER JOIN POMGR.LK_EVENT_PRODUCT_CATEGORY ON POMGR.EVENT.PRODUCT_CATEGORY_ID = POMGR.LK_EVENT_PRODUCT_CATEGORY.ID RIGHT JOIN POMGR.EVENT_PRODUCT_COLOR ON POMGR.EVENT.ID = POMGR.EVENT_PRODUCT_COLOR.EVENT_ID INNER JOIN POMGR.PRODUCT_COLOR ON POMGR.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID = POMGR.PRODUCT_COLOR.ID INNER JOIN POMGR_SNP.LK_PRODUCT_STATUS ON POMGR.PRODUCT_COLOR.PRODUCTION_STATUS_ID = POMGR_SNP.LK_PRODUCT_STATUS.ID WHERE POMGR.EVENT.START_DATE >= TRUNC(SysDate) ORDER BY POMGR.EVENT.ID DESC, POMGR.EVENT.START_DATE DESC Nulls Last'
    result = connection.execute(querymake_eventscal)

    eventsStyles = {}
    for row in result:
        eventsStyle = {}
        eventsStyle['event_id'] = row['event_id']
        eventsStyle['category'] = row['category']
        eventsStyle['event_title'] = row['event_title']
        eventsStyle['ev_start'] = row['ev_start']
        eventsStyle['ev_end'] = row['ev_end']
        eventsStyle['colorstyle'] = row['colorstyle']
        eventsStyle['production_status'] = row['production_status']
        eventsStyles[row['colorstyle']] = eventsStyle

    print eventsStyles
    connection.close()
    return eventsStyles
