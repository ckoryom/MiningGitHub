#!/usr/bin/python

import urllib2
import json

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
	def constructUrl(self, type):
		url = ""
		url += self.apiUrl + "/repos/"
		url += self.gitHubAccount + "/" + self.gitHubRepository + "/"
		url += type + "?page=" + str(self.page) + "&per_page=" + str(self.perPage)
		url += "&auth_token=" + self.token
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
					return link

	def requestType(self, type):
		self.constructUrl(type)
		self.response = urllib2.urlopen(self.url)
		headers = self.response.info().items()
		self.nextUrl = self.getHeaderValue(headers,"link")

	def getResponseJson(self):
		return json.load(self.response)




	