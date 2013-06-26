#!/usr/bin/env python

# #To familiarize yourself with pyinotify, run a first example like this:
#
# # $ cd pyinotify-x-x-x && python setup.py build
# # $ python src/pyinotify/pyinotify.py -v my-dir-to-watch
#
# # Let's start a more detailed example. Say, we want to monitor the temp directory '/tmp' and all its subdirectories for every new file's creation or deletion. For sake of simplicity, we only print messages for every notification on standart output.
# #
# # Now you have the choice to either receive and process the notifications in the thread who instantiate the monitoring, the main benefit is that it doesn't need to instantiate a new thread, the drawback is to block your program in this task. Or, you don't want to block your main thread, so you can handle the notifications in a new separate thread. Choose which one is the most adapted to your needs and is consistent with your constraints and design choices. Next, we will detail the two approaches:
# # 	Notifier	ThreadedNotifier
# #
# # #First the import statements: the watch manager stores the watches and provide operations on watches. EventsCodes bring a set of codes, each code is associated to an event. ProcessEvent is the processing class.

import os
from pyinotify import WatchManager, Notifier, ThreadedNotifier, EventsCodes, ProcessEvent

wm = WatchManager()

#The following class inherit from ProcessEvent, handle notifications and process defined actions with individual processing methods whose the name is written with the specific syntax: process_EVENT_NAME where EVENT_NAME is the name of the handled event to process.

mask = EventsCodes.IN_DELETE | EventsCodes.IN_CREATE  # watched events

class PTmp(ProcessEvent):
    def process_IN_CREATE(self, event):
        print "Create: %s" %  os.path.join(event.path, event.name)

    def process_IN_DELETE(self, event):
        print "Remove: %s" %  os.path.join(event.path, event.name)


#   This statement instantiate our notifier class and realizes initializations with in particular the inotify's instantiation. The second parameter is a callable object the one which will be used to process notified events this way: PTmp()(event) where event is the notified event.
 #   The next statement add a watch on the first parameter and recursively on all its subdirectories, note that symlinks are not followed. The recursion is due to the optional parameter named 'rec' set to True. By default, the monitoring is limited to the level of the given directory. It returns a dict where keys are paths and values are corresponding watch descriptors (wd) and is assigned to wdd. An unique wd is attributed to every new watch. It is useful (and often necessary) to keep those wds for further updating or removing one of those watches, see the dedicated section. Obviously, if the monitored element had been a file, the rec parameter would have been ignored whatever its value.
  #  Let's start reading the events and processing them. Note that during the loop we can freely add, update or remove any watches, we can also do anything we want, even stuff unrelated to pyinotify. We call the stop() method when we want stop monitoring.

class Notifier(watchdir):
    notifier = Notifier(wm, PTmp())
    watchdir = os.path.abspath(watchdir)
    wdd = wm.add_watch(watchdir, mask, rec=True)
    while True:  # loop forever
    	try:								# process the queue of events as explained above
        	notifier.process_events()
        	if notifier.check_events():
        		notifier.read_events()
            	# read notified events and enqeue them

            # you can do some tasks here...

        except KeyboardInterrupt:		# destroy the inotify's instance on this interrupt (stop monitoring)
            notifier.stop()
            break




class ThreadedNotifier(watchdir):
    #The second line starts the new thread, doing actually nothing as no directory or file is being monitored.
    notifier = ThreadedNotifier(wm, PTmp())
    notifier.start()
    watchdir = os.path.abspath(watchdir)
    wdd = wm.add_watch(watchdir, mask, rec=True)

####
    ####At any moment we can for example remove the watch on '/tmp' like This:

    if wdd[watchdir] > 0:  # test if the wd is valid, this test is not mandatory
       wm.rm_watch(wdd[watchdir])

	###	#### Note that its subdirectories (if any) are still being watched. If we wanted to remove '/tmp' and all the watches on its sudirectories, we could have done like that:
####

    wm.rm_watch(wdd[watchdir], rec=True)
    wm.rm_watch(wdd.values())

    notifier.stop()

#    That is, most of the code is written, next, we can add, update or remove watches on files or directories with the same principles.
##		The only remaining important task is to stop the thread when we wish stop monitoring, it will automatically destroy the inotify's instance. Call the following method:


# The EventsCodes Class 	top
# Edited Sun, 26 Nov 2006 10:53
# Event Name	Is an Event	Description
# IN_ACCESS	Yes	file was accessed.
# IN_ATTRIB	Yes	metadata changed.
# IN_CLOSE_NOWRITE	Yes	unwrittable file was closed.
# IN_CLOSE_WRITE	Yes	writtable file was closed.
# IN_CREATE	Yes	file/dir was created in watched directory.
# IN_DELETE	Yes	file/dir was deleted in watched directory.
# IN_DELETE_SELF	Yes	watched item itself was deleted.
# IN_DONT_FOLLOW	No	don't follow a symlink (lk 2.6.15).
# IN_IGNORED	Yes	raised on watched item removing. Probably useless for you, prefer instead IN_DELETE*.
# IN_ISDIR	No	event occurred against directory. It is always piggybacked to an event. The Event structure automatically provide this information (via .is_dir)
# IN_MASK_ADD	No	to update a mask without overwriting the previous value (lk 2.6.14). Useful when updating a watch.
# IN_MODIFY	Yes	file was modified.
# IN_MOVE_SELF	Yes	watched item itself was moved, currently its full pathname destination can only be traced if its source directory and destination directory are both watched. Otherwise, the file is still being watched but you cannot rely anymore on the given path (.path)
# IN_MOVED_FROM	Yes	file/dir in a watched dir was moved from X. Can trace the full move of an item when IN_MOVED_TO is available too, in this case if the moved item is itself watched, its path will be updated (see IN_MOVE_SELF).
# IN_MOVED_TO	Yes	file/dir was moved to Y in a watched dir (see IN_MOVE_FROM).
# IN_ONLYDIR	No	only watch the path if it is a directory (lk 2.6.15). Usable when calling .add_watch.
# IN_OPEN	Yes	file was opened.
# IN_Q_OVERFLOW	Yes	event queued overflowed. This event doesn't belongs to any particular watch.
# IN_UNMOUNT	Yes	backing fs was unmounted. Notified to all watches located on this fs.
#
#
#     wd (int): is the Watch Descriptor, it is an unique identifier who represents the watched item through which this event could be observed.
#     path (str): is the complete path of the watched item as given in parameter to the method .add_watch.
#     name (str): is not None only if the watched item is a directory, and if the current event has occurred against an element included in that directory.
#     mask (int): is a bitmask of events, it carries all the types of events watched on wd.
#     event_name (str): readable event name.
#     is_dir (bool): is a boolean flag set to True if the event has occurred against a directory.
#     cookie (int): is a unique identifier permitting to tie together two related 'moved to' and 'moved from' events.
#


class MyProcessing(ProcessEvent):
    def __init__(self):
        """
        Does nothing in this case, but you can as well implement this constructor
        and you don't need to explicitely call its base class constructor.
        """
        pass

    def process_IN_DELETE(event):
        """
        This method process a specific kind of event (IN_DELETE). event
        is an instance of Event.
        """
        print '%s: deleted' % os.path.join(event.path, event.name)

    def process_IN_CLOSE(event):
        """
        This method is called for these events: IN_CLOSE_WRITE,
        IN_CLOSE_NOWRITE.
        """
        print '%s: closed' % os.path.join(event.path, event.name)

    def process_default(event):
        """
        Ultimately, this method is called for all others kind of events.
        This method can be used when similar processing can be applied
        to various events.
        """
        print 'default processing'

# Explanations and details:
#
#     IN_DELETE have its own method providing a specific treatment. We associate an individual processing method by providing a method whose the name is written with the specific syntax: process_EVENT_NAME where EVENT_NAME is the name of the handled event to process. For the sake of simplicity, our two methods are very basics they only print messages on standart output:
#     There are related events which needs most of the time the same treatment. It would be annoying to have to implement two times the same code. In this case we can define a common method. For example we want to share the same method for these two related events:
#
#     mask = EventsCodes.IN_CLOSE_WRITE | EventsCodes.IN_CLOSE_NOWRITE
#
#     Then it's enough to provide a single processing method named process_IN_CLOSE according to the general syntax process_IN_FAMILYBASENAME. The two previous events will be processed by this method. In this case, beware to not implement process_IN_CLOSE_WRITE or process_IN_CLOSE_NOWRITE, because these methods have an higher precedence (see below), thereby are looked first and would have been called instead of process_IN_CLOSE (for a complete example see: src/examples/close.py).
#     It only makes sense to define process_IN_Q_OVERFLOW when its class instance is given to Notifier, indeed it could never be called from a processed object associated to a watch, because this event isn't associated to any watch.
#     EventsCodes.ALL_EVENTS isn't an event by itself, that means that you don't have to implement the method process_ALL_EVENTS (even worst it would be wrong to define this method), this is just an alias to tell the kernel we want to be notified for all kind of events on a given watch. The kernel raises individual events (with the IN_ISDIR flag if necessary). Instead, if we need to apply the same actions whatever the kind of event, we should implement a process_default method (for a complete example see: src/examples/simple.py).
#     Processing methods lookup's order (ordered by increasing order of priority): specialized method (ex: process_IN_CLOSE_WRITE) first, then family method (ex: process_IN_CLOSE), then default method (process_default).
#     One more thing: say you redifine the method process_default which contains the instruction os.ismount(my-mount-point), it would be for example a mistake having this method called for every event IN_OPEN occurred in /etc. Because, one particularity of os.ismount is to check in /etc/mtab if the partition is mounted, so we could easily imagine the kind of endless situation: call process_IN_OPEN, open /etc/mtab, call process_IN_OPEN, open /etc/mtab ... loop forever.
#
# Whenever possible you should process your notifications this way, with a single processing object. It is easy to imagine the benefits to have to deal with only one instance (efficiency, data sharing,...):

path = os.path.abspath(watchdir)
notifier = Notifier(wm, MyProcessing())
mask = EventsCodes.ALL_EVENTS
wm.add_watch(path, mask, proc_fun=MyProcessing())


# Read notifications, process events.
#     watch_manager is an instance of WatchManager.
#     default_proc_funcis an instance of ProcessEvent or one of its subclasses.

Notifier(watch_manager, default_proc_func=ProcessEvent())
check_events(timeout=4) 			#=> None		#Check for new events available to read.
timeout(int) 						#timeout passed on to select.select().
process_events() 					#=> None			#	#Routine for processing events from queue by calling their associated processing function (instance of ProcessEvent or one of its subclasses).
read_events() 						#=> None				#Read events from device and enqueue them, waiting to be processed.
stop() 								#=> None						#Stop the notifications.


ThreadedNotifier(watch_manager, default_proc_func=ProcessEvent())
										# 	  This notifier inherits from threading.Thread and from Notifier, instantiating a separate thread, and providing standart Notifier functionalities. This is a threaded version of Notifier.
										#     watch_manager is an instance of WatchManager.
										#     default_proc_funcis an instance of ProcessEvent or one of its subclasses.
										#     inherits all the methods of Notifier but override the stop() method.
start() 		#=> None				#Start the new thread, start events notifications.
stop() 			#=> None				#Stop the thread, stop the notifications.




#Represent a watch, i.e. a file or directory being watched.
# def Watch(wd, path, mask, proc_func, auto_add):
# 	wd(int) = wd 					#Watch Descriptor.
# 	path = os.path.abspath(watchdir)
# 	#path(str) = path				# Path of the file or directory being watched.
# 	mask(int) = mask				#Mask.
# 	proc_fun(ProcessEvent) = proc_func	#Processing object.
# 	auto_add(bool) = auto_add 					#Automatically add watches on creation of directories.


#The Watch Manager lets the client add a new watch, store the active watches, and provide operations on these watches.
##Add watch(s) on given path(s) with the specified mask.


class WatchManager(watchdir):
	path = os.path.abspath(watchdir)				#path = list() ##(str or list of str): ## Path(s) to watch, the path can either be a file or a directory.
	add_watch(path, mask, proc_fun=None, rec=False, auto_add=False) = dict()		#=> dict
	mask(int) = int(mask) 							#Bitmask of events.
	proc_func(ProcessEvent) = proc_func 			###	Processing object (must be callable). Will be called if provided, otherwise, notifier.default_proc_funcwill be called.
	rec(bool) =  bool(rec) 							######	Recursively add watches on the given path and on all its subdirectories.
	auto_add(bool) = bool(auto_add) 				#	Automatically add watches on newly created directories in the watch's path.
	update_watch(wd, mask=None, proc_func=None, rec=False, auto_add=False) = update_watch		#=> dict
											#Update existing watch(s). All these parameters are updatable.
	rm_watch(wd, rec=False) = dict() #=> dict			#Remove watch(s).
	get_wd(path) 		#=> int						#Return the watch descriptor associated to path.
	get_path(wd) 		#=> str						#Return the path associated to wd, if wd is invalid, None is returned.
	return os.path.abspath(wd)



ra = notifier.add_watch('/a-dir', mask)
if ra['/a-dir'] > 0: print "added"


#update_watch wd (or list of wds) 	{wd1: success, wd2: success, ...}
	#Where success is True if the op on wdx succeeded, False otherwise.
ru = notifier.update_watch(ra['/a-dir'], new_mask)
if ru['/a-dir']: print "updated"


#rm_watch 	wd (or list of wds) 	{wd1: success, wd2: success, ...}
	#Where success is True if the op on wdx succeeded, False otherwise.
rr = notifier.rm_watch(ra['/a-dir'])
if rr['/a-dir']: print "deleted"
