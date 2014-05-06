'''
Created on May 4, 2014

@author: ckoryom
'''
import unittest
import os
from TreeBuilder.datatree import DataTree

class DataTreeTest(unittest.TestCase):

    dataTree = None
    treeName = None
    fileName = None
    subElementName = None

    def setUp(self):
        self.dataTree = DataTree()
        self.treeName = "TestTree"
        self.subElementName = "testSubElement"
        self.fileName = "/xml/test.xml"

    def testInitiateTree(self):
        self.assertIsNotNone(self.dataTree.initiateTree(self.treeName), "Data Tree returned None")
    
    def testAddSubElement(self):
        self.dataTree.initiateTree(self.treeName)
        root = self.dataTree.root
        self.assertIsNotNone(self.dataTree.addSubElement(root, self.subElementName), "Data Tree returned None")
    
    def testSaveTree(self):
        os.chdir("..")
        backDirectory = list(str(self.fileName))
        backDirectory[0] = ""
        backDirectory = "".join(backDirectory)
        if os.path.isfile(backDirectory):
            os.remove(backDirectory)
        os.chdir("tests/")
        self.dataTree.initiateTree(self.treeName)
        root = self.dataTree.root
        self.dataTree.addSubElement(root, self.subElementName)
        self.dataTree.defineTree()
        self.assertIsNotNone(self.dataTree.saveTree(self.fileName), "Saving Tree Returned NONE")
        os.chdir("..")
        self.assertTrue(os.path.isfile(backDirectory), "The xml file was not saved succesfully")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()