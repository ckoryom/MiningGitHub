#!/usr/bin/python
'''
Created on May 3, 2014

@author: ckoryom
'''

import urllib2
import json

class Connection(object):
    apiUrl = "https://api.github.com"
    url = ""
    nextUrl = ""
    page = 1
    perPage = 100
    token = ""
    gitHubAccount = ""
    gitHubRepository = ""
    response = ""
    issueState = "closed"
    totalPages = 1
    currentPage = 1
    nextPage = 2
    dataType = ""
    
    def constructUrl(self, dataType, data):
        """
        Constructs the URL of the GitHub RESTFULL API
        """
        url = ""
        url += self.apiUrl + "/repos/"
        url += self.gitHubAccount + "/" + self.gitHubRepository + "/"
        if dataType == "issues":
            url += dataType + "?state=" + self.issueState
        elif dataType == "events":
            url += "issues/" + data + "/" + dataType
        elif dataType == "commits":
            url += dataType + "/" + data
        url += "?page=" + str(self.page) + "&per_page=" + str(self.perPage)
        url += "&access_token=" + self.token
        self.url = url

    def getHeaderValue(self, headers, key):
        """
        Gets the desired header object from the response.
        Also gets the NextUrl and LastUrl for the pagination
        """
        for item in headers:
            item = str(item)
            item = item.replace("(","")
            item = item.replace(")","")
            item = item.split(",")
            if str(item[0]) == "'" + key + "'":
                if key == "link":
                    values = str(item[1]).split(";")
                    link = str(values[0]).replace("'","")
                    link = link.replace("<","")
                    link = link.replace(">","")
                    link = link.replace(" ","")
                    result = link.find("&page=")
                    if result >= 0:
                        nextPage = ""
                        for i in range(result, len(link)):
                            if link[i].isdigit():
                                nextPage += link[i]
                        self.nextPage = int(nextPage)
                    values = str(item[2]).split(";")
                    linkLastPage = str(values[0]).replace("'","")
                    linkLastPage = linkLastPage.replace("<","")
                    linkLastPage = linkLastPage.replace(">","")
                    linkLastPage = linkLastPage.replace(" ","")
                    lastPage = linkLastPage.find("&page=")
                    if lastPage >= 0:
                        totalPages = ""
                        for i in range(lastPage, len(linkLastPage)):
                            if linkLastPage[i].isdigit():
                                totalPages += linkLastPage[i]
                        self.totalPages = int(totalPages)
                    return link
                

    def requestType(self, dataType, data, nextPage):
        """
        Connects to the GitHub RESTFUL API and gathers
        the response object
        """
        if nextPage == False:
            self.constructUrl(dataType, data)
        else:
            self.url = self.nextUrl
            self.currentPage += 1
        try:
            self.response = urllib2.urlopen(self.url)
            pass
            headers = self.response.info().items()
            self.nextUrl = self.getHeaderValue(headers,"link")
            self.dataType = dataType
        except Exception, e:
            print("Error found: " + str(e))
            print("There was a problem trying to gather data from: " + self.url)
            self.response = None

    def getResponseJson(self):
        """
        Converts Response object into JSON
        """
        if self.response != None:
            return json.load(self.response)
        else:
            return None
        
        