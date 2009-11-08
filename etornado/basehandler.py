# -*- coding: utf-8 -*-

import tornado.web
import tornado.database
import etornado.session
import functools
import re

class _BaseHandler(tornado.web.RequestHandler):
	function_list = []
	real_function_list = dict()

def template_method(method):
	@functools.wraps(method)
	def wrapper(self,*args,**kwargs):
		return method(self,*args,**kwargs)
	_BaseHandler.function_list.append(method.__name__)
	return wrapper

class BaseHandler(_BaseHandler):

	def __init__(self,application, request, transforms = None):
		tornado.web.RequestHandler.__init__(self,application,request,transforms);
		self.hostId = request.hostId
		self.hostName = request.hostName

		self.database = request.database
		self.session = etornado.session.EightSession(self)

	@template_method
	def user_data(self,what):
		if not self.get_current_user(): return None
		else:
			user_data = self.database.get("SELECT * FROM users INNER JOIN profile ON profile.users_id = users.users_id WHERE users.users_id = %s LIMIT 1",
							self.get_current_user(), use_cache = True, cache_time = 240
						)

			if user_data is not None: 
				try:
					data_map = {'displayname': 'profile_displayname', 'location': 'profile_location', 'image_url': 'profile_image_url', 'name' : 'users_name'}
					return user_data[data_map[what]]
				except: return None

			else: return None

	@template_method
	def user_logged(self):
		if not self.get_current_user(): return False
		return True

	def render(self,template_name, **kwargs):
		self.real_function_list = {}
		for k in self.function_list:
			if hasattr(self,k): self.real_function_list[k] = getattr(self, k)
		kwargs.update(self.real_function_list)
		return tornado.web.RequestHandler.render(self,template_name,**kwargs)

	def get_current_user(self):
		return self.session.get_value("uid")

	def get_user_locale(self):
		return None

	def e404(self):
		self.send_error(404)

	@template_method
	def niceurl(self,realstring, separator = 'dash',lowercase = False):
		str_orig = realstring

		if separator == 'dash': search, replace = '_','_'
		else: search, replace = '-','_'

		trans = { '&\#\d+?' : '', '&\S+?;' : '', '\s+' : replace, replace+'+': replace, replace+'$': replace, '^'+replace: replace, '\.+$' : ''}

		for k in trans: realstring  = re.sub(k,trans[k],realstring)

		if lowercase: realstring = realstring.lower()
		if len(realstring) == 0: return str_orig
		return realstring

	@template_method
	def cycle(self,opts):
		if not type(opts) == type([]): return ""

		if len(opts) <= 1: return opts[0]
		if not hasattr(self,'_cycle_last'):
			self._cycle_last = 0
			return opts[0]
		else:
			if len(opts) -1 == self._cycle_last:
				self._cycle_last = 0
				return opts[0]
			else:
				self._cycle_last += 1
				return opts[self._cycle_last]
