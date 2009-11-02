# -*- coding: utf-8 -*-

__author__="otavio"
__date__ ="$11/10/2009 13:20:44$"

#Helper modules
from hashlib import md5

from etornado.utils.serialize import serialize
from etornado.utils.serialize import unserialize

import itertools

class Row(dict):
    """A dict that allows for object-like property access syntax."""
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

class Connection(object):
	_db = None

	def __init__(self, host, database, user=None, password=None):
		pass

	def __del__(self):
		if self._db is not None: self.close()

	def close(self):
		pass

	def iter(self, query, *parameters):
		pass

	def query(self,query, *parameters):
		pass

	def get(self,query, *parameters):
		pass

	def execute(self,query, *parameters):
		pass

	def executemany(self,query, *parameters):
		pass

class EightSQLIteEngine(Connection):
	def __init__(self,host,database,user = None, password = None):
		from sqlite3 import connect
		self._db = connect(host)
	def close(self):
		 if self._db is not None: self._db.close()
		 self._db = None

	def iter(self,query,*parameters):
		raise Exception("Not supported")

	def query(self,query, *parameters):
		"""Returns a row list for the given query and parameters."""
		cursor = self._db.cursor()
		try:
			query = query % tuple("?" * len(parameters))

			cursor.execute(query, parameters)
			column_names = [d[0] for d in cursor.description]
			return [Row(itertools.izip(column_names, row)) for row in cursor]
		finally:
			cursor.close()

	def get(self,query, *parameters):
		"""Returns the first row returned for the given query."""
		rows = self.query(query, *parameters)
		if not rows:
		    return None
		elif len(rows) > 1:
		    raise Exception("Multiple rows returned for Database.get() query")
		else:
		    return rows[0]

	def execute(self,query, *parameters):
		"""Executes the given query, returning the lastrowid from the query."""
		cursor = self._db.cursor()
		try:
		    cursor.execute(query, parameters)
		    return cursor.lastrowid
		finally:
		    cursor.close()

	def executemany(self,query, *parameters):
		"""Executes the given query against all the given param sequences.
		We return the lastrowid from the query.
		"""
		cursor = self._db.cursor()
		try:
		    cursor.executemany(query, parameters)
		    return cursor.lastrowid
		finally:
		    cursor.close()

class EightMySQLEngine(Connection):
	def __init__(self,host,database, user=None, password=None):
		from tornado.database import Connection as MySQLEngine
		self._db = MySQLEngine(host,database,user,password)

	def close(self):
		if self._db is not None: self._db.close()
		self._db = None

	def iter(self,query,*parameters):
		return self._db.iter(query,*parameters)

	def query(self,query,*parameters):
		return self._db.query(query,*parameters)

	def get(self,query, *parameters):
		return self._db.get(query,*parameters)

	def execute(self,query,*parameters):
		return self._db.execute(query,*parameters)

	def executemany(self,query,*parameters):
		return self._db.executemany(query,*parameters)

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

class EightDatabaseHandler(Connection):
	use_cache = False
	cache_time = 60
	cache_object = False

	def __init__(self,host = None, database = None, user = None, password = None, application = None, database_backend = None):
		if host is None or database is None: raise Exception("Params cannot be None")

		Connection.__init__(self,host,database,user,password)

		if not database_backend: self._db = EightMySQLEngine(host,database,user,password)
		else: self._db = database_backend(host,database,user,password)

		self.cache_object = application.settings.get("database_cache_backend",EightDatabaseStringCache)(application)

	def __del__(self):
		if hasattr(self,"_db"): self._db.close()
		self._db = None

	@classmethod
	def instance(cls,**kwargs):
		if not hasattr(cls,"_instance"): cls._instance = cls(**kwargs)
		return cls._instance

	def query(self, query, *parameters, **kwargs):
		if not "use_cache" in kwargs: use_cache = self.use_cache
		else: use_cache = kwargs["use_cache"]

		if not use_cache: return self._db.query(query,*parameters)
		else:
			query_hash = str(md5(str(query)+serialize(parameters)).hexdigest())

			if not self.cache_object.get(query_hash):
				query_object = self._db.query(query,*parameters)
				self.cache_object.set(query_hash, query_object, self.cache_time)
				return query_object

			else: return self.cache_object.get(query_hash)

	def close(self):
		return self._db.close()

	def iter(self, query, *parameters):
		return self._db.iter(query,*parameters)

	def get(self,query, *parameters):
		return self._db.get(query,*parameters)

	def execute(self,query, *parameters):
		return self._db.execute(query,*parameters)

	def executemany(self,query, *parameters):
		return self._db.executemany(query,*parameters)