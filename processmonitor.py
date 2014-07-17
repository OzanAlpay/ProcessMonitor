#!/usr/bin/env python2.7
#First Please Read Readme
import time
from peewee import *
import subprocess
import sys
import hashlib
db = MySQLDatabase('ProcessMonitor',user='username',passwd='password')
db.connect()
db.set_autocommit(True)
class Process(Model):
	Processhashed = TextField()
	CPU = DecimalField()
	MEM = DecimalField()
	CMD = TextField()
	Time = DateTimeField()
	class Meta:
		database = db

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
def getLowerProcesses(array):
	filee = open("lower.txt","r+")
	for line in filee:
		if(type(stringtointeger(line)) is int):
			if(stringtointeger(line)>=1 and stringtointeger(line)<100):
				temp=stringtointeger(line)
				array.append(temp)
	return array
def getHigherProcesses(array):
	filee = open("higher.txt","r+")
	for line in filee:
		if(type(stringtointeger(line)) is int):
			if(stringtointeger(line)>=100 and stringtointeger(line)<99999):
				temp=stringtointeger(line)
				array.append(temp)
	return array
def getAllProcesses(array):
	getLowerProcesses(array)
	temparray=[]
	getHigherProcesses(temparray)
	for num in temparray:
		array.append(num)
	return array
def getCPU(processid):
	CPU=subprocess.Popen("ps -p "+str(processid)+" -o %cpu | tail -n 1 | cut -d ' ' -f 2",stdout=subprocess.PIPE,shell=True)
	return stringtofloat(CPU.stdout.read())
def getMEM(processid):
	MEM=subprocess.Popen("ps -p "+str(processid)+" -o %mem | tail -n 1 | cut -d ' ' -f 2",stdout=subprocess.PIPE,shell=True)
	return stringtofloat(MEM.stdout.read())
def getCMD(processid):
	CMD=subprocess.Popen("cat /proc/"+str(processid)+"/cmdline",stdout=subprocess.PIPE,shell=True)
	tempCMD=CMD.stdout.read()
	if tempCMD is False or tempCMD=='' :
		return False
	else :
		return tempCMD
def subprocessCalls():
	subprocess.call("ps aux | cut -d ' ' -f 9-10 | cat > lower.txt",shell=True)
	subprocess.call("ps aux | cut -d ' ' -f 5-8 | awk 'NF' | cut -c 1-6 | cat > higher.txt",shell=True)
def addtoDB(array):
	for process in array:
		if getCMD(process) is False :
			continue
		else:
			
			tempCPU = getCPU(process)
			tempMEM = getMEM(process)
			tempCMD = getCMD(process)
			hashed = hashlib.sha256(tempCMD)
			hashedCMD =hashed.hexdigest()
			now = time.strftime("%Y-%m-%d %H:%M:%S")
			tempprocess=Process(Processhashed=hashedCMD,CPU=tempCPU,MEM=tempMEM,CMD=tempCMD,Time=now)
			tempprocess.save()

subprocessCalls()
array=[]
getAllProcesses(array)
addtoDB(array)
