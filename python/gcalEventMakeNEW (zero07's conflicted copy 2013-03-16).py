

future_events = sqlQueryEventsIdUpcoming()
future_events_styles = sqlQueryEventsStylesUpcoming()


from collections import defaultdict
eventStyleDict = defaultdict(list)


ddict = defaultdict(list)
for ev in future_events_styles.iteritems():
    evid = ev[0]
    for sty,val in future_events.iteritems():
        styevid = val['event_id']
        if evid == styevid:
            ddict[ev].append(sty)
            

















def sqlQueryEventsIdUpcoming():
    import sqlalchemy
    import collections
    mysql_engine = sqlalchemy.create_engine('mysql://root:root@192.168.21.111:3301/data_imports')
    connection = mysql_engine.connect()
    querymake_eventStyles = "select distinct t1.colorstyle, t1.event_id, t1.production_status from events_style_status t1 join events_snapshot t2 on t1.event_id = t2.event_id where t2.ev_start BETWEEN SYSDATE( ) - INTERVAL 1 DAY AND SYSDATE( ) + INTERVAL 20 DAY"
    
    result = connection.execute(querymake_eventStyles)

    events = collections.defaultdict(list)  
    for row in result:
        event = {}        
        event['colorstyle'] = row['colorstyle']
        event'event_id'] = row['event_id']
        event['production_status'] = row['production_status']        
        #eventStyles[row['event_id']] = eventStyle
        events[row['event_id']].append(row['colorstyle'])
    print events
    connection.close()
    return events
    

def sqlQueryEventsStylesUpcoming():
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
    connection = orcl_engine.connect()
    querymake_eventscal = 'SELECT ATG_SNP.EVENT.ID AS "event_id", ATG_SNP.LK_EVENT_PRODUCT_CATEGORY.NAME AS "category", ATG_SNP.EVENT.EVENT_DESCRIPTION AS "event_title", ATG_SNP.EVENT.START_DATE AS "ev_start", ATG_SNP.EVENT.END_DATE AS "ev_end", ATG_SNP.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID AS "colorstyle", POMGR_SNP.LK_PRODUCT_STATUS.NAME AS "production_status" FROM ATG_SNP.EVENT INNER JOIN ATG_SNP.LK_EVENT_PRODUCT_CATEGORY ON ATG_SNP.EVENT.PRODUCT_CATEGORY_ID = ATG_SNP.LK_EVENT_PRODUCT_CATEGORY.ID RIGHT JOIN ATG_SNP.EVENT_PRODUCT_COLOR ON ATG_SNP.EVENT.ID = ATG_SNP.EVENT_PRODUCT_COLOR.EVENT_ID INNER JOIN ATG_SNP.PRODUCT_COLOR ON ATG_SNP.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID = ATG_SNP.PRODUCT_COLOR.ID INNER JOIN POMGR_SNP.LK_PRODUCT_STATUS ON ATG_SNP.PRODUCT_COLOR.PRODUCTION_STATUS_ID = POMGR_SNP.LK_PRODUCT_STATUS.ID WHERE ATG_SNP.EVENT.START_DATE >= TRUNC(SysDate) ORDER BY ATG_SNP.EVENT.ID DESC, ATG_SNP.EVENT.START_DATE DESC Nulls Last'
    result = connection.execute(querymake_eventscal)
    
    eventStyles = {}
    for row in result:
        eventStyle = {}        
        eventStyle['event_id'] = row['event_id']
        eventStyle['category'] = row['category']                
        eventStyle['event_title'] = row['event_title']
        eventStyle['ev_start'] = row['ev_start']
        eventStyle['ev_end'] = row['ev_end']        
        eventStyle['colorstyle'] = row['colorstyle']        
        eventStyle['production_status'] = row['production_status']  
        eventStyles[row['colorstyle']] = eventStyle
       
    print eventStyles
    connection.close()
    return eventStyles