# -*- coding: utf-8 -*-

import tornado.web

from SimpleXMLRPCServer import SimpleXMLRPCDispatcher
from xmlrpclib import ServerProxy
from xmlrpclib import MultiCall

'''
Uses Handler to export your method over XML-RPC Server
Override register_method to register your method manually
And put _ in front of your method name to export it automatically
'''
class Handler(tornado.web.RequestHandler,SimpleXMLRPCDispatcher):
	def __init__(self,application, request, transforms=None):
		tornado.web.RequestHandler.__init__(self,application, request, transforms)

		SimpleXMLRPCDispatcher.__init__(self,True,None)

		self.register_multicall_functions()

		self.register_methods()

	'''
	Override check_xsrf_cookies so the application settings doesn't mess with the XML-RPC
	'''
	def check_xsrf_cookie(self):
		pass

	def register_methods(self):
		pass

	def _dispatch(self, method, params):
		try:
			if not method[-2:] == '__': method = method.replace(".","_")
			else: method = "_".join(method.split(".")[:-1])+"."+method.split(".")[-1:][0]

			# We are forcing the '_' prefix on methods that are
			# callable through XML-RPC to prevent potential security
			# problems
			func = getattr(self, '_' + method)
		except AttributeError:
			raise Exception('method "%s" is not supported' % method)
		else:
			return func(*params)

	def get(self):
		self.write("This is an XMLRpcHandler, only POST is supported")

	def post(self):
		self.set_header('Content-Type', 'text/xml')
		self.write(self._marshaled_dispatch(self.request.body))

Proxy = ServerProxy

class ProxyMulti(MultiCall):
	def __init__(self,uri, transport=None, encoding=None, verbose=0, allow_none=0, use_datetime=0):
		MultiCall.__init__(self,None)

		self._server = Proxy(uri, transport, encoding, verbose,allow_none, use_datetime)

	def clean_calls(self):
		self.__call_list = []

