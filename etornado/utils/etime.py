# -*- coding: utf-8 -*-

__author__="otavio"
__date__ ="$01/11/2009 10:17:58$"

import time
#import datetime

def unixtime():
	return int(time.mktime(time.localtime()))
