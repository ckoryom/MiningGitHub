'''
Created on May 6, 2014

@author: ckoryom
'''
from __future__ import division
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
    
    def writeToFile(self, data, fileName):
        f = open(fileName, "w")
    
    def secondsToMinutes(self, seconds):
        return seconds/60
    
    def daysToHours(self, days):
        return days*24
    
    def hoursToDays(self, hours):
        return hours/24
    
    def calculateDates(self, dateA, dateB):
        dateObjectA = datetime.strptime(dateA, "%Y-%m-%dT%H:%M:%SZ")
        dateObjectB = datetime.strptime(dateB, "%Y-%m-%dT%H:%M:%SZ")
        timeDelta = abs(dateObjectB - dateObjectA)
        if (self.parameters.values["timeFormat"] == "hours"):
            days = timeDelta.days
            daysHours = self.daysToHours(days)
            hours = self.secondsToHours(timeDelta.seconds)
            hours += daysHours
            return hours
        elif (self.parameters.values["timeFormat"] == "minutes"):
            return self.secondsToMinutes(timeDelta.seconds)
        elif (self.parameters.values["timeFormat"] == "days"):
            hours = self.secondsToHours(timeDelta.seconds)
            daysFromHours = self.hoursToDays(hours)
            days = timeDelta.days + daysFromHours
            return days
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
    
    def calculateYValue (self, slope, intercept, xValue):
        y = float(slope)*float(xValue) + float(intercept)
        return y
    
    def cleanData(self,data):
        data = data.replace(" ", "")
        data = data.replace("[", "")
        data = data.replace("]", "")
        return data
    
    def plot(self, size):
        xCommand = "x <- c("
        for i in range(0,size):
            if (i==0):
                xCommand += str(i + 1)
            else:
                xCommand += "," + str(i)
        xCommand += ")"
        self.runCommand(xCommand)
        self.runCommand("plot(x,vector,main=)")
        self.runCommand("myLine.fit <- lm(vector ~ x)")
        self.runCommand("abline(myLine.fit)")
        rsquared = self.runCommand("summary(myLine.fit)$r.squared")
        coefficient = self.runCommand("coef(myLine.fit)[1]")
        coefficient = self.cleanData(str(coefficient))
        intercept = self.runCommand("coef(myLine.fit)[1]")
        intercept = self.cleanData(str(intercept))
        slope = self.runCommand("coef(myLine.fit)[2]")
        slope = self.cleanData(str(slope))
        print "r-Squared = " + str(rsquared)
        print "Coefficient = " + str(coefficient)
        print "Intercept = " + str(intercept)
        print "Slope = " + str(slope)
        predictedNPlus = self.calculateYValue(slope,intercept,int(self.parameters.values["calculateNextN"]))
        print "Predicted n + " + str(int(self.parameters.values["calculateNextN"])) + " = " + str(predictedNPlus)
        raw_input("plotting...")        
    
    
    def makeGroups (self,issues,groups,type, nPlus):
        itemCount = 0
        group = list()
        groupMean = 0
        timeGroups = list()
        previousIssue = None
        finish = False
        findNPlus = False
        nPlusFound = False
        iOld = 0
        nPlusCounter = 0
        for issueList in issues:
            counter = 0
            for issue in issueList:
                if itemCount == 0 and type == "MTTF":
                    firstIssue = issue
                if (group != None and len(group)== int(groups)):
                    groupMean = self.calculateArithmeticMean(group)
                    timeGroups.append(groupMean)
                    group = list()
                groupCounter = 0
                for i in range(counter, counter + int(groups)):
                    if (i < len(issueList) ):
                        time = 0
                        if type == "MTTR":
                            time = self.calculateTimeToRepair(issueList[i])
                            time = int(time * 100) / 100.00
                            if findNPlus == False:
                                group.append(time)
                        elif type == "MTBF":
                            if previousIssue != None:
                                time = self.calculateDates(previousIssue["created_at"], issueList[i]["created_at"])
                                time = int(time * 100) / 100.00
                            else:
                                time = 0
                            if findNPlus == False:
                                group.append(time)
                            previousIssue = issue
                        elif type == "MTTF":
                            if firstIssue != None:
                                time = self.calculateDates(firstIssue["created_at"], issueList[i]["created_at"])
                                time = int(time * 100) / 100.00
                            else:
                                time = 0
                            if findNPlus == False:
                                group.append(time)
                                
                        if groupCounter == 0:
                            iOld = i
                            if (self.printResults and findNPlus == False):
                                print "       "+str(issueList[i]["number"])+"       ||       "+str(issueList[i]["created_at"])+"       ||       "+str(issueList[i]["closed_at"])+"       ||       "+str(time)+""
                        groupCounter += 1
                    if findNPlus:
                        if nPlusCounter < int(nPlus):
                            nPlusIssue = issueList[i]
                            nPlusTime = time
                        nPlusCounter += 1
                counter += 1
                itemCount += 1
                if itemCount == int(self.parameters.values["issuesLimit"]) + int(nPlus):
                    if (self.printResults):
                        print "N+" + str(nPlus) + "       "+str(nPlusIssue["number"])+"       ||       "+str(nPlusIssue["created_at"])+"       ||       "+str(nPlusIssue["closed_at"])+"       ||       "+str(nPlusTime)+""
                    nPlus = time
                    nPlusFound = True
                    
                if nPlusFound :
                    finish = True
                    break
                if (self.parameters.values["issuesLimit"] != None):
                    if (itemCount >= int(self.parameters.values["issuesLimit"])):
                        findNPlus = True
            if finish:
                break
        return timeGroups
                
    def calculateAvailability(self, MTBF, MTTR):
        availability = MTBF / (MTBF + MTTR)
        if (self.printResults):
            print "Availability = " + str(availability)
        return availability
    
    def calculateMeanTimeToRepair(self,groups): 
        if (self.printResults):
            print "       Issue       ||       OpeningDate       ||       ClosingDate       ||       Time("+self.parameters.values["timeFormat"]+")"
            print "--------------------------------------------------------------------------------------------"
        timeGroups = self.makeGroups(self.issues, groups, "MTTR", int(self.parameters.values["calculateNextN"]))
        mean = self.calculateArithmeticMean(timeGroups)
        if (self.printResults):
            print "--------------------------------------------------------------------------------------------"
            print "Item Count: " + str(len(timeGroups) + 1)
            print "Groups of: " + str(groups) + " -- MTTR: " + str(mean)
        if (self.plotResults):
            self.plot(len(timeGroups))
        return mean
    
    def calculateMeanTimeToFailure(self,groups): 
        if (self.printResults):
            print "       Issue       ||       OpeningDate       ||       ClosingDate       ||       Time("+self.parameters.values["timeFormat"]+")"
            print "--------------------------------------------------------------------------------------------"
        timeGroups = self.makeGroups(self.issues, groups, "MTTF", int(self.parameters.values["calculateNextN"]))
        mean = self.calculateArithmeticMean(timeGroups)
        if (self.printResults):
            print "--------------------------------------------------------------------------------------------"
            print "Item Count: " + str(len(timeGroups) + 1)
            print "Groups of: " + str(groups) + " -- MTTF: " + str(mean)
        if (self.plotResults):
            self.plot(len(timeGroups))
        return mean
    
    def calculateMeanTimeToFailureOld(self,groups):
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
            print "Item Count: " + str(len(timeGroups) + 1)
            print "Groups of: " + str(groups) + " -- MeanTimeToFailure: " + str(meanTimeToFailure)
        if (self.plotResults):
            self.plot(len(timeGroups))
        return meanTimeToFailure
    
    def calculateMeanTimeBetweenFailure(self,groups):
        if (self.printResults):
            print "       Issue       ||       OpeningDate       ||       ClosingDate       ||       Time("+self.parameters.values["timeFormat"]+")"
            print "--------------------------------------------------------------------------------------------"
        timeGroups = self.makeGroups(self.issues, groups, "MTBF", int(self.parameters.values["calculateNextN"]))
        mean = self.calculateArithmeticMean(timeGroups)
        if (self.printResults):
            print "--------------------------------------------------------------------------------------------"
            print "Item Count: " + str(len(timeGroups) + 1)
            print "Groups of: " + str(groups) + " -- MTBF: " + str(mean)
        if (self.plotResults):
            self.plot(len(timeGroups))
        return mean
        