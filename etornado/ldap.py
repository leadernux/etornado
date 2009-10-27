# -*- coding: utf-8 -*-

__author__="otavio"
__date__ ="$12/10/2009 20:59:33$"

try:
	import ldap
	import ldap.modlist
except ImportError, e: raise Exception("LDAP: "+str(e))

class EightLdap(object):
	connection = False

	def __init__(self, ldap_server = None, bind_dn = None, bind_secret = None, synchrounous = False):
		if ldap_server:
			try:
				self.connection = ldap.open(ldap_server)
				if not synchrounous:
					if bind_dn: self.connection.simple_bind(bind_dn, bind_secret)
				else:
					if bind_dn: self.connection.simple_bind_s(bind_dn, bind_secret)
			except:
				raise Exception("LDAP: Cannot connect to LDAP server on:"+ldap_server)
		self.synchrounous = synchrounous

	@classmethod
	def instance(cls):
		if not hasattr(cls,"_instance"):
			cls._instance = cls()
		return cls._instance

	def close(self):
		if self.connection:
			if not self.synchrounous: self.connection.unbind()
			else: self.connection.unbind_s()
			self.connection = False

	def search(self,search_query = None, base_dn = None):
		result_set = []

		if search_query:
			if self.connection:
				try:
					if self.synchrounous: ldap_result_id =\
						self.connection.search_s(base_dn,ldap.SCOPE_SUBTREE,search_query, None)
					else: ldap_result_id =\
						self.connection.search(base_dn,ldap.SCOPE_SUBTREE,search_query, None)
					while 1:
						result_type, result_data = self.connection.result(ldap_result_id, 0)
						if result_data == []:
							break
						else:
							if result_type == ldap.RES_SEARCH_ENTRY:
								result_set.append(result_data)
				except: return False
				finally: return result_set

		return False

	def delete(self,delete_dn = None):
		if delete_dn:
			if self.connection:
				try:
					if self.synchrounous: self.connection.delete_s(delete_dn)
					else: self.connection.delete(delete_dn)
				except: return False
				finally: return True

		return False

	def add(self):
		pass