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

    def addSubElement(self, elementFather, subElementName):
        """
        Adds a subelement to the tree
        """
        if elementFather == self.root:
            return ET.SubElement(self.root, subElementName)
        else:
            return ET.SubElement(elementFather, subElementName)

    def defineTree(self):
        """
        Construct the definitive TREE
        """
        self.tree = ET.ElementTree(self.root)

    def saveTree(self, fileName):
        """
        Save the tree into XML file
        """
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