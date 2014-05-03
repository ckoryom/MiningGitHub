#!/usr/bin/python

from connection import Connection
from datatree import DataTree

class Mining:

	gitHubAccount = ""
	gitHubRepository = ""
	token = ""
	dataTree = ""
	
	def getProgressPercentage(self, currentCount, connection):
		totalItems = connection.perPage * connection.totalPages
		percent = (currentCount*100)/totalItems
		print(connection.type + ": " + str(currentCount) + " of " + str(totalItems) +  " - "  + str(percent) + "% of " + connection.type)
	
	def startMiningProcedure(self):
		self.gitHubAccount = raw_input("Enter GitHub account:")
		self.gitHubRepository = raw_input("Enter GitHub repository:")
		self.token = raw_input("Enter Auth Token:")
		self.dataTree = DataTree()
		self.dataTree.initiateTree("DataTree")
		self.mineIssues()
		self.dataTree.defineTree()
		self.dataTree.saveTree("/xml/" + self.gitHubRepository +".xml")

	def mineCommits(self, sha, issueElement):
		commitsConnection = Connection()
		commitsConnection.gitHubAccount = self.gitHubAccount
		commitsConnection.gitHubRepository = self.gitHubRepository
		commitsConnection.token = self.token
		commitsConnection.requestType("commits", sha, False)
		commit = commitsConnection.getResponseJson()
		commitElement = self.dataTree.addSubElement(issueElement, "commit")
		commitElement.set("sha", sha)
		try:
			commitElement.set("message", str(commit["commit"]["message"]))
			pass
		except Exception, e:
			print "Could not get Message from sha# " + str(sha)
		for file in commit["files"]:
			fileElement = self.dataTree.addSubElement(commitElement, "file")
			fileElement.set("filename", str(file["filename"]))
		self.dataTree.defineTree()
		self.dataTree.saveTree("/xml/" + self.gitHubRepository +".xml")
			
			
	def mineEvents(self, issue, issueElement):
		eventsConnection = Connection()
		eventsConnection.gitHubAccount = self.gitHubAccount
		eventsConnection.gitHubRepository = self.gitHubRepository
		eventsConnection.token = self.token
		eventsConnection.requestType("events", str(issue["number"]), False)
		events = eventsConnection.getResponseJson()
		count = 0
		for event in events:
			self.getProgressPercentage(count, eventsConnection)
			if str(str(event["commit_id"])) != "None":
				self.mineCommits(str(event["commit_id"]), issueElement)
			count += 1
				
	
	def mineIssues(self):
		issuesConnection = Connection()
		issuesConnection.gitHubAccount = self.gitHubAccount
		issuesConnection.gitHubRepository = self.gitHubRepository
		issuesConnection.token = self.token
		issuesConnection.requestType("issues", "", False)
		issues = issuesConnection.getResponseJson()
		count = 0
		for issue in issues:
			self.getProgressPercentage(count, issuesConnection)
			issueElement = self.dataTree.addSubElement(self.dataTree.root, "issue")
			issueElement.set("id", str(issue["number"]))
			issueElement.set("state", str(issue["state"]))
			try:
				issueElement.set("title", str(issue["title"]))
				pass
			except Exception, e:
				print "Could not get Title from Issue# " + str(issue["number"])
			self.mineEvents(issue, issueElement)
			count += 1
	
	
		
		
				