'''
Created on May 3, 2014

@author: ckoryom
'''

import elementtree.ElementTree as ET
import os

class DataTree(object):
    root = ""
    tree = ""
    def initiateTree(self, treeName):
        self.root = ET.Element(treeName)

    def addSubElement(self, elementFather, subElementName):
        if elementFather == self.root:
            return ET.SubElement(self.root, subElementName)
        else:
            return ET.SubElement(elementFather, subElementName)

    def defineTree(self):
        self.tree = ET.ElementTree(self.root)

    def saveTree(self, fileName):
        #currentPath = os.getcwd()
        os.chdir("..")
        path =  os.getcwd() + fileName
        os.chdir("Application/")
        self.tree.write(path)
        outFile = open(path, 'r')
        content = outFile.read()
        outFile.close()
        outFile = open(path, 'w')
        outFile.write("<?xml version=\"1.0\"?>\n")
        outFile.write("<?xml-stylesheet type=\"text/xsl\"href=\"test.xsl\"?>\n")
        outFile.write("<!DOCTYPE BobActivityLog SYSTEM \"test.dtd\">\n")
        outFile.write(content)
        outFile.close()