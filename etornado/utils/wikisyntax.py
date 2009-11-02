# -*- coding: utf-8 -*-

import re
import os.path
import urllib2
import copy

OBJECT_TAGS = []

def register_tag(tag):
	global OBJECT_TAGS
	OBJECT_TAGS.append(tag)

class WikiObjectTag(object):
	page = None

	def __init__(self, page = None):
		self.page = page

	def get_expression(self):
		return re.compile(self._get_expression())

	def _get_expression(self):
		pass

	def parse(self,text):
		pass

class Bold(WikiObjectTag):
	def _get_expression(self):
		return "\*\*([^\*\*]*)\*\*"

	def parse(self,text):
		return "<b>"+text.group(1)+"</b>"

register_tag(Bold)

class Italic(WikiObjectTag):
	def _get_expression(self):
		return "//([^//]*)//"

	def parse(self,text):
		return "<i>"+text.group(1)+"</i>"

register_tag(Italic)

class Monospaced(WikiObjectTag):
	def _get_expression(self):
		return "''([^'']*)''"

	def parse(self,text):
		return "<code>"+text.group(1)+"</code>"

register_tag(Monospaced)

class Link(WikiObjectTag):
	def _get_expression(self):
		return "\[\[([^\]\]]*)\]\]"

	def parse(self,text):
		url, descr, namespace, page = self.parse_link(text.group(1))
		return "<a href=\"%s\">%s</a>" % (url, descr)

	def parse_link(self,link):
		href = ""
		desc = ""
		try: url, descr = link.split("|",2)
		except: url, descr = link, link

		if not url.startswith("http://") and not url.startswith("https://"):
			try:
				namespace, page = url.split(":",2)
				descr = url.split(":",2)[1]
			except: namespace, page = None, url
		else:
			namespace, page = None, url

		togo = ""
		if namespace is not None: togo += namespace+":"
		togo += url

		if not page.startswith("http://") and not page.startswith("https://"): href = os.path.join(self.page.link_baseurl,urllib2.quote(togo))
		else: href = page

		return (href,descr,namespace,page)

register_tag(Link)

class Img(WikiObjectTag):
	def _get_expression(self):
		return "\{\{([^\}\}]*)\}\}"

	def parse(self,text):
		url, descr, namespace, page = self.parse_link(text.group(1))
		return "<img src=\"%s\" alt=\"%s\" title=\"%s\"/>" % (url, descr, descr)

	def parse_link(self,link):
		href = ""
		desc = ""
		try: url, descr = link.split("|",2)
		except: url, descr = link, link

		if not url.startswith("http://") and not url.startswith("https://"):
			try:
				namespace, page = url.split(":",2)
				descr = url.split(":",2)[1]
			except: namespace, page = None, url
		else:
			namespace, page = None, url

		if not page.startswith("http://") and not page.startswith("https://"): href = os.path.join(self.page.image_baseurl,urllib2.quote(page))
		else: href = page

		return (href,descr,namespace,page)

register_tag(Img)

class Underline(WikiObjectTag):
	def _get_expression(self):
		return "__([^__]*)__"

	def parse(self,text):
		return "<u>"+text.group(1)+"</u>"

register_tag(Underline)

class Footnote(WikiObjectTag):
	def _get_expression(self):
		return "\(\(([^\)\)]*)\)\)"

	def parse(self,text):
		footnote_id = self.page.add_footnote(text.group(1))
		return "<sup><a href=\"#fnt_%s\" alt=\"%s\" title=\"%s\">%s)</a></sup>" % (footnote_id, text.group(1), text.group(1), footnote_id)

register_tag(Footnote)

class Strike(WikiObjectTag):
	def _get_expression(self):
		return "~~([^~~]*)~~"

	def parse(self,text):
		return "<strike>"+text.group(1)+"</strike>"

register_tag(Strike)

class H3(WikiObjectTag):
	def _get_expression(self):
		return "====([^====]*)===="

	def parse(self,text):
		self.page.add_section(text.group(1),3)
		return "<h3>"+text.group(1)+"</h3>"

register_tag(H3)

class H4(WikiObjectTag):
	def _get_expression(self):
		return "===([^===]*)==="

	def parse(self,text):
		self.page.add_section(text.group(1),4)
		return "<h4>"+text.group(1)+"</h4>"

register_tag(H4)

class H5(WikiObjectTag):
	def _get_expression(self):
		return "==([^==]*)=="

	def parse(self,text):
		self.page.add_section(text.group(1),5)
		return "<h5>"+text.group(1)+"</h5>"

register_tag(H5)

class NewLine(WikiObjectTag):
	def _get_expression(self):
		return "(.*)\n"

	def parse(self,text):
		return text.group(1)+"<br/>\n"

register_tag(NewLine)

class WikiPage(object):
	page_name = None
	link_baseurl = "/wiki/page"
	image_baseurl = "/static/wiki/images"
	footnote_list = []
	section_list = []

	def add_section(self,section, section_size):
		self.section_list.append((section,section_size))
		return len(self.section_list)

	def add_footnote(self,footnote):
		self.footnote_list.append(footnote)
		return len(self.footnote_list)

	def __init__(self, page_name = None):
		self.page_name = page_name
		self.init_tags()

	def init_tags(self):
		self._pre_formatter = []
		global OBJECT_TAGS
		for tag in OBJECT_TAGS:
			tag = tag(self)
			self._pre_formatter.append((tag.get_expression(),tag.parse))

	def render(self,text):
		for k in self._pre_formatter:
			text = k[0].sub(k[1], text)
		print(text)
		return text

	def render_context(self):
		obj = copy.deepcopy(self)
		return obj

	def render_file(self,fp = None):
		if type(fp) is type(None): return False

		if type(fp) is str:
			try: fp = open(fp,'r')
			except: return False
		#try:
			text = fp.read()
			fp.close()
			return self.render(text)
		#except:
		#	try: fp.close()
		#	except: pass
		#	return False

if __name__ == "__main__":
	import sys
	page = WikiPage("wikisyntax")
	rendered = page.render_file("wikisyntax.wiki")
	if len(sys.argv) > 1 and sys.argv[1] == "qt":
		from PyQt4.QtCore import *
		from PyQt4.QtGui import *
		from PyQt4.QtWebKit import *

		app = QApplication(sys.argv)
		app.connect(app,SIGNAL('lastWindowClosed()'),app.quit)

		mainWindow = QMainWindow()
		mainWindow.setMinimumSize(640,480)

		webView = QWebView(mainWindow)

		#Writes to a file
		try:
			fp = open("wikisyntax.html","w+")
			fp.write(rendered)
			fp.close()
		except:
			sys.exit()

		webView.setUrl(QUrl("wikisyntax.html"))
		mainWindow.setCentralWidget(webView)
		mainWindow.show()

		app.exec_()
