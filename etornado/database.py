# -*- coding: utf-8 -*-

__author__="otavio"
__date__ ="$11/10/2009 13:20:44$"

#General tornado database module
import tornado.database

#Helper modules
import hashlib

from etornado.utils.serialize import serialize
from etornado.utils.serialize import unserialize

class EightDatabaseCache(object):
	cache_timer = {}

	def __init__(self):
		try:
			import time
		except ImportError:
			raise Exception("No time module found")

	@classmethod
	def instance(cls):
		if not hasattr(cls,"_instance"):
			cls._instance = cls()
		return cls._instance

	def set(self,key_name = None, key_value = None, key_time = 60):
		self.cache_timer[key_name] = (key_time,int(time.time()))

	def valid_key(self,key_name):
		if not self.cache_timer.has_key(key_name):
			return False
		else:
			if int(time.time()) - self.cache_timer[key_name][1] > self.cache_timer[key_name][0]:
				return False

		return True

	def get(self,key_name):
		if self.valid_key(key_name):
			return None
		else:
			return None

	def _del(self,key_name):
		del self.cache_timer[key_name]


class EightDatabaseStringCache(EightDatabaseCache):
	query_cache = {}
	query_time = {}

	def __init__(self, application = None):
		EightDatabaseCache.__init__(self)

	def set(self,key_name = None, key_value = None, key_time = 60):
		self.query_cache[key_name] = serialize(key_value)
		EightDatabaseCache.set(self,key_name, key_value, key_time)

	def get(self,key_name):
		if self.valid_key(key_name):
			return unserialize(self.query_cache[key_name])

		return None

	def _del(self,key_name):
		del self.query_cache[key_name], self.query_time[key_name]
		EightDatabaseCache._del(self,key_name)

class EightDatabaseMemCache(EightDatabaseCache):
	memcache_client = False

	def __init__(self, application = None):
		memcachemodule = False
		try:
			import cmemcached
			memcachemodule = cmemcached
		except ImportError:
			try:
				import memcache
				memcachemodule = memcache
			except ImportError:
				raise Exception("Memcache not avaiable")
		finally: EightDatabaseCache.__init__(self)

		if application.settings.get("memcache_servers"):
			self.memcache_client = memcachemodule.Client(application.settings.get("memcache_servers"))
		else:
			raise Exception("Memcache Servers not configured, use memcache_servers settings to application")

	def set(self,key_name = None, key_value = None, key_time = 60):
		if not self.memcache_client: return False

		self.memcache_client.set("db_"+key_name, key_value, key_time)

	def get(self,key_name):
		if not self.memcache_client: return None

		return self.memcache_client.get("db_"+key_name)

	def _del(self,key_name):
		if not self.memcache_client: return False

		self.memcache_client.delete("db_"+key_name)

class EightDatabaseHandler(tornado.database.Connection):
	use_cache = False
	cache_time = 60
	cache_object = False

	def __init__(self,host = None, database = None, user = None, password = None, application = None):
		if host is None or database is None: raise Exception("Params cannot be None")

		tornado.database.Connection.__init__(self,host,database,user,password)
		self.cache_object = application.settings.get("database_cache_backend",EightDatabaseStringCache)(application)

	def __del__(self):
		if hasattr(self,"_db"): tornado.database.Connection.__del__(self)

	@classmethod
	def instance(cls,**kwargs):
		if not hasattr(cls,"_instance"): cls._instance = cls(**kwargs)
		return cls._instance

	def query(self, query, *parameters, **kwargs):
		if not "use_cache" in kwargs: use_cache = self.use_cache
		else: use_cache = kwargs["use_cache"]

		if not use_cache: return tornado.database.Connection.query(self,query,*parameters)
		else:
			query_hash = str(hashlib.md5(str(query)+serialize(parameters)).hexdigest())

			if not self.cache_object.get(query_hash):
				query_object = tornado.database.Connection.query(self,query,*parameters)
				self.cache_object.set(query_hash, query_object, self.cache_time)
				return query_object

			else: return self.cache_object.get(query_hash)