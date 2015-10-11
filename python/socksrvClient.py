from collections import deque
import os
sys.path += [os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')]
#queue = deque([newlist.append(link)])


import socket
address= ('localhost', 8082)
sclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sclient.connect(address)
#print sclient.gethostname()
sclient.send("client sending %s%s" % address)
data = sclient.recv(1024)

sclient.close()

print 'Data Sent, Client Closed'

print 'Received:'
print data
#server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#server_address = ('localhost', 8082)
#server.bind(server_address)
#server.listen(5)

#connection, client_address = server.accept()

#print 'connection from:', connection.getpeername()


#connection.shutdown(socket.SHUT_RD | socket.SHUT_WR)
#connection.close()

#print 'Connection closed'

#server.close()
