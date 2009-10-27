# -*- coding: utf-8 -*-

import eblog.BlogBaseHandler

class MainHandler(eblog.BlogBaseHandler.BlogBaseHandler):
	def get(self):
		posts = self.database.query("SELECT * FROM posts INNER JOIN users ON users.users_id = posts.users_id WHERE blog_id = %s ORDER BY posts_time", self.blog_info("blog_id"), use_cache = True)

		self.render("main.html", posts = posts)

def getHandlerInfo():
	return (r"/",MainHandler)
