# -*- coding: utf-8 -*-

__author__="otavio"
__date__ ="$16/10/2009 21:34:03$"

from etornado.basehandler import BaseHandler

from eblog.BlogConfig import BlogConfig

import time

class BlogBaseHandler(BaseHandler):
	def __init__(self,application, request, transforms = None):
		BaseHandler.__init__(self,application, request, transforms)
		self.function_list.update(dict(
			blog_info = self.blog_info,
			theme_css=self.theme_css,
			gen_menu_items=self.gen_menu_items,
			timestamp_convert=self.timestamp_convert,
			word_wrap=self.word_wrap,
			render_content=self.render_content
		))

	def render_content(self,string):
		return "<br/>".join(string.split("\n"))

	def word_wrap(self,text,limit,suffix='...'):
		if len(text) <= limit:
			return text
		return text[:limit].rsplit(' ', 1)[0]+suffix

	def timestamp_convert(self,timestamp,format):
		return time.strftime(format,time.localtime(timestamp))

	def theme_css(self):
		return self.static_url("themes/"+self.blog_info("blog_theme")+"/style.css")

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

	def blog_info(self,key_name):
		blog_config = BlogConfig().instance().get_info(self.hostId)
		if not blog_config: return ""
		else:
			if blog_config.has_key(key_name):
				return blog_config[key_name]
			else: return ""
