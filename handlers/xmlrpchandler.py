# -*- coding: utf-8 -*-

import etornado.utils.xmlrpc

class XmlRpcHandler(etornado.utils.xmlrpc.Handler):
	def _auth_login(self,user_name, user_pass):
		return [user_name,user_pass]

def getHandlerInfo():
	return (r"/xmlrpc",XmlRpcHandler)