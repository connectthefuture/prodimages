# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 14:35:36 2013

@author: jb
"""

#! /usr/bin/env python

import gdata.calendar.service
import getpass
def print_event_feed(event_feed):
    for index, event in enumerate(event_feed.entry):
        print "\t%d) %s\r\n\tContent: %s" % (
                index, event.title.text, event.content.text)
        print "\t\tWho:"
        for person in event.who:
            print "\t\t\tName: %s\n\t\t\temail: %s" % (person.name
                , person.email)
        print "\t\tAuthors:"
        for author in event.author:
            print "\t\t\t%s" % (author.name.text)
        print "\t\tWhen:"
        for e_index, e_time in enumerate(event.when):
            print "\t\t\t%d) Start time: %s\n\t\t\tEnd time: %s" % (
                e_index
                , e_time.start_time
                , e_time.end_time)

def list_own_calendars(calendar_service):
    try:
        #Get the CalendarListFeed
        all_calendars_feed = calendar_service.GetOwnCalendarsFeed()
    except Exception, e:
        print "Error getting all calendar feed: %s" % (e)
        return
    #Print the feed's title
    print all_calendars_feed.title.text
    #Now loop through all of the CalendarListEntry items.
    for (index, cal) in enumerate(all_calendars_feed.entry):
        #Print out the title and the summary if there is one
        if (cal.summary is not None):
            print "%d) %s - Summary: %s" % (
                index, cal.title.text, cal.summary.text)
        else:
            print "%d) %s" % (index, cal.title.text)
        #Print out the authors
        print "\tAuthors:"
        for author in cal.author:
            print "\t\t%s" % (author.name.text)
        #Print out other information
        print "\tPublished: %s \n\tUpdated: %s \n\ttimezone: %s" % (
            cal.published.text, cal.updated.text, cal.timezone.value)
        print "\tColour: %s \n\tHidden: %s \n\tSelected: %s" % (
            cal.color.value, cal.hidden.value, cal.selected.value)
        print "\tAccess Level: %s" % (cal.access_level.value)
        # Now Print out the events
        print "\tEvents:"
        a_link = cal.GetAlternateLink()
        if (a_link is not None):
            event_feed = calendar_service.GetCalendarEventFeed(a_link.href)
            print_event_feed(event_feed)




## Function Auth and Login With Exception Handlers
def main():
    import getpass    
    username = raw_input("Enter your username: ")
    
    password = raw_input("Enter your password: ")
    #getpass.getpass("Enter your password: ")
    calendar_service = gdata.calendar.service.CalendarService(username, password, "Default")
    try:
        calendar_service.ProgrammaticLogin()
    except gdata.service.BadAuthentication, e:
        print "Authentication error logging in: %s" % e
        return
    except Exception, e:
        print "Error Logging in: %s" % e
        return
    list_own_calendars(calendar_service)

if __name__ == "__main__":
    main()