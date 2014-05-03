'''
Created on May 3, 2014

@author: ckoryom
'''
from GitHub.connection import Connection
from TreeBuilder.datatree import DataTree

class Mining(object):
    gitHubAccount = ""
    gitHubRepository = ""
    token = ""
    dataTree = ""
    
    def getProgressPercentage(self, currentCount, connection):
        currentCount += 1
        totalItems = connection.perPage * connection.totalPages
        percent = (currentCount*100)/totalItems
        print(connection.dataType + ": " + str(currentCount) + " of " + str(totalItems) +  " - "  + str(percent) + "% of " + connection.dataType)
    
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
        if commit != None:
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
        if events != None:
            for event in events:
                if str(str(event["commit_id"])) != "None":
                    self.mineCommits(str(event["commit_id"]), issueElement)
                count += 1
                
    
    def mineIssues(self):
        issuesConnection = Connection()
        issuesConnection.gitHubAccount = self.gitHubAccount
        issuesConnection.gitHubRepository = self.gitHubRepository
        issuesConnection.token = self.token
        
        count = 0
        finished = False
        while (finished == False):
            if (count == 0):
                issuesConnection.requestType("issues", "", False)
            elif count > 0:
                issuesConnection.requestType("issues", "", True)
            issues = issuesConnection.getResponseJson()
            if issues != None:
                for issue in issues:
                    self.getProgressPercentage(count, issuesConnection)
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
                    self.mineEvents(issue, issueElement)
                    count += 1
            if issuesConnection.currentPage == issuesConnection.totalPages:
                finished = True
        print "Finished with repository: " + self.gitHubAccount + "/" + self.gitHubRepository