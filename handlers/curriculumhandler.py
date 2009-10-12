# -*- coding: utf-8 -*-

import etornado.basehandler

class CurriculumHandler(etornado.basehandler.BaseHandler):
	def get(self,userName = False):
		self.write(userName)

def getHandlerInfo():
	return (r"/curriculo/(.*)",CurriculumHandler)
