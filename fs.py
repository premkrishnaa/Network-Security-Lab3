import socket       
import sys

def main():
	 
	s = socket.socket()         
	print "Socket successfully created"
	 
	port = 8680 + id
	# print(port)         
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 	 
	s.bind(('', port))        
	print "socket binded to %s" %(port)
	 
	s.listen(5)     
	print "socket is listening"           
	 
	while True:
	 
		c, addr = s.accept()     
		print 'Got connection from', addr
		c.send('Thank you for connecting')
	 
	   	c.close()

id = int(sys.argv[1])
main()