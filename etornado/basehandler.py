# -*- coding: utf-8 -*-

import tornado.web

import tornado.database

import etornado.session

class BaseHandler(tornado.web.RequestHandler):
	def __init__(self,application, request, transforms = None):
		tornado.web.RequestHandler.__init__(self,application,request,transforms);
		self.hostId = request.hostId
		self.hostName = request.hostName

		self.database = request.database
		self.session = etornado.session.EightSession(self)

		#Themes
		self.function_list = dict(
			theme_css=self.theme_css,
			user_displayname=self.user_displayname
		)

	@property
	def user_displayname(self):
		if not self.get_current_user():
			return "Convidado"
		else:
			return "Usuário!"

	def theme_css(self):
		return self.static_url("themes/adornment/style.css")

	def render(self,template_name, **kwargs):

		kwargs.update(self.function_list)

		return tornado.web.RequestHandler.render(self,template_name,**kwargs)

	def get_current_user(self):
		return self.session.get_value("uid")

	def get_user_locale(self):
		return None
