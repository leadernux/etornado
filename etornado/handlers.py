# -*- coding: utf-8 -*-

import sys
import os
import glob
import hashlib

def init_all(file_name):
	sys.path.append(os.path.dirname(file_name))
	sys.path.append(os.path.join(os.path.dirname(file_name),"handlers"))

import basehandler

class LoginHandler(basehandler.BaseHandler):
	def get(self):
		self.render("login.html")
	def post(self):
		if self.hostId:
			user_name, user_pass = self.get_argument("user_name"), self.get_argument("user_pass")

			sql = "SELECT * FROM users WHERE users_name = %s AND users_password = %s AND hosts_id = %s"

			tmp = self.database.get(
						sql,
						user_name,
						hashlib.md5(user_pass).hexdigest(),
						self.hostId
					)
			if tmp:
				self.session.set_value("uid",tmp.users_id)
				self.redirect('/')
			else:
				self.redirect('/login/nouser')
		else:
			self.redirect("/")

class LogoutHandler(basehandler.BaseHandler):
	def get(self):
		self.session.delete_session()
		self.redirect("/")

def get_handlers(file_name):
	myDir = os.path.join(os.path.dirname(file_name),"handlers")
	myModules = []

	myModules.append((r"/login",LoginHandler))
	myModules.append((r"/logout",LogoutHandler))

	for myFile in glob.glob(myDir+"/*handler.py"):
		moduleName = os.path.basename(myFile).split(".")[0]
		moduleObject = __import__(moduleName,fromlist = ["handlers"])
		myModules.append(moduleObject.getHandlerInfo())

	return myModules