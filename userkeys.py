from Crypto.Hash import SHA256
import base64
import os

for i in range(1,11):
	hash = SHA256.new()
	k = 'pwd' + str(i) + 'user' + str(i) + 'pwd'
	print(k)
	loc = 'user' + str(i) + '/key.txt'
	hash.update(k)
	enc = base64.b64encode(hash.digest()[:16])
	print(enc)
	dec = base64.b64decode(enc)
	print(dec == hash.digest()[:16])
	f = open(loc,'w')
	f.write(enc)
	print(len(enc))
	f.close()