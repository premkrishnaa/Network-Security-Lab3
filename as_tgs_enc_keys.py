from Crypto.Hash import SHA256
from Crypto.Cipher import AES
import base64
import os

for i in range(1,11):
	hash = SHA256.new()
	loc = 'user' + str(i) + '/key.txt'
	fname = 'AS/key_user_' + str(i) + '.txt'
	f = open(loc,'r')
	s = f.readline()
	print(len(s))
	print(s)
	f.close()
	password = 'cseiitm2017'
	print('password len: ' + str(len(password)))
	hash.update(password)
	key = hash.digest()[:16]
	iv = hash.digest()[16:]
	print(base64.b64encode(key),base64.b64encode(iv))
	obj = AES.new(key, AES.MODE_CBC, iv)
	ciphertext = obj.encrypt(base64.b64decode(s))
	obj1 = AES.new(key, AES.MODE_CBC, iv)
	plaintext = obj1.decrypt(ciphertext)
	print(base64.b64encode(plaintext) == s)
	f = open(fname,'w')
	f.write(base64.b64encode(ciphertext))
	f.close()

for i in range(1,10):
	hash = SHA256.new()
	loc = 'FS' + str(i) + '/key.txt'
	fname = 'TGS/key_fs_' + str(i) + '.txt'
	f = open(loc,'r')
	s = f.readline()
	print(len(s))
	f.close()
	password = 'cseiitm2017'
	hash.update(password)
	key = hash.digest()[:16]
	iv = hash.digest()[16:]
	obj = AES.new(key, AES.MODE_CBC, iv)
	ciphertext = obj.encrypt(base64.b64decode(s))
	obj1 = AES.new(key, AES.MODE_CBC, iv)
	plaintext = obj1.decrypt(ciphertext)
	print(base64.b64encode(plaintext) == s)
	f = open(fname,'w')
	f.write(base64.b64encode(ciphertext))
	f.close()

hash = SHA256.new()
k = 'pwd' + 'TGSKEY' + 'pwd'
print(k)
hash.update(k)
s = hash.digest()[:16]
hash =SHA256.new()
password = 'cseiitm2017'
hash.update(password)
key = hash.digest()[:16]
iv = hash.digest()[16:]
obj = AES.new(key, AES.MODE_CBC, iv)
ciphertext = obj.encrypt(s)
obj1 = AES.new(key, AES.MODE_CBC, iv)
plaintext = obj1.decrypt(ciphertext)
print(plaintext == s)
loc = 'AS' + '/key_tgs.txt'
f = open(loc,'w')
f.write(base64.b64encode(ciphertext))
f.close()
loc = 'TGS' + '/key_tgs.txt'
f = open(loc,'w')
f.write(base64.b64encode(ciphertext))
f.close()