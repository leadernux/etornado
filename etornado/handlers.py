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

from tornado.web import asynchronous as tornado_asynchnous

try:
	from tornado.auth import TwitterMixin as TornadoTwitterMixin
	from etornado.profile import Profile

	class TwitterLoginHandler(basehandler.BaseHandler, TornadoTwitterMixin):
		@tornado_asynchnous
		def get(self):
			if self.get_argument("oauth_token",None):
				self.get_authenticated_user(self.async_callback(self._on_auth))
				return
			self.authorize_redirect()

		def _on_auth(self,user):
			if not user:
				self.redirect('/login/nouser')
			else:
				user_id = 'twitter-'+str(user["id"])
				user_fields = {
						"profile_displayname" : user['name'],
						"profile_location" : user['location'],
						"profile_image_url" : user['profile_image_url'],
						"user_name" : user['username']
					}

				self.session.set_value("uid",user_id)

				profile = Profile()
				if profile.login(user_id,user_fields): self.redirect('/')
				else: self.redirect('/login/nouser')
except:
	class FailLoginHandler(basehandler.BaseHandler):
		def get(self):
			self.write("Missing pyCurl")

	class TwitterLoginHandler(FailLoginHandler):
		pass

class LogoutHandler(basehandler.BaseHandler):
	def get(self):
		self.session.delete_session()
		self.redirect("/")

def get_handlers(file_name):
	myDir = os.path.join(os.path.dirname(file_name),"handlers")
	myModules = []

	myModules.append((r"/login",LoginHandler))
	myModules.append((r"/login-twitter",TwitterLoginHandler))
	myModules.append((r"/logout",LogoutHandler))

	for myFile in glob.glob(myDir+"/*handler.py"):
		moduleName = os.path.basename(myFile).split(".")[0]
		moduleObject = __import__(moduleName,fromlist = ["handlers"])
		tmp = moduleObject.getHandlerInfo()
		if type(tmp) == type([]):
			for i in tmp: myModules.append(i)
		else: myModules.append(tmp)

	return myModules