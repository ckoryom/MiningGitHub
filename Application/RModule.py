'''
Created on May 6, 2014

@author: ckoryom
'''
import pyRserve
from datetime import datetime
from Model.parameters import Parameters

class RModule(object):
    
    issues = []
    connection = None
    parameters = Parameters()
    printResults = True
    plotResults = True
    
    def __init__(self):
        self.connection = pyRserve.connect()
        self.connection
        self.checkConnection(True)
    
    def disconnect(self):
        self.connection.close()
        self.connection
        self.checkConnection(True)
    
    def checkConnection(self, printStatus):
        if (self.connection.isClosed):
            if printStatus :
                print "Connection to R is Closed..."
            return False
        else:
            if printStatus :
                print "Connection to R is Opened..."
            return True
    
    def runCommand(self, command):
        if self.checkConnection(False):
            result = self.connection.eval(command)
            return result
    
    def calculateTimeToRepair(self, issue):
        time = self.calculateDates(issue["closed_at"], issue["created_at"])
        return time
    
    def secondsToHours(self, seconds):
        return seconds/3600
    
    def secondsToMinutes(self, seconds):
        return seconds/60
    
    def calculateDates(self, dateA, dateB):
        dateObjectA = datetime.strptime(dateA, "%Y-%m-%dT%H:%M:%SZ")
        dateObjectB = datetime.strptime(dateB, "%Y-%m-%dT%H:%M:%SZ")
        timeDelta = abs(dateObjectB - dateObjectA)
        if (self.parameters.values["timeFormat"] == "hours"):
            return self.secondsToHours(timeDelta.seconds)
        elif (self.parameters.values["timeFormat"] == "minutes"):
            return self.secondsToMinutes(timeDelta.seconds)
        elif (self.parameters.values["timeFormat"] == "days"):
            return timeDelta.days
        else:
            return timeDelta.hours
    
    def calculateArithmeticMean(self, vector):
        vectorCount = 0
        command = "vector <- c("
        for v in vector:
            if vectorCount == 0:
                command += str(v)
            else:
                command += "," + str(v)
            vectorCount += 1
        command += ")"
        self.runCommand(command)
        return float(self.runCommand("mean(vector)"))
    
    def plot(self, size):
        xCommand = "x <- c("
        for i in range(0,size):
            if (i==0):
                xCommand += str(i + 1)
            else:
                xCommand += "," + str(i)
        xCommand += ")"
        self.runCommand(xCommand)
        self.runCommand("plot(x,vector)")
        self.runCommand("myLine.fit <- lm(vector ~ x)")
        self.runCommand("abline(myLine.fit)")
        raw_input("plotting...")        
    
    def calculateMeanTimeToRepair(self,groups):
        itemCount = 0
        timeGroups = list()
        vector = list()
        issueCount = 0
        finish = False
        if (self.printResults):
            print "       Issue       ||       OpeningDate       ||       ClosingDate       ||       RepairTime("+self.parameters.values["timeFormat"]+")"
            print "--------------------------------------------------------------------------------------------"
        for issueList in self.issues:
            for issue in issueList:
                if (int(itemCount) >= int(groups)):
                    itemCount = 0
                    groupMean = self.calculateArithmeticMean(vector)
                    timeGroups.append(groupMean)
                    vector = list()
                timeToRepair = self.calculateTimeToRepair(issue)
                vector.append(timeToRepair)
                if (self.printResults):
                    print "       "+str(issue["number"])+"       ||       "+str(issue["created_at"])+"       ||       "+str(issue["closed_at"])+"       ||       "+str(timeToRepair)+""
                itemCount += 1
                issueCount += 1
                if (self.parameters.values["issuesLimit"] != None):
                    if (issueCount >= int(self.parameters.values["issuesLimit"])):
                        finish = True
                        break
            if(finish):
                break
        meanTimeToRepair = self.calculateArithmeticMean(timeGroups)
        if (self.printResults):
            print "--------------------------------------------------------------------------------------------"
            print "Item Count: " + str(len(timeGroups))
            print "Groups of: " + str(groups) + " -- MeanTimeToRepair: " + str(meanTimeToRepair)
        if (self.plotResults):
            self.plot(len(timeGroups))
        return meanTimeToRepair
    
    def calculateMeanTimeToFailure(self,groups):
        issueCount = 0
        itemCount = 0
        timeGroups = list()
        vector = list()
        previousIssue = None
        finish = False
        if (self.printResults):
            print "       Issue       ||       OpeningDate       ||       ClosingDate       ||       SystemStableTime("+self.parameters.values["timeFormat"]+")"
            print "--------------------------------------------------------------------------------------------"
        for issueList in self.issues:
            for issue in issueList:
                if (int(itemCount) >= int(groups)):
                    itemCount = 0
                    groupMean = self.calculateArithmeticMean(vector)
                    timeGroups.append(groupMean)
                    vector = list()
                if issueCount == 0:
                    stableTime = 0
                else:
                    stableTime = self.calculateDates(previousIssue["closed_at"], issue["created_at"])
                vector.append(stableTime)
                previousIssue = issue
                if (self.printResults):
                    print "       "+str(issue["number"])+"       ||       "+str(issue["created_at"])+"       ||       "+str(issue["closed_at"])+"       ||       "+str(stableTime)+""
                itemCount += 1
                issueCount += 1
                if (self.parameters.values["issuesLimit"] != None):
                    if (issueCount >= int(self.parameters.values["issuesLimit"])):
                        finish = True
                        break
            if(finish):
                break
        meanTimeToFailure = self.calculateArithmeticMean(timeGroups)
        if (self.printResults):
            print "--------------------------------------------------------------------------------------------"
            print "Item Count: " + str(len(timeGroups))
            print "Groups of: " + str(groups) + " -- MeanTimeToFailure: " + str(meanTimeToFailure)
        if (self.plotResults):
            self.plot(len(timeGroups))
        return meanTimeToFailure
    
    def calculateMeanTimeBetweenFailure(self,groups):
        issueCount = 0
        itemCount = 0
        timeGroups = list()
        vector = list()
        previousIssue = None
        finish = False
        if (self.printResults):
            print "       Issue       ||       OpeningDate       ||       ClosingDate       ||       TimeLastFailure("+self.parameters.values["timeFormat"]+")"
            print "--------------------------------------------------------------------------------------------"
        for issueList in self.issues:
            for issue in issueList:
                if (int(itemCount) >= int(groups)):
                    itemCount = 0
                    groupMean = self.calculateArithmeticMean(vector)
                    timeGroups.append(groupMean)
                    vector = list()
                if issueCount == 0:
                    failureTime = 0
                else:
                    failureTime = self.calculateDates(previousIssue["created_at"], issue["created_at"])
                vector.append(failureTime)
                previousIssue = issue
                if (self.printResults):
                    print "       "+str(issue["number"])+"       ||       "+str(issue["created_at"])+"       ||       "+str(issue["closed_at"])+"       ||       "+str(failureTime)+""
                itemCount += 1
                issueCount += 1
                if (self.parameters.values["issuesLimit"] != None):
                    if (issueCount >= int(self.parameters.values["issuesLimit"])):
                        finish = True
                        break
            if(finish):
                break
        meanTimeBetweenFailure = self.calculateArithmeticMean(timeGroups)
        if (self.printResults):
            print "--------------------------------------------------------------------------------------------"
            print "Item Count: " + str(len(timeGroups))
            print "Groups of: " + str(groups) + " -- MeanTimeBetweenFailure: " + str(meanTimeBetweenFailure)
        if (self.plotResults):
            self.plot(len(timeGroups))
        return meanTimeBetweenFailure
        