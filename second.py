import os
import subprocess
import time
import _mysql
import MySQLdb
import peewee
def stringtointeger(x):
	try:
		return int(x)
	except ValueError:
		return x
def stringtofloat(x):
	try:	
		return float(x)
	except ValueError:
		return x	
def getlowerprocesses(array):
	filee=open("lower.txt","r+")
	for line in filee:
		if(type(stringtointeger(line)) is int):
			if(stringtointeger(line)>=1 and stringtointeger(line)<161):
				temp=stringtointeger(line)
				array.append(temp)
	return array
def gethigherprocesses(array):
	filee=open("higher.txt","r+")
	for line in filee:
		if(type(stringtointeger(line)) is int):
			if(stringtointeger(line)>=161 and stringtointeger(line)<10000):
				temp=stringtointeger(line)
				array.append(temp)
	return array
def getProcesses(array):
	getlowerprocesses(array)
	temparray=[]
	gethigherprocesses(temparray)
	for num in temparray:
		array.append(num)
	return array
def getProcessCPU(processid):
	proc=subprocess.Popen("ps -p "+str(processid)+" -o %cpu | tail -n 1 | cut -d ' ' -f 2" ,stdout=subprocess.PIPE,shell=True)
	return stringtofloat(proc.stdout.read())
def getProcessMemory(processid):
	proc=subprocess.Popen("ps -p "+str(processid)+" -o %mem | tail -n 1 | cut -d ' ' -f 2",stdout=subprocess.PIPE,shell=True)
	return stringtofloat(proc.stdout.read())
def getProcessCMD(processid):
	proc=subprocess.Popen("cat /proc/"+str(processid)+"/cmdline",stdout=subprocess.PIPE,shell=True)
	return proc.stdout.read()
def writeIntoDatabase(array):
	db = MySQLdatabase("Processes",usr="root",passwd="klavye123")
	x=db.cursor()
	for proc in array:
		Process_ID=stringtointeger(proc)
		CPU=getProcessCPU(proc)
		MEM=getProcessMemory(proc)
		CMD=getProcessCMD(proc)
		print "Process ID : "Process_ID
		print "CPU Usage : %"CPU
		print "Memory Usage : %"MEM
		print "CMD Directory : %"CMD
		now=time.strftime("%Y-%m-%d %H:%M:%S")
		print now
		x.execute("""INSERT INTO Process (ProcessID,CMD,CPU,MEM,TIME) values (%s,%s,%s,%s,%s)""",(Process_ID,CMD,CPU,MEM,now))
                db.commit()		

def subprocesscalls():
	subprocess.call("ps aux | cut -d ' ' -f 9-10 | cat > lower.txt",shell=True)
	subprocess.call("ps aux | cut -d ' ' -f 5-8 | awk 'NF' | cut -c 1-6 | cat > higher.txt",shell=True)
class Process(peewee.Model):
"""Program Starts"""

print "Program Started"
subprocesscalls()
array=[]
getProcesses(array)
print array
print len(array)
writeIntoDatabase(array)
