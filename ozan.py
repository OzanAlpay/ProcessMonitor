#!/usr/bin/env python


import subprocess
import time
import _mysql
import MySQLdb
import peewee
class Process(Model):
	Process_ID = CharField()
	CPU = DecimalField()
	MEM = DecimalField()
	CMD = CharField()
	Time = DateTimeField()
	
	
