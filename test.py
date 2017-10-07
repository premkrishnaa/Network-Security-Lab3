import os.path
import time
if(os.path.exists('user1/key.txt')):
	t1=(time.time())
	t2=(os.path.getmtime('user1/key.txt'))
	print('file exists')
	print(t1-t2)
	if(t1-t2 > 180):
		print('Expired')
	else:
		print('Valid')
	# f = open('temp.txt','r')
else:
	print('No file exists')