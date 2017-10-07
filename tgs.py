import socket               
import sys
from Crypto.Hash import SHA256
from base64 import b64encode as be
from base64 import b64decode as bd
from Crypto.Cipher import AES
from Crypto import Random

def getUserNo(user):
	l = len(user)
	if(user[l-1:] == "0"):
		return user[l-2:]
	return user[l-1:]

def getFileServerNo(fs):
	return fs[len(fs)-1:]

def aes_cbc_dec(key,iv,msg):
	obj = AES.new(key, AES.MODE_CBC, iv)
 	return obj.decrypt(msg)

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
	 
	port = 8471               	 
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
	s.bind(('', port))        
	print "socket binded to %s" %(port)
	 
	s.listen(5)     
	print "socket is listening"           
	 
	while True:
	 
		c, addr = s.accept()     
		print 'Got connection from', addr
	 	data = c.recv(2000)
	 	# print(data)

	 	data_split = data.split(' ')
	 	# print(data_split)
	 	fileserver = data_split[0]
	 	TS1 = data_split[1]
	 	Nonce_ = data_split[2]
	 	ticket_tgs = data_split[3]
	 	auth_c = data_split[4]

	 	rndfile = Random.new()

		hash = SHA256.new()
		hash.update(password)
		key = hash.digest()[:16]
		iv = hash.digest()[16:]
	 	server_key_file = 'TGS/key_fs_' + str(getFileServerNo(fileserver)) + '.txt'
	 	f = open(server_key_file,'r')
		server_key_encrypted = bd(f.readline())
	 	server_key = aes_cbc_dec(key,iv,server_key_encrypted)
	 	f.close()

	 	f = open('TGS/key_tgs.txt','r')
	 	key_tgs_encrypted = bd(f.readline())
		key_tgs = aes_cbc_dec(key,iv,key_tgs_encrypted)
		f.close()

		print('key_tgs: ' + be(key_tgs))
		print('server_key: ' + be(server_key))

		key_c_v = be(rndfile.read(16)) 
		print('key_c_v: ' + key_c_v)		

		ticket_tgs_msg = remove_padding(aes_ecb_dec(key_tgs,bd(ticket_tgs)))
		print(ticket_tgs_msg)
		ticket_tgs_msg_split = ticket_tgs_msg.split(' ')
		key_c_tgs = bd(ticket_tgs_msg_split[0])
		userid = ticket_tgs_msg_split[1]
		useraddr = ticket_tgs_msg_split[2]
		T = (ticket_tgs_msg_split[3])

		auth_c_msg = remove_padding(aes_ecb_dec(key_c_tgs,bd(auth_c)))
		print(auth_c_msg)
		auth_c_msg_split = auth_c_msg.split(' ')
		userid_ = auth_c_msg_split[0]
		TS1_ = auth_c_msg_split[1]

		if(TS1_ != TS1 or userid != userid_ or useraddr != str(addr[0]) or float(T) > float(TS1)):
			c.send('ERROR')
		else:
			f = open('TGS/key_user_' + getUserNo(userid) + '_tgs.txt','w')
			f.write(be(key_c_tgs))
			f.close()

			ticket_v_msg = key_c_v + ' ' +  userid + ' ' + TS1
			ticket_v = aes_ecb_enc(server_key,add_padding(ticket_v_msg))
			
			k_c_tgs_msg = key_c_v + ' ' + TS1 + ' ' + Nonce_ + ' ' + fileserver
			e_k_c_tgs = aes_ecb_enc(key_c_tgs,add_padding(k_c_tgs_msg))
			print('k_c_tgs_msg: ' + k_c_tgs_msg)

			msg = userid + ' ' + be(ticket_v) + ' ' + be(e_k_c_tgs)
			print(remove_padding(aes_ecb_dec(key_c_tgs,e_k_c_tgs)))
			c.send(msg)
	 
	   	c.close()

password = sys.argv[1]
print(password)
main()