#!/usr/bin/python

import urllib2
import json
from libxml2 import isDigit

class Connection:
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
	type = ""
	
	def constructUrl(self, type, data):
		url = ""
		url += self.apiUrl + "/repos/"
		url += self.gitHubAccount + "/" + self.gitHubRepository + "/"
		if type == "issues":
			url += type + "?state=" + self.issueState
		elif type == "events":
			url += "issues/" + data + "/" + type
		elif type == "commits":
			url += type + "/" + data
		url += "?page=" + str(self.page) + "&per_page=" + str(self.perPage)
		url += "&access_token=" + self.token
		self.url = url

	def getHeaderValue(self, headers, key):
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
				

	def requestType(self, type, data, next):
		if next == False:
			self.constructUrl(type, data)
		else:
			self.url = self.nextUrl
			self.currentPage += 1
		self.response = urllib2.urlopen(self.url)
		headers = self.response.info().items()
		self.nextUrl = self.getHeaderValue(headers,"link")
		self.type = type

	def getResponseJson(self):
		return json.load(self.response)




	