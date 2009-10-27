# -*- coding: utf-8 -*-

__author__="root"
__date__ ="$16/10/2009 21:07:31$"

from etornado.multiapplication import MultiHostApplication

class BlogConfig(object):
	@classmethod
	def instance(cls):
		if not hasattr(cls,"_instance"):
			cls._instance = cls()
		return cls._instance

	def __init__(self):
		self.application = MultiHostApplication.instance()
		self.database = self.application.database

	def get_info(self,host_id = 0):
		if host_id == 0:
			return {
					"blog_id": 0,
					"blog_name": "Blog Default",
					"blog_title": "Blog Default",
					"blog_subtitle": "Just another blog...",
					"blog_copyright": "Another System",
					"blog_theme": "ormeggiare"
				}
		else:
			blog_info = self.database.query("SELECT * FROM blogs WHERE host_id = %s LIMIT 1",str(host_id),use_cache = True)
			if blog_info:
				blog_info = blog_info[0]
				return  {
						"blog_id": str(blog_info.blog_id),
						"blog_name": str(blog_info.blog_name),
						"blog_title": str(blog_info.blog_title),
						"blog_subtitle": str(blog_info.blog_subtitle),
						"blog_copyright": str(blog_info.blog_copyright),
						"blog_theme": str(blog_info.blog_theme)
					}
		return False

