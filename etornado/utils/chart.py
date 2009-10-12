# -*- coding: utf-8 -*-

__author__="otavio"
__date__ ="$12/10/2009 11:42:27$"

import urllib2

class ChartLegendPosition(object):
	TOP = 't'
	LEFT = 'l'
	RIGHT = 'r'
	BOTTOM = 'b'

class BaseChart(object):
	url_base = "http://chart.apis.google.com/chart?"
	chart_type = "p3"
	chart_labels = []
	chart_data = []
	chart_size = [200,100]
	chart_colors = []
	chart_title = None
	chart_legends = []
	chart_legends_pos = ChartLegendPosition.BOTTOM

	def __init__(self, chart_type = None):
		if chart_type: self.chart_type = chart_type

	def set_chart_size(self,w = 200,h = 100):
		if w*h <= 300000: self.chart_size = [w,h]
		else: raise Exception("Width larger than 300.000 pixels")

	def set_chart_labels(self,labels = []):
		self.chart_labels = labels

	def set_chart_data(self,data = []):
		self.chart_data = data

	def set_chart_colors(self,colors = []):
		self.chart_colors = colors

	def set_chart_title(self,chart_title = None):
		self.chart_title = chart_title

	def set_chart_legends(self,chart_legends = []):
		self.chart_legends = chart_legends

	def set_chart_legends_pos(self,chart_legends_pos = ChartLegendPosition.BOTTOM):
		self.chart_legends_pos = chart_legends_pos

	def make_url(self):
		url = self.url_base

		url += "cht=%s&chs=%sx%s" % (self.chart_type,self.chart_size[0],self.chart_size[1])

		if len(self.chart_labels) > 0:
			url += "&chl="
			for label in self.chart_labels:
				url += urllib2.quote(label) + "|"

			url = url[:-1]

		if len(self.chart_data) > 0:
			url += "&chd=t:"
			for data in self.chart_data:
				if type(data) == type([]):
					url += urllib2.quote(",".join(data)) + "|"
				else:
					url += str(data) + ","
			url = url[:-1]

		if len(self.chart_colors) > 0:
			url += "&chco="+urllib2.quote(",".join(self.chart_colors))

		if self.chart_title:
			url += "&chtt="+urllib2.quote(self.chart_title)

		if len(self.chart_legends) > 0:
			url += "&chdl="+urllib2.quote("|".join(self.chart_legends))
			if self.chart_legends_pos:
				url += "&chdlp="+self.chart_legends_pos

		return url

	def __str__(self):
		return self.make_url()

class Pie3D(BaseChart):
	def __init__(self):
		BaseChart.__init__(self,chart_type = 'p3')

class Pie(BaseChart):
	def __init__(self):
		BaseChart.__init__(self,chart_type = 'p')

class Venn(BaseChart):
	def __init__(self):
		BaseChart.__init__(self,chart_type = 'v')

	"""
	1 - A relative size
	2 - B relative size
	2 - C relative size
	"""
	def set_venn_data(self, values = []):
		self.set_chart_data()
		self.chart_data.extend(values)

	"""
	1 - A-B intersect value
	2 - A-C intersect value
	3 - B-C intersect value
	"""
	def set_venn_intersect(self,values = []):
		self.chart_data.extend(values)

	"""
	A-B-C intersect value
	"""
	def set_venn_geral_intersect(self,value = 0):
		self.chart_data.extend([value])

class Dispersion(BaseChart):
	def __init__(self):
		BaseChart.__init__(self,chart_type = 's')

	"""
	values ->
		list(
			tuple(x, y)
		)
	"""
	def set_dispersion_data(self, values = [('x','y')]):
		x = []
		y = []
		for k in values:
			x.extend([k[0]])
			y.extend([k[1]])
		self.set_chart_data([x,y])

class Radar(BaseChart):
	def __init__(self):
		BaseChart.__init__(self, chart_type = 'r')


class GoogleOMeter(BaseChart):
	def __init__(self):
		BaseChart.__init__(self, chart_type = 'gom')

	def set_gom_data(self, value):
		self.set_chart_data([value])


class Qr(BaseChart):
	chart_qr_text = 'EightSystems'

	def __init__(self):
		BaseChart.__init__(self,chart_type = 'qr')

	def set_chart_qr_text(self, chart_qr_text = None):
		if chart_qr_text: self.chart_qr_text = chart_qr_text

	def make_url(self):
		url = BaseChart.make_url(self)
		url += '&chl='+urllib2.quote(self.chart_qr_text)

		return url
