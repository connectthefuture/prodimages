

future_events_styles = sqlQueryEventsIdUpcoming()
future_events = sqlQueryEventsUpcoming()


from collections import defaultdict
eventStyleDict = defaultdict(list)


ddict = defaultdict(list)
for ev in future_events_styles.iteritems():
    evid = ev[0]
    for sty,val in future_events.iteritems():
        styevid = val['event_id']
        if evid == styevid:
            ddict[ev].append(sty)
            















for key,value in future_events.iteritems():
    import datetime, time    
    for kv in iter(value):
        titlekv = value['event_id']
        desckv = value['event_title']
        lockv = str('bluefly')
        sdatekvraw = '{:%Y,%m,%d,%H,%M,%S,00,00,00}'.format(value['ev_start'])
        edatekvraw = '{:%Y,%m,%d,%H,%M,%S,00,00,00}'.format(value['ev_end'])
        sdatekvsplit = sdatekvraw.split(",")
        edatekvsplit = edatekvraw.split(",")
        sdatekv = map(int,sdatekvsplit)
        edatekv = map(int,edatekvsplit)
        titleid = '{0} {1}'.format(titlekv,desckv)
        ddict = defaultdict(list)
        for ev in future_events.iteritems():
            evid = ev[0]
            for ksty,val in future_events_styles.iteritems():
                styevid = val['event_id']
                style = val['colorstyle']
                if evid == styevid:
                    ddict[styevid].append(style)
        for style1 in ddict.itervalues():
            styles = str(style1)
        from GoogleCalendar import *
        gCalMNG = GoogleCalendarMng()
        myname = "john bragato"
        myemail = "john.bragato@gmail.com"
        gCalMNG.connect (myemail, "yankee17")
        calendar = gCalMNG.getCalendar ("Default1")
        gcalevents = calendar.getEvents()
        events = calendar.getEvents()
        for event in gcalevents:
            print event.getTitle()
            print event.getContent()
            print time.strftime("%Y-%m-%dT%H:%M:%S" ,
                                time.localtime(event.getStartTime()))
            print time.strftime("%Y-%m-%dT%H:%M:%S" ,
                                time.localtime(event.getEndTime()))
        ev = newEvent(myname, myemail, titleid, styles, lockv, time.mktime(sdatekv), time.mktime(edatekv))
        print ev
        calendar.addEvent (ev)