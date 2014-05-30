#!/usr/bin/python
'''
Created on May 31, 2014

@author: ckoryom
'''
import csv
import os

class FileManager(object):

    def prepareData(self, data):
        list = [["openDate", "closingDate"]]
        for issues in data:
            for issue in issues:
                list.append([[issue["created_at"],issue["closed_at"]]])
        return list
    
    def writeToCsv(self, filename, data):
        data = self.prepareData(data)
        os.chdir("..")
        path =  os.getcwd() + filename
        os.chdir("Application/")
        with open(path, 'wb') as fp:
            a = csv.writer(fp, delimiter=',')
            a.writerows(data)
            
            