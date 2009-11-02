# -*- coding: utf-8 -*-

__author__="otavio"
__date__ ="$01/11/2009 06:32:50$"

import eblog.BlogBaseHandler

class PagesHandler(eblog.BlogBaseHandler.BlogBaseHandler):
	def get(self,page_url):
		page = self.database.query(
			"SELECT * FROM pages WHERE blog_id = %s AND pages_url = %s",
			self.blog_info("blog_id"),
			page_url
		)
		if len(page) == 0:
			self.e404()
		else:
			self.render("page_view.html",page = page[0])

def getHandlerInfo():
	return [(r"\/pages\/(.*)",PagesHandler)]
