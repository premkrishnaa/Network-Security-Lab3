import socket               
import sys
import os

def main():

	while True:
		comm = raw_input("ker5>")
		if(comm == 'exit'):
			os.system("ps > temp.txt")
			process = getPythonProcesses()
			# print(process)
			process.remove(currProcID)
			# print(process)
			for id in process:
				os.system("kill " + str(id))
			os.system("rm temp.txt")
			exit()
		else:
			comm_split = comm.split()
			# print(comm_split)
			if(comm_split[0] == 'get'):
				print('get')
			elif(comm_split[0] == 'put'):
				print('put')
			else:
				print('Error in command!\nAborting....')
				exit()
	 
	s = socket.socket()         
	 
	port = 6583               
	 
	s.connect(('127.0.0.1', port))
	 
	print s.recv(1024)
	s.close() 

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
# print(fs_list)
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
os.system("python as.py &")
os.system("python tgs.py &")
for n in fs_list:
	os.system("python fs.py " + str(n) + " &")

main()