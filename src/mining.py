#!/usr/bin/python

from connection import Connection
from datatree import DataTree

class Mining:

	gitHubAccount = ""
	gitHubRepository = ""
	token = ""
	dataTree = ""

	def startMiningProcedure(self):
		self.gitHubAccount = raw_input("Enter GitHub account:")
		self.gitHubRepository = raw_input("Enter GitHub repository:")
		self.token = raw_input("Enter Auth Token:")
		self.dataTree = DataTree()
		self.dataTree.initiateTree("DataTree")
		self.mineIssues()
		self.dataTree.defineTree()
		self.dataTree.saveTree("/xml/" + self.gitHubRepository +".xml")

	def mineIssues(self):
		issuesConnection = Connection()
		issuesConnection.gitHubAccount = self.gitHubAccount
		issuesConnection.gitHubRepository = self.gitHubRepository
		issuesConnection.token = self.token
		issuesConnection.requestType("issues",False)
		issues = issuesConnection.getResponseJson()
		for issue in issues:
			issueElement = self.dataTree.addSubElement(self.dataTree.root, "issue")
			issueElement.set("id", str(issue["number"]))
			issueElement.set("state", str(issue["state"]))
			try:
				issueElement.set("title", str(issue["title"]))
				pass
			except Exception, e:
				print "Could not get Titlte from Issue# " + str(issue["number"])
