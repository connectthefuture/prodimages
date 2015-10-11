import socket, os, sys

#CFG_SRV_BIND_IF = socket.gethostname()
CFG_SRV_BIND_IF = socket.gethostname()
CFG_SRV_BIND_PORT = 8082
CFG_SRV_LISTEN_BACKLOG = 10

HTTP_RESPONSE = '''HTTP/1.1 200 OK
Date: Mon, 13 May 2013 19:27:06 GMTServer: Apache/2.2.2 (Unix) mod_ssl/2.2.3 OpenSSL/0.9.81 mod_wsgi/1.0.2 Python/2.7.3
Content-Length:49
Content-Type: text/html
Connection: close

<html><body><h1>THIS IS THE RESPONSE!</h1></body></html>
'''

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_address = (CFG_SRV_BIND_IF, CFG_SRV_BIND_PORT)

print >>sys.stderr, 'Our URL is http://localhost:%d' % server_address[1]
print >>sys.stderr, 'We can only be stopped by ctrl-c'

server.bind(server_address)
    #bind((socket.gethostname(), 80))

server.listen(CFG_SRV_LISTEN_BACKLOG)

while True:
	try:
		connection, client_address = server.accept()
		print >>sys.stderr, 'New Connection From', client_address
		data = connection.recv(1024)
		if data:
            data = str(data)
            print data
            connection.send("%s" % data)    
        #	break
    	#connection.send(data)
		connection.send("%s" % HTTP_RESPONSE)
		print >>sys.stderr, 'Response Sent'
		
		connection.shutdown(socket.SHUT_RD | socket.SHUT_WR)
		
		connection.close()
		print >>sys.stderr, 'Connection Closed'
#print 'connection from:', connection.getpeername()
	except:
		print '\nOuch that Hurt'
		break

		
print >>sys.stderr, 'System Shutting Down'
server.close()
print >>sys.stderr, 'Its Closed'
#connection.shutdown(socket.SHUT_RD | socket.SHUT_WR)
#connection.close()

#print 'Connection closed'

#server.close
#conn, addr = s.accept()

#while True:
#    data = conn.recv(1024)
#    if not data:
#        break
#    conn.send(data)

#conn.close()
#os.unlink(FILE)

