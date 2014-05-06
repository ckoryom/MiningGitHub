#!/usr/bin/python
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
        """
        Initiates the tree to construct
        """
        self.root = ET.Element(treeName)
        return self.root

    def addSubElement(self, elementFather, subElementName):
        """
        Adds a subelement to the tree
        """
        try:
            if elementFather == self.root:
                return ET.SubElement(self.root, subElementName)
            else:
                return ET.SubElement(elementFather, subElementName)
            pass
        except Exception, e:
            print str(e)
            print "There was an error adding a subElement"
            return None

    def defineTree(self):
        """
        Construct the definitive TREE
        """
        self.tree = ET.ElementTree(self.root)
        return self.tree

    def saveTree(self, fileName):
        """
        Save the tree into XML file
        """
        try:
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
            pass
            return outFile
        except Exception, e:
            print str(e)
            print "There was an error when trying to save the xml: " + fileName
            return None