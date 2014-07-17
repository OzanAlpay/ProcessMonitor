#!/usr/bin/env python
import sys
import os
import subprocess
import time
def stringtointeger ( x ):
	try :
		 return int(x)
	except ValueError:
		return x
def ifint ( x ) :
	if type(x) is int :
		return True
	else :	
		return False
def getlowerprocesses(array):
	filee=open("processes1.txt","r+")
	for line in filee:
		if(type(stringtointeger(line)) is int):
			if(stringtointeger(line)>=1 and stringtointeger(line)<=160):
				temp=stringtointeger(line)
				array.append(temp)
	filee.close()
	return array
def gethigherprocesses(array):
	filee=open("processes2.txt","r+")
	for line in filee:
		if(type(stringtointeger(line)) is int):
			if(stringtointeger(line)>160 and stringtointeger(line)<100000):
				temp=stringtointeger(line)
				array.append(temp)
	filee.close()
	return array
def getnumberofprocesses(array):
	getlowerprocesses(array)
	array2=[]
	gethigherprocesses(array2)
	for num in array2:
		array.append(num)
	return array
def comparetwolists(list1,list2,lastopened):
	print "List 1 Length : ",len(list1)
	print "List 2 Length : ",len(list2)
	for num in list1:
		if num not in list2:
			if num in lastopened:
				print "Last Closed Process ID : ",num
				print "Details : "
				print "Close Time :"
				print time.strftime("%c")
				print getprocessinfo(num)
				lastopened.remove(num)
				
	for num in list2:
		if num not in list1:
			if getinfo(num):
				print "Recent Started Process ID : ",num
				print "It's id is : ",num
				print "Details : "
				print getprocessinfo(num)
				print "Open Time : "
				print time.strftime("%c")
				lastopened.append(num)
				
				
def subprocesscalls ():
	subprocess.call("ps aux | cut -d ' ' -f 9-10 | cat > processes1.txt",shell = True)
	subprocess.call("ps aux | cut -d ' ' -f 5-8  | awk 'NF'|cut -c 1-6 | cat > processes2.txt",shell = True)
def getprocessinfo(processid):	
	print	subprocess.call("ps -p "+str(processid),shell=True)
def getinfo(processid):
	
	subprocess.call("ps -p "+str(processid)+" | tail -n 1 | cut -d ' ' -f 1 | cat > processinfo0.txt",shell=True)
	subprocess.call("ps -p "+str(processid)+" | tail -n 1 | cut -d ' ' -f 2 | cat > processinfo1.txt",shell=True)
	subprocess.call("ps -p "+str(processid)+" | tail -n 1 | cut -d ' ' -f 3 | cat > processinfo2.txt",shell=True)
	subprocess.call("ps -p "+str(processid)+" | tail -n 1 | cut -d ' ' -f 4 | cat > processinfo3.txt",shell=True)
	subprocess.call("ps -p "+str(processid)+" | tail -n 1 | cut -d ' ' -f 5 | cat > processinfo4.txt",shell=True)
	file0=open("processinfo0.txt","r+")
	file1=open("processinfo1.txt","r+")
	file2=open("processinfo2.txt","r+")
	file3=open("processinfo3.txt","r+")
	file4=open("processinfo4.txt","r+")
	info0=file0.readline()
	info1=file1.readline()
	info2=file2.readline()
	info3=file3.readline()
	info4=file4.readline()
	
	file0.close()
	file1.close()
	file2.close()
	file3.close()
	file4.close()
	if ifint(stringtointeger(info0)) or ifint(stringtointeger(info1)) or ifint(stringtointeger(info2)) or ifint(stringtointeger(info3)) :
		return True
	return False

""" Starts Here """
print "Program Started"
a=0
processes_last_opened=[]
processes_old=[]
subprocesscalls()
getnumberofprocesses(processes_old)
processes_present=[]
subprocesscalls()
getnumberofprocesses(processes_present)
print "Iteration : ",a
a=a+1
comparetwolists(processes_old,processes_present,processes_last_opened)
"""print "Unimportant Processes : ",unimportant_processes"""
while True:
	time.sleep(5)
	print "Iteration : ",a
	processes_old=[]
	processes_old=processes_present
	processes_present=[]
	subprocesscalls()
	getnumberofprocesses(processes_present)
	comparetwolists(processes_old,processes_present,processes_last_opened)
	print (len(processes_present) - len(processes_old) )
	
	a=a+1
