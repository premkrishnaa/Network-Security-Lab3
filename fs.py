import socket       
import sys
import os.path
from base64 import b64encode as be
from base64 import b64decode as bd
from Crypto.Cipher import AES

def getUserNo(user):
	l = len(user)
	if(user[l-1:] == "0"):
		return user[l-2:]
	return user[l-1:]

def getFileServerNo(fs):
	return fs[len(fs)-1:]

def aes_ecb_enc(key,msg):
	obj = AES.new(key, AES.MODE_ECB)
 	return obj.encrypt(msg)

def aes_ecb_dec(key,msg):
	obj = AES.new(key, AES.MODE_ECB)
 	return obj.decrypt(msg)

def add_padding(msg):
	l = 16 - (len(msg) % 16)
	return msg + ('{' * (l))

def remove_padding(msg):
	return msg.rstrip('{')

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

	 	data = c.recv(3000)
	 	# print(data)

	 	data_split = data.split(' ')
	 	# print(data_split)
	 	option = data_split[0]
		fileserver = 'FS' + str(id)
	 	if(option == 'AUTH'):
		 	ticket_v = data_split[1]
		 	auth_v = data_split[2]
		 	server_key_file = fileserver + '/key.txt'
		 	f = open(server_key_file,'r')
			server_key = bd(f.readline())
		 	f.close()

			print('server_key: ' + be(server_key))
			ticket_v_msg = remove_padding(aes_ecb_dec(server_key,bd(ticket_v)))
			ticket_v_msg_split = ticket_v_msg.split()
			key_c_v = bd(ticket_v_msg_split[0])
			userid = ticket_v_msg_split[1]
			TS1 = ticket_v_msg_split[2]

			auth_v_msg = remove_padding(aes_ecb_dec(key_c_v,bd(auth_v)))
			auth_v_msg_split = auth_v_msg.split()
			userid_ = auth_v_msg_split[0]
			fileserver_ = auth_v_msg_split[1]
			TS2 = auth_v_msg_split[2]
			if(userid != userid_ or fileserver_ != fileserver or float(TS1) > float(TS2)):
				c.send('ERROR')
			else:
				f = open(fileserver + '/key_user_' + str(getUserNo(userid)) + '_fs_' + str(getFileServerNo(fileserver)) + '.txt', 'w')
				f.write(ticket_v_msg_split[0])
				f.close() 
				msg = be(aes_ecb_enc(key_c_v,add_padding(TS2)))
	 			c.send(msg)
		else:
			userid = data_split[1]
			filename = data_split[2]
			f = open(fileserver + '/key_user_' + str(getUserNo(userid)) + '_fs_' + str(getFileServerNo(fileserver)) + '.txt', 'r')
			key_c_v = bd(f.readline())
			f.close()
			if(option == 'PUT'):
				filetext_encoded = data_split[3]
				filetext = remove_padding(aes_ecb_dec(key_c_v,bd(filetext_encoded)))
				# print(filetext)
				filename_enc = filename + '.enc'
				f = open(fileserver + '/' + userid + '/' + filename_enc,'w')
				f.write(filetext_encoded)
				f.close()
				f = open(fileserver + '/' + userid + '/' + filename,'w')
				f.write(filetext)
				f.close()
			elif(option == 'GET'):
				filepath = fileserver + '/' + userid + '/' + filename
				if(os.path.exists(filepath)):
					f = open(filepath,'r')
					filetext = ''
					for ln in f.readlines():
						filetext += ln
					filetext_encoded = be(aes_ecb_enc(key_c_v,add_padding(filetext)))
					c.send(filetext_encoded)
				else:
					c.send('NONE')
	   	c.close()

id = int(sys.argv[1])
main()