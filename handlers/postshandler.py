# -*- coding: utf-8 -*-

import eblog.BlogBaseHandler

class PostsHandler(eblog.BlogBaseHandler.BlogBaseHandler):
	def get(self,post_id = False):
		if post_id:
			post = self.database.query("SELECT * FROM posts INNER JOIN users ON users.users_id = posts.users_id WHERE blog_id = %s AND posts.posts_id = %s", self.blog_info("blog_id"), post_id, use_cache = True)

			self.render("post.html", post = post[0])

def getHandlerInfo():
	return [(r"/post/view/(.*)",PostsHandler)]
