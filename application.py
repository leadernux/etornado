#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
ETornado application launcher
Under the terms of the Apache License
See LICENSE for more details
Copyleft Eight Systems http://eightsystems.com.br
'''

if __name__ == "__main__":
	import os

	'''
	Imports the options module, parse_command_line, parse_config_file and the define method
	'''
	from tornado.options import parse_command_line as options_parse_command_line
	from tornado.options import parse_config_file as options_parse_config_file
	from tornado.options import define, options

	'''
	Starts all the definitions
	'''
	define("port",default = 8080, help = "run on the given port", type = int)
	define("debug", default = True, help = "run in debug mode", type = bool)
	define("memcache_servers", default = "127.0.0.1:11211", help = "Memcache Servers", multiple = True)
	define("database_backend", default = "sqlite", help = "Database Backend (sqlite, mysql)", type = str)
	define("database_host", default = "application.sqlite", help = "Database Host (with SQLIte, the Filename)", type = str)
	define("database_name", default = "eight_application", help = "Database Name", type = str)
	define("database_user", default = None, help = "Database Username")
	define("database_password", default = None, help = "Database Password")
	define("use_locale", default = False, help = "Use locales", type = bool)
	define("database_cache_backend", default = "memcache", help = "Database Cache Backend (memcache, string)", type = str)
	define("session_storage_engine", default = "memcache", help = "Session Storage Backend (file, memcache, database)", type = str)
	define("cookie_secret", default = "3c82d334e491b20a410a61ad2725bd18/Vo=", help = "Cookie Secret Hash", type = str)

	'''
	Search for the application config in the following files: [/etc/eapplication.conf, ./application.conf]
	'''
	for cfg_file in ("/etc/eapplication.conf", "application.conf"):
		try: options_parse_config_file(cfg_file)
		except: print("Didn't load %s") % (cfg_file,)

	'''
	Parse the command line now
	'''
	options_parse_command_line()

	'''
	Regularize the memcache servers
	'''
	if type(options.memcache_servers) is not type([]): options.memcache_servers = [options.memcache_servers]

	'''
	Import the etornado handlers and init all the handlers
	'''
	import etornado.handlers
	etornado.handlers.init_all(__file__)

	'''Now initialize the base modules,
	MultiHostApplication, database, database cache storage, session, session storage
	'''
	from etornado.multiapplication import MultiHostApplication

	from etornado.database import EightDatabaseMemCache, EightSQLIteEngine, EightMySQLEngine, EightDatabaseStringCache

	database_backends = {"sqlite": EightSQLIteEngine, "mysql": EightMySQLEngine}
	try: options.database_backend = database_backends[options.database_backend]
	except: options.database_backend = EightSQLIteEngine

	database_cache_backends = {"memcache" : EightDatabaseMemCache, "string" : EightDatabaseStringCache}
	try: options.database_cache_backend = database_cache_backends[options.database_cache_backend]
	except: options.database_backend = EightDatabaseStringCache

	from etornado.session import EightSessionMemcacheBackend, EightSessionFileBackend, EightSessionDatabaseBackend
	session_engines = {"memcache": EightSessionMemcacheBackend, "file": EightSessionFileBackend, "database" : EightSessionDatabaseBackend}
	try: options.session_storage_engine = session_engines[options.session_storage_engine]
	except: options.session_storage_engine = EightSessionFileBackend

	'''
	The tornado settings
	'''
	settings = {
		"cookie_secret" : options.cookie_secret,
		"login_url" : "/login",
		"xsrf_cookies" : True,
		"static_path" : os.path.join(os.path.dirname(__file__),"static"),
		"template_path" : os.path.join(os.path.dirname(__file__),"templates"),
		"debug" : options.debug,
		"multihost_db_host": options.database_host,
		"multihost_db_name": options.database_name,
		"multihost_db_user": options.database_user,
		"multihost_db_password": options.database_password,
		"memcache_servers": options.memcache_servers,
		"use_locale": options.use_locale,
		"http_port": options.port,
		"database_backend": options.database_backend,
		"database_cache_backend": options.database_cache_backend,
		"session_storage_engine": options.session_storage_engine
	}

	'''
	Instance the Application
	'''
	application = MultiHostApplication.instance(etornado.handlers.get_handlers(__file__), **settings)

	'''
	Start the server
	'''
	application.start_server(__file__)