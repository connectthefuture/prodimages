#!/usr/bin/python

import httplib,time,csv,getopt,sys,Queue,threading
from timeit import Timer
from urlparse import urlsplit,urlunsplit

HTTP_TIMEOUT = 120.0
workers = []


def readFile(str):
    urilist = Queue.Queue()
    reader = csv.reader(open(str,"rb"))
    for row in reader :
        urilist.put(row[0])
    return urilist

def usage():
    print "Usage: warmup_svr.py [-v] [-i file|--input=file] [--help] [-s|--server=server] [-t|--threads=numthreads] [-h|--header=header]"

def threadedWarmupServer(server,URIQueue,threadnum,verbose,header):
    serveroverride = False

    if server != None:
        serveroverride = True

    a = True
    while a:
        try:
            uri = URIQueue.get(0)
            u = urlsplit(uri)
            if serveroverride == True:
                conn = httplib.HTTPConnection(server)
            else:
                if len(u[1]) == 0 :
                    conn = False
                else :
                    conn = httplib.HTTPConnection(u[1])
                    server = u[1]
            startTime = time.time()
            try:
                if len(u[3]) == 0:
                    conn.request("GET", u[2])
                else:
                    conn.request("GET", u[2]+"?"+u[3])
            except Exception:
                startTime = -1
                elapsed = float((time.time() - startTime))
                print "[%.0f] %s %.4f FAILED CONNECTION" % (threadnum, uri, elapsed)
            else:
                r = conn.getresponse()
                elapsed = float((time.time() - startTime))
                if len(u[3]) == 0:
                    print "[%.0f] %s://%s%s%s%s %.4f %s %s" % (threadnum,"http",server,u[2],u[3],u[4], elapsed, r.status, r.reason)
                else:
                    print "[%.0f] %s://%s%s?%s%s %.4f %s %s" % (threadnum,"http",server,u[2],u[3],u[4], elapsed, r.status, r.reason)
                if header != None :
                    print "###HEADER %s###\n" %header,r.getheader(header),"\n###END_HEADER %s###\n" %header
                if verbose:
                    print "###HEADERS###\n",r.getheaders(),"\n###END_HEADERS###"

                r.read()
        except Queue.Empty:
            a = False

## GETTING COMMAND LINE OPTIONS

def main():

### DECLARING VARIABLES
    input = None
    verbose = False
    server = None
    MAX_THREADS = 3
    header = None

    startTime = time.time()
    urilist = Queue.Queue()

    try:
        opts,args = getopt.getopt(sys.argv[1:], "i:s:t:vh", ["help", "input=", "server=","threads=","header="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

#    print opts,args
#    sys.exit()

    for o, a in opts:
        if o == "-v":
            verbose = True
        if o in ("-h", "--header"):
            header = a;
        if o in ("--help"):
            usage()
            sys.exit()
        if o in ("-i", "--input"):
            input = a;
        if o in ("-s", "--server"):
            server = a;
        if o in ("-t", "--threads"):
            MAX_THREADS = int(a);


    if input == None :
        urilist.put("http://localhost/")
    else:
        urilist = readFile(input)

### Creating Worker threads and kicking them off
### urilist is a Queue that is threadsafe

    ### Making sure we are not creating more threads than queue size
    numthreads = min(MAX_THREADS, urilist.qsize())
    for i in range(numthreads):
        workers.append(threading.Thread(target=threadedWarmupServer, args=(server,urilist,i,verbose,header)))
        workers[-1].start()

### Verifying that workers are finished

    for w in workers:
        w.join()
### Finishing up and logging how long we took

    elapsed = float((time.time() - startTime))
    print "Total running time: %.4f" %elapsed

if __name__ == "__main__":
    main()

