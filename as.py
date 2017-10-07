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

def aes_cbc_dec(key,iv,msg):
	obj = AES.new(key, AES.MODE_CBC, iv)
 	return obj.decrypt(msg)

def aes_ecb_enc(key,msg):
	obj = AES.new(key, AES.MODE_ECB)
 	return obj.encrypt(msg)

def add_padding(msg):
	l = 16 - (len(msg) % 16)
	return msg + ('{' * (l))

def main():
	 
	s = socket.socket()         
	print "Socket successfully created"
	 
	port = 6583               
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
	s.bind(('', port))        
	print "socket binded to %s" %(port)
	 
	s.listen(5)     
	print "socket is listening"           
	 
	while True:
	 
		c, addr = s.accept()     
		print 'Got connection from', addr
	 	data = str(c.recv(100))
	 	# print(data)
	 	data_split = data.split(' ')
	 	# print(data_split)
	 	user = data_split[0]
	 	T = data_split[1]
	 	Nonce = data_split[2]

	 	rndfile = Random.new()
	 	# print(user,T,Nonce)
		hash = SHA256.new()
		hash.update(password)
		key = hash.digest()[:16]
		iv = hash.digest()[16:]
	 	user_key_file = 'AS/key_user_' + str(getUserNo(user)) + '.txt'
	 	f = open(user_key_file,'r')
		user_key_encrypted = bd(f.readline())
	 	user_key = aes_cbc_dec(key,iv,user_key_encrypted)
	 	f.close()

	 	f = open('AS/key_tgs.txt','r')
	 	key_tgs_encrypted = bd(f.readline())
		key_tgs = aes_cbc_dec(key,iv,key_tgs_encrypted)
		f.close()

		print('key_tgs: ' + be(key_tgs))
		print('user_key: ' + be(user_key))

		key_c_tgs = be(rndfile.read(16)) 
		print('key_c_tgs: ' + key_c_tgs)		

		ekc_msg = key_c_tgs + ' ' + T + ' ' + Nonce
		ekc = be(aes_ecb_enc(user_key,add_padding(ekc_msg)))

		ticket_msg = key_c_tgs + ' ' + user + ' ' + addr[0] + ' ' + T
		print('ticket_msg: ' + ticket_msg)
		ticket_tgs = be(aes_ecb_enc(key_tgs,add_padding(ticket_msg)))

		msg = user + ' ' + ticket_tgs + ' ' + ekc

		c.send(msg)
	 
	   	c.close()

password = sys.argv[1]
main()