#!/usr/bin/python
'''
Created on May 3, 2014

@author: ckoryom
'''
from GitHub.connection import Connection
from TreeBuilder.datatree import DataTree
from Model.parameters import Parameters
from RModule import RModule

class Mining(object):
    gitHubAccount = ""
    gitHubRepository = ""
    token = ""
    dataTree = None
    parameters = Parameters()
    issues = list()
    menu = None
    
    def writeToTree (self):
        if (self.parameters.values["writeXML"]):
            if (self.dataTree is None):
                self.dataTree = DataTree()
                self.dataTree.initiateTree("DataTree")
            else:
                self.dataTree.defineTree()
                self.dataTree.saveTree("/xml/" + self.gitHubRepository +".xml")
    
    def getProgressPercentage(self, currentCount, connection):
        """
        Return the current progress of the desired connection class
        Normally we want to keep the progress status of the issues.
        Total Items is an aproximate, we multiply the items per page
        with the total number of pages
        """
        currentCount += 1
        totalItems = connection.perPage * connection.totalPages
        percent = (currentCount*100)/totalItems
        print(connection.dataType + ": " + str(currentCount) + " of " + str(totalItems) +  " - "  + str(percent) + "% of " + connection.dataType)
    
    def startMiningProcedure(self):
        """
        This calls the first mining functions for the issues and
        sets the GitHub account and repository to mine.
        """
        self.gitHubAccount = raw_input("Enter GitHub account:")
        self.gitHubRepository = raw_input("Enter GitHub repository:")
        self.token = raw_input("Enter Auth Token:")
        self.writeToTree()
        self.parameters.values["issuesLimit"] = raw_input("Number of Issues to mine:")
        self.issues = self.mineIssues()
        self.writeToTree()
        if (self.parameters.values["useR"]):
            rModule = RModule()
            rModule.issues = self.issues
            rModule.parameters = self.parameters
            self.menu.RMenu(rModule)
            
        
        

    def mineCommits(self, sha, issueElement):
        """
        Gets the commit JSON object from the RESTFUL GitHub API
        We pass the sha to look for and the issueElement to
        construct the XML tree
        """
        commitsConnection = Connection()
        commitsConnection.gitHubAccount = self.gitHubAccount
        commitsConnection.gitHubRepository = self.gitHubRepository
        commitsConnection.token = self.token
        commitsConnection.requestType("commits", sha, False)
        commit = commitsConnection.getResponseJson()
        if commit != None:
            if (self.parameters.values["writeXML"]):
                commitElement = self.dataTree.addSubElement(issueElement, "commit")
                commitElement.set("sha", sha)
                try:
                    commitElement.set("message", str(commit["commit"]["message"]))
                    pass
                except Exception, e:
                    print "Error:" + str(e)
                    print "Could not get Message from sha# " + str(sha)
                for commitFile in commit["files"]:
                    fileElement = self.dataTree.addSubElement(commitElement, "file")
                    fileElement.set("filename", str(commitFile["filename"]))
                self.writeToTree()
            
    def mineEvents(self, issue, issueElement):
        """
        Gets the events JSON object from the RESTFUL GitHub API
        We pass the issue number to look for and the issueElement to
        construct the XML tree.
        We only take care of events that have a commit_id
        """
        eventsConnection = Connection()
        eventsConnection.gitHubAccount = self.gitHubAccount
        eventsConnection.gitHubRepository = self.gitHubRepository
        eventsConnection.token = self.token
        eventsConnection.requestType("events", str(issue["number"]), False)
        events = eventsConnection.getResponseJson()
        count = 0
        if events != None:
            for event in events:
                if str(str(event["commit_id"])) != "None":
                    self.mineCommits(str(event["commit_id"]), issueElement)
                count += 1
                
    def mineIssues(self):
        """
        Gets the issues JSON object from the RESTFUL GitHub API
        Here we also construct the XML tree
        """
        issuesConnection = Connection()
        issuesConnection.gitHubAccount = self.gitHubAccount
        issuesConnection.gitHubRepository = self.gitHubRepository
        issuesConnection.token = self.token
        
        if (self.parameters.values["labels"] != None):
            issuesConnection.labels = self.parameters.values["labels"]
        nPlus = 0
        
        count = 0
        finished = False
        while (finished == False):
            if (count == 0):
                issuesConnection.requestType("issues", "", False)
            elif count > 0:
                issuesConnection.requestType("issues", "", True)
            issues = issuesConnection.getResponseJson()
            if issues != None:
                self.issues.append(issues)
                for issue in issues:
                    self.getProgressPercentage(count, issuesConnection)
                    issueElement = None
                    if (self.parameters.values["writeXML"]):
                        issueElement = self.dataTree.addSubElement(self.dataTree.root, "issue")
                        issueElement.set("id", str(issue["number"]))
                        issueElement.set("state", str(issue["state"]))
                        try:
                            issueElement.set("title", str(issue["title"]))
                            pass
                        except Exception, e:
                            print "Error:" + str(e)
                            print "Could not get Title from Issue# " + str(issue["number"])
                        labels = ""
                        labelCount = 0
                        for label in issue["labels"]:
                            if labelCount == 0:
                                labels += label["name"]
                            else:
                                labels += "," + label["name"]
                            labelCount += 1
                        issueElement.set("labels", labels)
                    if (self.parameters.values["mineCommits"]):
                        self.mineEvents(issue, issueElement)
                    count += 1
                    if (self.parameters.values["issuesLimit"] != None):
                        if (count + 2 >= int(self.parameters.values["issuesLimit"])):
                            finished = True
                            break
            if issuesConnection.currentPage == issuesConnection.totalPages:
                finished = True
            
        print "Finished with repository: " + self.gitHubAccount + "/" + self.gitHubRepository
        return self.issues