# -*- coding: utf-8 -*-

__author__="otavio"
__date__ ="$12/10/2009 11:13:55$"

try:
	import etornado.database
except: raise Exception("No etornado database module found")

class Model(object):
	table_name = "model"
	_last_where = ""

	def __init__(self):
		self.database = etornado.database.EightDatabaseHandler.instance()

	def insert(self,**kwargs):
		pass

	def update(self,**kwargs):
		pass

	def where(self,**kwargs):
		_last_where = "WHERE ";

		for k in kwargs:
			_last_where += "`%s` = %s AND" % (k,kwargs[k])

		self._last_where = _last_where[:-3]
