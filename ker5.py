import socket               
import sys
import os
import os.path
import time
from Crypto.Hash import SHA256
from base64 import b64encode as be, b64decode as bd
from Crypto.Cipher import AES
from Crypto import Random

def getFSPort(fs):
	return int(fs[len(fs)-1:]) + 8680
def getASPort():
	return 6583
def getTGSPort():
	return 8471

def aes_ecb_enc(key,msg):
	obj = AES.new(key, AES.MODE_ECB)
 	return obj.encrypt(msg)

def aes_ecb_dec(key,msg):
	obj = AES.new(key, AES.MODE_ECB)
 	return obj.decrypt(msg)

def add_padding(msg):
	l = 16 - (len(msg) % 16)
	return msg + ('{' * (l%16))

def remove_padding(msg):
	return msg.rstrip('{')

def getUserNo(user):
	l = len(user)
	if(user[l-1:] == "0"):
		return user[l-2:]
	return user[l-1:]

def getFileServerNo(fs):
	return fs[len(fs)-1:]

def main():

	while True:
		comm = raw_input("ker5>")
		if(comm == 'exit'):
			os.system("ps > temp.txt")
			process = getPythonProcesses()
			print(process)
			process.remove(currProcID)
			print(process)
			for id in process:
				os.system("kill " + str(id))
			os.system("rm temp.txt")
			os.system("rm dump.txt")
			exit()
		else:
			comm_split = comm.split()
			# print(comm_split)
			rndfile = Random.new()
			if(len(comm_split) < 4):
				print('Error in command!\nChoose again....')
				continue
			user = comm_split[1]
			fileserver = comm_split[2]
			filename = comm_split[3]
			if(comm_split[0] == 'get' or comm_split[0] == 'put'):
				flag = 0
				flag_ = 0
				print('get/put')
				if(int(getFileServerNo(fileserver)) not in fs_list):
					print('File server not active! Try again..')
					continue
				fname = 'key_user_' + str(getUserNo(user)) + '_fs_' + str(getFileServerNo(fileserver)) + '.txt'
				fpath =  user + '/' + fname
				print(fpath)
				if(os.path.exists(fpath)):
					flag = 1
					t1=(time.time())
					t2=(os.path.getmtime(fpath))
					print('file exists')
					print(t1-t2)
					if(t1-t2 > 180):
						print('Kc,v Expired')
						flag = 0
						fname_ = 'key_user_' + str(getUserNo(user)) + '_tgs.txt'
						fpath_ = user + '/' + fname_
						if(os.path.exists(fpath_)):
							flag_ = 1
							t1_ = (time.time())
							t2_ = (os.path.getmtime(fpath_))
							if(t1_ - t2_ > 180):
								print('Kc,tgs Expired')
								flag_ = 0
							else:
								print('Kc,tgs Valid')
					else:
						print('Kc,v Valid')
				if(flag == 0 and flag_ == 0):
					# Establish Kc,tgs
					s = socket.socket()
					port = getASPort()
					s.connect(('127.0.0.1', port))
					T = str(time.time())
					Nonce = be(rndfile.read(16))
					s.send(user + ' ' + T + ' ' + Nonce)
					# print s.recv(1024)
					f = open(user + '/key.txt')
					kc = bd(f.readline())
					f.close()
					as_msg = s.recv(1024)
					as_msg_split = as_msg.split(' ')
					userid = as_msg_split[0]
					ticket_tgs = as_msg_split[1]
					ekc_enc = bd(as_msg_split[2])
					ekc_msg = remove_padding(aes_ecb_dec(kc,ekc_enc))
					ekc_msg_split = ekc_msg.split(' ')
					# print(ekc_msg_split[0])
					if(userid == user and T == ekc_msg_split[1] and Nonce == ekc_msg_split[2]):
						f = open(user + '/key_user_' + str(getUserNo(user)) + '_tgs.txt','w')
						f.write(ekc_msg_split[0] + ' ' + ticket_tgs)
						f.close()
					else:
						print('Error in AS')
						continue
					s.close()

				if(flag == 0):
					# Establish Kc,v
					f = open(user + '/key_user_' + str(getUserNo(user)) + '_tgs.txt','r')
					tmp = f.readline().split(' ')
					key_c_tgs = bd(tmp[0])
					ticket_tgs = tmp[1]
					f.close()
					s = socket.socket()
					port = getTGSPort()
					s.connect(('127.0.0.1', port))
					Nonce_ = be(rndfile.read(16))
					TS1 = str(time.time())
					auth_msg = user + ' ' + TS1
					auth_c = aes_ecb_enc(key_c_tgs,add_padding(auth_msg))
					tgs_msg = fileserver + ' ' + TS1 + ' ' + Nonce_ + ' ' + ticket_tgs + ' ' + be(auth_c)
					s.send(tgs_msg)

					tgs_recv_msg = s.recv(2000)
					# print(tgs_recv_msg)
					if(tgs_recv_msg == 'ERROR'):
						print('TGS Authentication failed.. Try again')
						continue
					tgs_recv_msg_split = tgs_recv_msg.split(' ')
					userid = tgs_recv_msg_split[0]
					ticket_v = tgs_recv_msg_split[1]
					e_k_c_tgs_enc = bd(tgs_recv_msg_split[2])
					e_k_c_tgs_msg = remove_padding(aes_ecb_dec(key_c_tgs,e_k_c_tgs_enc))

					e_k_c_tgs_split = e_k_c_tgs_msg.split(' ')
					
					key_c_v = e_k_c_tgs_split[0]
					TS1_ = e_k_c_tgs_split[1]
					Nonce_tgs = e_k_c_tgs_split[2]
					fileserver_ = e_k_c_tgs_split[3]
					if(userid == user and TS1 == TS1_ and Nonce_ == Nonce_tgs and fileserver == fileserver_):
						f = open(user + '/key_user_' + str(getUserNo(user)) + '_fs_' + str(getFileServerNo(fileserver)) + '.txt','w')
						f.write(key_c_v + ' ' + ticket_v)
						f.close()
					else:
						print('Error in TGS')
						continue
					s.close()
			else:
				print('Error in command!\nChoose again....')
				continue
	 
def getPythonProcesses():
	f = open("temp.txt")
	procList = []
	for x in f:
		if(x != "\n"):
			x_split = x.split()
			if(x_split[3] == 'python'):
				procList.append(int(x_split[0]))
				# print(x_split[0])
	return procList

# print(sys.argv)
N = int(sys.argv[2])
if(N<3 or N>9):
	print('Error in command!\nAborting')
	exit()
# print(N)
l = len(sys.argv)
fs_list = []
for i in range(3,l):
	temp = int(sys.argv[i][2:])
	if(temp<1 or temp>9):
		print('Error in command!\nAborting')
		exit()	
	if(temp not in fs_list):
		fs_list.append(temp)
print(fs_list)
if(N != len(fs_list)):
	print('Error in command!\nAborting')
	exit()

os.system("ps > temp.txt")
process = getPythonProcesses()
if(len(process)>1):
	print("Error!!")
	exit()
currProcID = process[0]
# print(currProcID)
os.system("python -u as.py cseiitm2017 >> dump.txt &")
os.system("python -u tgs.py cseiitm2017 >> dump.txt &")
for n in fs_list:
	os.system("python -u fs.py " + str(n) + " >> dump.txt &")

main()