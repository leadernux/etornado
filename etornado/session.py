import os.path
# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="otavio"
__date__ ="$11/10/2009 20:55:03$"

try:
	import time
	import pickle
	import random
	import hashlib
except ImportError,e:
	raise Exception("Session: Import essential modules: "+str(e))

class EightSessionDatabaseBackend(object):
	def __init__(self):
		try:
			from etornado.database import EightDatabaseHandler
			self.database = EightDatabaseHandler.instance()
		except: raise Exception("Database not initiated")

		try: self.database.get("SELECT * FROM session LIMIT 1")
		except:
			if not self.create_table(): raise Exception("Table doesn't exists and cannot create")

	def create_table(self):
		sql = """
			CREATE TABLE session(
				`session_id` VARCHAR(32) NOT NULL,
				PRIMARY KEY(`session_id`),
				session_data TEXT NOT NULL,
				session_time INT(11) NOT NULL
			)
		"""

		try: self.database.execute(sql)
		except: return False
		return True

	def get_session(self,session_id):
		session_data = self.database.get("SELECT * FROM session WHERE session_id = %s",session_id)

		if session_data: return pickle.loads(str(session_data.session_data))
		return None

	def set_session(self,session_id, session_data):
		session_time = int(time.time())
		session_data = pickle.dumps(session_data)

		sql = """INSERT INTO session (`session_id`, `session_data`, `session_time`)
				VALUES (%s, %s, %s)
				ON DUPLICATE KEY
					UPDATE `session_data` = %s, `session_time` = %s"""

		try: self.database.execute(sql, session_id, session_data, session_time, session_data, session_time)
		except Exception, e: raise e
		return True

	def delete_session(self,session_id):
		try: self.database.execute("DELETE FROM session WHERE session_id = %s",session_id)
		except: return False
		return True

class EightSessionFileBackend(object):
	def __init__(self):
		try:
			from etornado.multiapplication import MultiHostApplication
			self.file_path = MultiHostApplication.instance().settings.get("file_session_path","/tmp")
			import os

		except: raise Exception("Cannot initialize FileBackend")

	def get_session(self,session_id):
		session_path = os.path.join(self.file_path, "sess_"+session_id+".txt")
		if os.path.exists(session_path):
			try:
				fp = open(session_path,"r")
				tmp = pickle.load(fp)
				fp.close()
			except: return None
			finally: return tmp

		else: return None

	def set_session(self,session_id, session_data):
		session_path = os.path.join(self.file_path, "sess_"+session_id+".txt")
		try:
			fp = open(session_path,"w+")
			pickle.dump(session_data,fp)
			fp.close()
		except: return False

		return True

	def delete_session(self,session_id):
		session_path = os.path.join(self.file_path, "sess_"+session_id+".txt")
		if os.path.exists(session_path):
			try:
				os.unlink(session_path)
			except: return False

		return True

class EightSessionMemcacheBackend(object):
	memcache_client = False

	def __init__(self):
		try:
			import cmemcached
			from etornado.multiapplication import MultiHostApplication
			app = MultiHostApplication.instance()
			if app.settings.get("memcache_servers"):
				self.memcache_client = cmemcached.Client(app.settings.get("memcache_servers"))
			else: raise Exception()
		except: raise Exception("CMemcacheD not initiated")

	def get_session(self,session_id):
		return self.memcache_client.get("session_"+session_id)

	def set_session(self,session_id, session_data):
		self.memcache_client.set("session_"+session_id, session_data,60*60)

	def delete_session(self,session_id):
		self.memcache_client.delete("session_"+session_id)

class EightSession(object):
	session_data = {}
	session_storage = False
	session_id = False

	def __init__(self, request = None):
		from etornado.multiapplication import MultiHostApplication

		self.session_storage = MultiHostApplication.instance().settings.get("session_storage_engine",EightSessionFileBackend)()

		if request is not None:
			if request.get_secure_cookie('session_id'):
				self.session_id = request.get_secure_cookie('session_id')
			else:
				self.session_id = hashlib.md5(str(random.random()+time.time())).hexdigest()
		else:
			self.session_id = hashlib.md5(str(random.random()+time.time())).hexdigest()

		self.load_session(request)

	def set_value(self,key_name,key_value = None):
		if type(key_name) == str: self.session_data[key_name] = key_value
		else:
			for k in key_name: self.session_data[k] = key_name[k]

		self.update_session()

	def update_session(self): return self.session_storage.set_session(self.session_id, self.session_data)

	def load_session(self, request):
		self.session_data = self.session_storage.get_session(self.session_id)
		if self.session_data == None: self.session_data = {}

		if request is not None: request.set_secure_cookie('session_id',self.session_id)

	def delete_session(self): return self.session_storage.delete_session(self.session_id)

	def get_value(self,key_name):
		if self.session_data.has_key(key_name): return self.session_data[key_name]
		return None
