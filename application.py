# -*- coding: utf-8 -*-

if __name__ == "__main__":
	import os

	import etornado.handlers
	etornado.handlers.init_all(__file__)

	from etornado.multiapplication import MultiHostApplication
	from etornado.database import EightDatabaseMemCache
	from etornado.session import EightSessionMemcacheBackend

	settings = {
		"cookie_secret" :"3c82d334e491b20a410a61ad2725bd18/Vo=",
		"login_url" : "/login",
		"xsrf_cookies" : True,
		"static_path" : os.path.join(os.path.dirname(__file__),"static"),
		"template_path" : os.path.join(os.path.dirname(__file__),"templates"),
		"debug" : True,
		"multihost_db_host": "localhost",
		"multihost_db_name": "eight_blog",
		"multihost_db_user": "root",
		"multihost_db_password": None,
		"memcache_servers": ["127.0.0.1:11211"],
		"use_locale": True,
		"http_port": 8080,
		"database_cache_backend": EightDatabaseMemCache,
		"session_storage_engine": EightSessionMemcacheBackend
	}

	application = MultiHostApplication.instance(etornado.handlers.get_handlers(__file__), **settings)
	application.start_server(__file__)