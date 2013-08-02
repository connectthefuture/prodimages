def sqlQueryEventsUpcoming():
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
    connection = orcl_engine.connect()
    querymake_eventscal = 'select distinct atg_snp.event.id as "event_id", atg_snp.event.start_date as "ev_start", atg_snp.event.end_date as "ev_end", atg_snp.event.event_description as "event_title" from atg_snp.event where atg_snp.event.start_date >= trunc(sysdate) order by start_date desc'
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
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
    connection = orcl_engine.connect()
    querymake_eventscal = 'SELECT ATG_SNP.EVENT.ID AS "event_id", ATG_SNP.LK_EVENT_PRODUCT_CATEGORY.NAME AS "category", ATG_SNP.EVENT.EVENT_DESCRIPTION AS "event_title", ATG_SNP.EVENT.START_DATE AS "ev_start", ATG_SNP.EVENT.END_DATE AS "ev_end", ATG_SNP.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID AS "colorstyle", POMGR_SNP.LK_PRODUCT_STATUS.NAME AS "production_status" FROM ATG_SNP.EVENT INNER JOIN ATG_SNP.LK_EVENT_PRODUCT_CATEGORY ON ATG_SNP.EVENT.PRODUCT_CATEGORY_ID = ATG_SNP.LK_EVENT_PRODUCT_CATEGORY.ID RIGHT JOIN ATG_SNP.EVENT_PRODUCT_COLOR ON ATG_SNP.EVENT.ID = ATG_SNP.EVENT_PRODUCT_COLOR.EVENT_ID INNER JOIN ATG_SNP.PRODUCT_COLOR ON ATG_SNP.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID = ATG_SNP.PRODUCT_COLOR.ID INNER JOIN POMGR_SNP.LK_PRODUCT_STATUS ON ATG_SNP.PRODUCT_COLOR.PRODUCTION_STATUS_ID = POMGR_SNP.LK_PRODUCT_STATUS.ID WHERE ATG_SNP.EVENT.START_DATE >= TRUNC(SysDate) ORDER BY ATG_SNP.EVENT.ID DESC, ATG_SNP.EVENT.START_DATE DESC Nulls Last'
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

    
future_events_styles = sqlQueryEventsStylesUpcoming()
future_events = sqlQueryEventsUpcoming()



"""
SELECT
  ATG_SNP.EVENT.ID                             AS "event_id",
  ATG_SNP.LK_EVENT_PRODUCT_CATEGORY.NAME       AS "category",
  ATG_SNP.EVENT.EVENT_DESCRIPTION              AS "event_title",
  ATG_SNP.EVENT.START_DATE                     AS "ev_start",
  ATG_SNP.EVENT.END_DATE                       AS "ev_end",
  ATG_SNP.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID AS "colorstyle",
  POMGR_SNP.LK_PRODUCT_STATUS.NAME             AS "production_status"
FROM
  ATG_SNP.EVENT
INNER JOIN ATG_SNP.LK_EVENT_PRODUCT_CATEGORY
ON
  ATG_SNP.EVENT.PRODUCT_CATEGORY_ID = ATG_SNP.LK_EVENT_PRODUCT_CATEGORY.ID
RIGHT JOIN ATG_SNP.EVENT_PRODUCT_COLOR
ON
  ATG_SNP.EVENT.ID = ATG_SNP.EVENT_PRODUCT_COLOR.EVENT_ID
INNER JOIN ATG_SNP.PRODUCT_COLOR
ON
  ATG_SNP.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID = ATG_SNP.PRODUCT_COLOR.ID
INNER JOIN POMGR_SNP.LK_PRODUCT_STATUS
ON
  ATG_SNP.PRODUCT_COLOR.PRODUCTION_STATUS_ID = POMGR_SNP.LK_PRODUCT_STATUS.ID
WHERE
  ATG_SNP.EVENT.START_DATE >= TRUNC(SysDate)
ORDER BY
  ATG_SNP.EVENT.ID DESC,
  ATG_SNP.EVENT.START_DATE DESC Nulls Last


def merge_dicts(*dicts): 
    return dict(chain(*[d.iteritems() for d in dicts])) 

newdict = merge_dicts(future_event_styles,future_events)

newdict = dict([(k, [future_events['event_id'], future_event_styles['event_id']]) for 'event_id' in future_events])

newdict = dict(future_events.items() + future_event_styles.items())

d1 = future_events
d2 = future_event_styles
newdict = dict(((k, (d1[k], d2[k])) for k in d1))
dicts = d1,d2

newdictprint = {k:[d.get(k) for d in dicts] for k in {k for d in dicts for k in d}}


for ev in future_events1.iteritems():
    evid = ev[0]
    for sty,val in future_events.iteritems():
        styevid = val['event_id']
        if evid == styevid:
            print ev, sty




"""





for key,value in future_events.iteritems():
    import datetime, time    
    for kv in iter(value):
        titlekv = value['ID']
        desckv = value['EVENT_DESCRIPTION']
        lockv = str('bluefly')
        sdatekvraw = '{:%Y,%m,%d,%H,%M,%S,00,00,00}'.format(value['START_DATE'])
        edatekvraw = '{:%Y,%m,%d,%H,%M,%S,00,00,00}'.format(value['END_DATE'])
        sdatekvsplit = sdatekvraw.split(",")
        edatekvsplit = edatekvraw.split(",")
        sdatekv = map(int,sdatekvsplit)
        edatekv = map(int,edatekvsplit)
        titleid = '{0}_{1}'.format(titlekv,desckv)
        
        
    from GoogleCalendar import *
    gCalMNG = GoogleCalendarMng()
    myname = "john bragato"
    myemail = "john.bragato@gmail.com"
    gCalMNG.connect (myemail, "yankee17")
    calendar = gCalMNG.getCalendar ("Default")
    gcalevents = calendar.getEvents()
    events = calendar.getEvents()
    for event in events:
        if event.getTitle() == titleid:
            event.setContent (event.getContent() + "Changes on location")
            event.setLocation ("Barcelona")
            event.update()
            
        
    
    for event in gcalevents:
        print event.getTitle()
        print event.getContent()
        print time.strftime("%Y-%m-%dT%H:%M:%S" ,
                            time.localtime(event.getStartTime()))
        print time.strftime("%Y-%m-%dT%H:%M:%S" ,
                            time.localtime(event.getEndTime()))
    ev = newEvent(myname, myemail, titleid, titlekv, lockv, time.mktime(sdatekv), time.mktime(edatekv))
    print ev
    calendar.addEvent (ev)


