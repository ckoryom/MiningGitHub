#!/usr/bin/python

from array import *
from connection import Connection

import elementtree.ElementTree as ET
import json
import urllib2

connection = Connection()
connection.gitHubAccount = raw_input("Enter GitHub account:")
connection.gitHubRepository = raw_input("Enter GitHub repository:")
connection.token = raw_input("Enter Auth Token:")
connection.requestType("commits")
data = connection.getResponseJson()

for commit in data:
	#commitXML = ET.SubElement(root,"commit")
	#commitXML.set("sha",str(commit["sha"]))
	print(commit["sha"])

