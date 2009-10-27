# -*- coding: utf-8 -*-

__author__="otavio"
__date__ ="$16/10/2009 20:35:29$"

def _unicode(value):
	if isinstance(value, str):
		return value.decode("utf-8")
	assert isinstance(value,unicode)
	return value

try:
	import json
	assert hasattr(json,"loads") and hasattr(json,"dumps")
	_decode = lambda s: json.loads(s)
	_encode = lambda v: json.dumps(v)
except:
	try:
		import simplejson
		_decode = lambda s: simplejson.loads(_unicode(s))
		_encode = lambda v: simplejson.dumps(v)
	except:
		try:
			import pickle
			_decode = lambda s: pickle.loads(_unicode(s))
			_encode = lambda v: pickle.dumps(v)
		except:
			raise Exception("No json, simplejson or pickle module found")

def serialize(s):
	return _encode(s)

def unserialize(s):
	return _decode(s)

