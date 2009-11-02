# -*- coding: utf-8 -*-

import eblog.BlogBaseHandler

import etornado.utils.etime

class PostsHandler(eblog.BlogBaseHandler.BlogBaseHandler):
	def get(self,post_id = False):
		if post_id:
			post = self.database.query("SELECT * FROM posts INNER JOIN users ON users.users_id = posts.users_id WHERE blog_id = %s AND posts.posts_id = %s", self.blog_info("blog_id"), post_id, use_cache = True)
			if len(post) == 0:
				self.e404()
			else:
				tags = self.database.query("SELECT tags.tags_id, tags.tags_name FROM posts \
					INNER JOIN posts_tags ON posts_tags.posts_id = posts.posts_id \
					INNER JOIN tags ON tags.tags_id = posts_tags.tags_id\
					WHERE posts.posts_id = %s AND posts.blog_id = %s\
				",post_id, self.blog_info("blog_id"), use_cache = True)

				comments = self.database.query("SELECT * FROM posts_comments \
					WHERE blog_id = %s AND posts_id = %s\
					ORDER BY comments_time\
				",self.blog_info("blog_id"),post_id, use_cache = True)

				self.render("post.html", post = post[0], tags = tags, comments = comments)

class PostCommentHandler(eblog.BlogBaseHandler.BlogBaseHandler):
	def post(self):
		args = self.request.arguments
		if args.has_key('posts_id') and args.has_key('display_name') and args.has_key('comment_text'):
			try:
				posts_id, display_name, comment_text = args['posts_id'][0],args['display_name'][0],args['comment_text'][0]
				sql = "INSERT INTO posts_comments \
					(`blog_id`, `posts_id`, `comments_author`, `comments_time`,`comments_text`)\
					VALUES(%s,%s,%s,%s,%s)"
				self.database.execute(sql,
					self.blog_info("blog_id"),
					posts_id,
					display_name,
					etornado.utils.etime.unixtime(),
					comment_text
				)

				sql = "UPDATE posts SET posts_comments = posts_comments + 1 WHERE blog_id = %s AND posts_id = %s"

				self.database.execute(sql,
					self.blog_info("blog_id"),
					posts_id
				)

			except:
				self.redirect('/')
			finally:
				self.redirect("/post/view/From-Comment/"+posts_id+"#comments")
		else:
			self.redirect('/')

def getHandlerInfo():
	return [
			(r"\/post\/view\/.*\/(.*)",PostsHandler),
			(r"\/post\/post-comment",PostCommentHandler)
		]
