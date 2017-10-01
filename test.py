f = open("temp.txt")

for x in f:
	if(x != "\n"):
		x_split = x.split()
		if(x_split[3] == 'python'):
			print(x_split[0])