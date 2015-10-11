import socket
import sys
def socketClient(HOST,PORT):
	#host, port = "localhost", 8082
	data = " ".join(sys.argv[1:])

# Create a socket (SOCK_STREAM means a TCP socket)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server and send data
	sock.connect((HOST, PORT))
	sock.send(data + "\n")

# Receive data from the server and shut down
	received = sock.recv(1024)
	sock.close()

	print "Sent:	 %s" % data
	print "Received: %s" % received
	
	
socketClient("localhost", 8082, data="Message__D")

#print client


