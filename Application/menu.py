'''
Created on May 6, 2014

@author: ckoryom
'''

from Application.mining import Mining
from Model.parameters import Parameters

class Menu(object):
    
    mining = Mining()
    
    def selectMenu (self):
        menuId = 0
        while (int(menuId) != 1 and int(menuId) != 2 and int(menuId) != 3):
            print "1) Mine Repository Data to XML"
            print "2) Mine Repository Data to R"
            print "3) Exit"
            menuId = raw_input("Selection:")
        if (int(menuId) == 1):
            self.mining.startMiningProcedure()
        elif (int(menuId) == 2):
            print "Using R Module..."
            parameters = Parameters()
            parameters.values["mineCommits"] = False
            parameters.values["writeXML"] = False
            parameters.values["useR"] = True
            parameters.values["issuesLimit"] = 10
            parameters.values["labels"] = "bug"
            self.mining.menu = self 
            self.mining.parameters = parameters
            self.mining.startMiningProcedure()
        elif (int(menuId) == 3):
            return ""
    
    def groupOption(self):
        print "Group data size:"
        size = raw_input("size:")
        return size
    
    def RMenu(self, rModule):
        menuId = 0
        while (int(menuId) != 1 and int(menuId) != 2 and int(menuId) != 3 and int(menuId) != 4):
            print "1) Get MTTR"
            print "2) Get MTTF"
            print "3) Get MTBF"
            print "4) Get ALL"
            menuId = raw_input("Selection:")
        if (int(menuId) == 1):
            rModule.calculateMeanTimeToRepair(self.groupOption())
        elif (int(menuId) == 2):
            rModule.calculateMeanTimeToFailure(self.groupOption())
        elif (int(menuId) == 3):
            rModule.calculateMeanTimeBetweenFailure(self.groupOption())
        elif (int(menuId) == 4):
            untouchedModule = rModule
            MTBF = rModule.calculateMeanTimeBetweenFailure(self.groupOption())
            rModule = untouchedModule
            MTTR = rModule.calculateMeanTimeToRepair(self.groupOption())
            rModule = untouchedModule
            MTTF = rModule.calculateMeanTimeToFailure(self.groupOption())
            availability = rModule.calculateAvailability(MTBF, MTTR)
        
        