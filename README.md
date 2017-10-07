Assumptions: The file directory structure is already present, size of the file being sent/received is atmost 2000 bytes

userkeys.py, fileserverkeys.py and as_tgs_enc_keys.py have been used to generate the keys that are assumed to be pre-existing

To run the client:

python ker5.py -N <3-9> <FileServers>

Note: There is no Makefile here since its a python project

script file is script.log, timing file is time.txt
Scriptreplay command:
	scriptreplay --timing=time.txt script.log