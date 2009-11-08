# -*- coding: utf-8 -*-

from etornado.database import EightDatabaseHandler

from random import random
from hashlib import md5

class Profile(object):
	def __init__(self):
		self.database = EightDatabaseHandler.instance()

	def login(self,user_id,user_fields):
		#First select the user, so we know if it exists =)
		rs = self.database.query("SELECT * FROM users WHERE users_id = %s",user_id)
		if len(rs) == 0:
			#Too bad, user doesn't exists, so maybe is from an openid?
			try: self.database.execute("INSERT INTO users (`users_id`, `users_name`, `users_password`) VALUES(%s, %s, %s)",user_id,user_fields['user_name'], md5(str(random())).hexdigest())
			except: return False

		#Now the profile =)
		rs = self.database.query("SELECT * FROM profile WHERE users_id = %s",user_id)
		if len(rs) == 0:
			#Too bad, user doesn't exists, so maybe is from an openid?
			try: 
				self.database.execute("INSERT INTO profile (`users_id`, `profile_displayname`, `profile_location`, `profile_image_url`) VALUES(%s, %s, %s,%s)",
					user_id,
					user_fields['profile_displayname'],
					user_fields['profile_location'],
					user_fields['profile_image_url']
				)
			except: return False
		else:
			#Updating user data =)
			try: 
				self.database.execute("UPDATE profile SET `profile_displayname` = %s, `profile_location` = %s, `profile_image_url` = %s WHERE `users_id` = %s",
					user_fields['profile_displayname'],
					user_fields['profile_location'],
					user_fields['profile_image_url'],
					user_id
				)
			except: return False

		return True
