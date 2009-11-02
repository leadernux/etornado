# -*- coding: utf-8 -*-

import re

class WikiSyntax(object):
	def __init__(self):
		BOLDITALIC_TOKEN = "'''''(.*)'''''"
		BOLD_TOKEN = "'''(.*)'''"
		ITALIC_TOKEN = "''(.*)''"
		UNDERLINE_TOKEN = "__(.*)__"
		STRIKE_TOKEN = "~~(.*)~~"

		self._pre_formatter = [
			(BOLDITALIC_TOKEN,self._bolditalic),
			(BOLD_TOKEN,self._bold),
			(ITALIC_TOKEN,self._italic),
			(STRIKE_TOKEN,self._strike)
		]

	def _bolditalic(self,text):
		pass

	def _bold(self,text):
		pass

	def _italic(self,text):
		pass

	def _strike(self,text):
		pass

	def render(self,text):
		for k in self._pre_formatter:
			
		return text

if __name__ == "__main__":
	test = WikiSyntax()
	print(test.render("~~Olá!~~"))