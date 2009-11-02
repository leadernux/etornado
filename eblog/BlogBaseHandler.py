# -*- coding: utf-8 -*-

__author__="otavio"
__date__ ="$16/10/2009 21:34:03$"

from etornado.basehandler import BaseHandler, template_method

from eblog.BlogConfig import BlogConfig

import time

class BlogBaseHandler(BaseHandler):
	def __init__(self,application, request, transforms = None):
		BaseHandler.__init__(self,application, request, transforms)

	@template_method
	def render_content(self,string):
		return "<br/>".join(string.split("\n"))

	@template_method
	def word_wrap(self,text,limit,suffix='...'):
		if len(text) <= limit:
			return text
		return text[:limit].rsplit(' ', 1)[0]+suffix

	@template_method
	def timestamp_convert(self,timestamp,format):
		return time.strftime(format,time.localtime(timestamp))

	@template_method
	def theme_css(self):
		return self.static_url("themes/"+self.blog_info("blog_theme")+"/style.css")

	@template_method
	def gen_menu_items(self):
		_menuItems = self.database.query("SELECT * FROM links WHERE blogs_id = %s ORDER BY links_weight", self.blog_info("blog_id"), use_cache = True)

		if not _menuItems:
			menuItems = [("Inicio","/")]
		else:
			menuItems = []
			for _menuItem in _menuItems: menuItems.append((str(_menuItem.links_name),str(_menuItem.links_url)))

		html = "";
		for menuItem in menuItems:
			html += "<li><a href=\"%s\">%s</a></li>" % (menuItem[1],menuItem[0])

		return html;

	@template_method
	def blog_info(self,key_name):
		blog_config = BlogConfig().instance().get_info(self.hostId)
		if not blog_config: return ""
		else:
			if blog_config.has_key(key_name):
				return blog_config[key_name]
			else: return ""