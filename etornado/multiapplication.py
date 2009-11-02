# -*- coding: utf-8 -*-

__author__="otavio"
__date__ ="$11/10/2009 13:22:45$"

from tornado.web import Application
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.locale import load_translations as locale_load_translations

#Handlers
import re
import os

from database import EightDatabaseHandler

class MultiHostApplication(Application):
	def __init__(self,handlers=None, default_host=[0,".*"], transforms=None,**settings):
		Application.__init__(self,handlers,default_host,transforms,**settings);

		if self.settings.get("multihost_db_host"):
			try:
				self.database = EightDatabaseHandler.instance(
							host=self.settings.get("multihost_db_host"),
							database=self.settings.get("multihost_db_name"),
							user=self.settings.get("multihost_db_user"),
							password = self.settings.get("multihost_db_password"),
							application = self,
							database_backend = self.settings.get("database_backend")
						);

				self.hosts = []
				for host in self.database.query("SELECT * FROM hosts"):
					self.hosts.append([host.id,host.hostname, re.compile(host.hostname)])
			except Exception, e: raise Exception("Cannot connect to database: "+str(e))
		else:
			self.database = False
			self.hosts = False

		self.default_host = default_host

	def __call__(self,request):
		host = request.host.lower().split(":")[0]
		if self.hosts:
			for hostname in self.hosts:
				if hostname[2].match(host):
					request.hostId = hostname[0]
					request.hostName = host
					break
				else:
					request.hostId = self.default_host[0]
					request.hostName = self.default_host[1]
		else:
			request.hostId = self.default_host[0]
			request.hostName = self.default_host[1]

		request.database = self.database

		Application.__call__(self,request)

	@classmethod
	def instance(cls,handlers=None, default_host=[0,".*"], transforms=None,**settings):

		if not hasattr(cls,"_instance"):
			cls._instance = cls(handlers, default_host, transforms,**settings)

		return cls._instance

	def start_server(self,file_name = None):
		if file_name is not None:
			if self.settings.get("use_locale"):
				locale_load_translations(os.path.join(os.path.dirname(file_name),"translations"))

			http_server = HTTPServer(self)

			if not self.settings.get("http_port"):
				http_server.listen(80)
			else:
				http_server.listen(self.settings.get("http_port"))

			IOLoop.instance().start()
