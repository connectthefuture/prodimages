#!/usr/bin/env python
import os,re,sys
import pyinotify
from pyinotify import WatchManager, Notifier, ThreadedNotifier, EventsCodes, ProcessEvent

class MyEventHandler(ProcessEvent):
    from pyinotify import WatchManager, Notifier, ThreadedNotifier, EventsCodes, ProcessEvent
    def __init__(self, **kargs):
        #self.watchdir = self.watchdir
        self.eventfunc = {}
        self.mask = pyinotify.IN_CREATE | pyinotify.IN_MODIFY | pyinotify.IN_DELETE
    def process_IN_ACCESS(self, event):        
        print "ACCESS event:", event.pathname
    def process_IN_ATTRIB(self, event):
        print "ATTRIB event:", event.pathname
    def process_IN_CLOSE_NOWRITE(self, event):
        print "CLOSE_NOWRITE event:", event.pathname
    def process_IN_CLOSE_WRITE(self, event):
        print "CLOSE_WRITE event:", event.pathname
    def process_IN_CREATE(self, event):
        pathtoevent = os.path.join(event.path, event.name)	
        if os.path.isdir(pathtoevent):
            diradded = os.path.join(event.path, event.name)
            print "CREATED DIRECTORY:", diradded
        if os.path.isfile(pathtoevent):
            fileadded = os.path.join(event.path, event.name)
            print "CREATED FILE:", fileadded
        print "CREATE event:", event.pathname
    def process_IN_DELETE(self, event):
        print "DELETE event:", event.pathname    	
        pathtoevent = os.path.join(event.path, event.name)
        if os.path.isdir(pathtoevent):
            dirdeleted = os.path.join(event.path, event.name)
            print "DELETED DIRECTORY:", dirdeleted
        if os.path.isfile(pathtoevent):
            filedeleted = os.path.join(event.path, event.name)
            print "DELETED FILE:", filedeleted
    def process_IN_MODIFY(self, event):
        pathtoevent = os.path.join(event.path, event.name)
        if os.path.isdir(pathtoevent):
            dirmodified = os.path.join(event.path, event.name)
            print "MODIFIED DIRECTORY:", dirmodified	
        if os.path.isfile(pathtoevent):
            filemodified = os.path.join(event.path, event.name)
            print "MODIFIED FILE:", filemodified
    def process_IN_OPEN(self, event):
        pathtoevent = os.path.join(event.path, event.name)
        print "OPEN event:", event.pathname
        fileopened = os.path.join(event.path, event.name)
        if os.path.isdir(pathtoevent):
            dirmodified = os.path.join(event.path, event.name)
        if os.path.isfile(pathtoevent):
            file = os.path.join(event.path, event.name)




def main(watchdir):
    eh = MyEventHandler()
    wm = myeventhandler.WatchManager()
    wm.add_watch(watchdir,pyinotify.ALL_EVENTS, rec=True, auto_add=True)
    notifier = pyinotify.Notifier(wm, eh)
    notifier.loop()
    
#    def main(self):
#        # watch manager
#        wm = WatchManager()
#        wm.add_watch(self.watchdir, pyinotify.ALL_EVENTS, rec=True, auto_add=True)
        #wm.add_watch('/home/johnb/mnt/Post_Ready/aPhotoPush', pyinotify.ALL_EVENTS, rec=True, auto_add=True)
        # event handler
#        eh = MyEventHandler()
        # notifier
#        notifier = pyinotify.Notifier(wm, eh)
#        notifier.loop()
if __name__ == '__main__':
    main()
