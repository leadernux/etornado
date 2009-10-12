# -*- coding: utf-8 -*-

import etornado.basehandler

class MainHandler(etornado.basehandler.BaseHandler):
	def get(self):
		self.render("main.html")

def getHandlerInfo():
	return (r"/",MainHandler)
