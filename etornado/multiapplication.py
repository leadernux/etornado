# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="root"
__date__ ="$11/10/2009 13:22:45$"

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.locale

#Handlers
import re
import os

from database import EightDatabaseHandler
from session import EightSession

class MultiHostApplication(tornado.web.Application):
	def __init__(self,handlers=None, default_host="", transforms=None,**settings):
		tornado.web.Application.__init__(self,handlers,default_host,transforms,**settings);

		if self.settings.get("use_multihost"):
			if self.settings.get("multihost_db_host"):

				self.database = EightDatabaseHandler.instance(
							host=self.settings.get("multihost_db_host"),
							database=self.settings.get("multihost_db_name"),
							user=self.settings.get("multihost_db_user"),
							password = self.settings.get("multihost_db_password"),
							application = self
						);

				self.hosts = []
				for host in self.database.query("SELECT * FROM hosts"):
					self.hosts.append([host.id,host.hostname])
			else:
				self.database = False
				self.hosts = False
		else:
			self.database = False
			self.hosts = False

	def __call__(self,request):
		host = request.host.lower().split(":")[0]
		if self.hosts:
			for hostname in self.hosts:
				if re.match(hostname[1],host):
					request.hostId = hostname[0]
					request.hostName = host
					break
				else:
					request.hostId = False
					request.hostName = False
		else:
			request.hostId = False
			request.hostName = False

		request.database = self.database

		tornado.web.Application.__call__(self,request)

	@classmethod
	def instance(cls,handlers=None, default_host="", transforms=None,**settings):

		if not hasattr(cls,"_instance"):
			cls._instance = cls(handlers, default_host, transforms,**settings)

		return cls._instance

	def start_server(self,file_name = None):
		if file_name is not None:
			if self.settings.get("use_locale"):
				tornado.locale.load_translations(os.path.join(os.path.dirname(file_name),"translations"))

			http_server = tornado.httpserver.HTTPServer(self)

			if not self.settings.get("http_port"):
				http_server.listen(80)
			else:
				http_server.listen(self.settings.get("http_port"))

			tornado.ioloop.IOLoop.instance().start()
