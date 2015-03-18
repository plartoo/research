#!/usr/bin/env python

import sys
import tweepy

CONSUMER_KEY = 'JkZ2Z4ANT7Hl2GEmiNSv2Q'
CONSUMER_SECRET = 'TAQXavOeF2tAVRHjfJfLPPa6cMLwZRtkbILhADxbHuk'
ACCESS_KEY = '635662865-eMKmd5MNFlpQ6IPLAa3s60KKRDzvekzPjnCzTPM'
ACCESS_SECRET = 'UW4VQW4xQuLty4t0NFZHHNC9BltepXdFVuNLy7npM'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

#api.update_status(sys.argv[1])
#api.update_status('hello testing testing json json')


myuser = 'rochcitest'
#api.send_direct_message(screen_name = myuser, text = sys.argv[1])

#msgs = api.direct_messages()
#print msgs

# print the tweets i made in the past
#statuses = tweepy.Cursor(api.user_timeline).items()
#for status in statuses:
#	print "  "
#	print status.text

"""
mymentions= tweepy.Cursor(api.mentions).items()
for status in mymentions:
	print " "
	print status.text

# returns an array of numeric IDs for every user following the specified user.
followers = api.followers_ids(screen_name = myuser)
print followers

# Returns an array of numeric IDs for every user the specified user is following
friends = api.friends_ids(screen_name = myuser)
print friends
"""

print api.show_friendship(source_screen_name=myuser, target_screen_name='rochcitest1')[0].__dict__
print api.show_friendship(source_screen_name=myuser, target_screen_name='rochcitest1')[1].__dict__
print api.show_friendship(source_screen_name=myuser, target_screen_name='rochcitest1')[0].followed_by


>>> import sys
>>> import tweepy
>>> import json
>>> from utils import *
>>> api = authenticate('rochcitest1')
>>> mens=tweepy.Cursor(api.mentions).items()
>>> mens
<tweepy.cursor.ItemIterator object at 0x159dfd0>
>>> mens[1]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'ItemIterator' object does not support indexing
>>> mens[0]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'ItemIterator' object does not support indexing
>>> mens.first
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'ItemIterator' object has no attribute 'first'
>>> mens.__dict__
{'count': 0, 'page_index': -1, 'current_page': None, 'limit': 0, 'page_iterator': <tweepy.cursor.PageIterator object at 0x159df90>}
>>> for status in mens:
...     print status.author.__dict__
... 
{'follow_request_sent': False, 'profile_use_background_image': True, 'id': 635662865, '_api': <tweepy.api.API object at 0x159df10>, 'verified': False, 'profile_image_url_https': 'https://si0.twimg.com/sticky/default_profile_images/default_profile_5_normal.png', 'profile_sidebar_fill_color': 'DDEEF6', 'is_translator': False, 'geo_enabled': False, 'profile_text_color': '333333', 'followers_count': 1, 'protected': True, 'location': '', 'default_profile_image': True, 'id_str': '635662865', 'utc_offset': -18000, 'statuses_count': 5, 'description': '', 'friends_count': 1, 'profile_link_color': '0084B4', 'profile_image_url': 'http://a0.twimg.com/sticky/default_profile_images/default_profile_5_normal.png', 'notifications': None, 'show_all_inline_media': False, 'profile_background_image_url_https': 'https://si0.twimg.com/images/themes/theme1/bg.png', 'profile_background_color': 'C0DEED', 'profile_background_image_url': 'http://a0.twimg.com/images/themes/theme1/bg.png', 'name': 'rochcitest', 'lang': 'en', 'profile_background_tile': False, 'favourites_count': 0, 'screen_name': 'rochcitest', 'url': None, 'created_at': datetime.datetime(2012, 7, 14, 21, 17, 47), 'contributors_enabled': False, 'time_zone': 'Eastern Time (US & Canada)', 'profile_sidebar_border_color': 'C0DEED', 'default_profile': True, 'following': True, 'listed_count': 0}
>>> for status in mens:
...     author = status.author
... 
>>> print author.name
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'author' is not defined
>>> author = None
>>> for status in mens:
...     author = status.author
... 
>>> print author.name
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'NoneType' object has no attribute 'name'
>>> authors = []
>>> for status in mens:
...     authors.append(status.author)
... 
>>> authors
[]
>>> for status in mens:
...     print status.author
...     authors.append(status.author)
... 
>>> for status in mens:
...     print status.author.__dict__
... 
>>> mens=tweepy.Cursor(api.mentions).items()
>>> for status in mens:
...     authors.append(status.author)
... 
>>> print authors
[<tweepy.models.User object at 0x18110d0>]
>>> authors[0].name
'rochcitest'
>>> authors[0].created_at
datetime.datetime(2012, 7, 14, 21, 17, 47)
>>> authors[0].created_at.type
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'datetime.datetime' object has no attribute 'type'
>>> authors[0].created_at.type()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'datetime.datetime' object has no attribute 'type'
>>> type(authors[0].created_at)
<type 'datetime.datetime'>
>>> import datetime
>>> authors[0].created_at.__dict__
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'datetime.datetime' object has no attribute '__dict__'
>>> authors[0].created_at
datetime.datetime(2012, 7, 14, 21, 17, 47)
>>> authors[0].created_at
datetime.datetime(2012, 7, 14, 21, 17, 47)
>>> import time
>>> time.mktime(authors[0].created_at)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: argument must be 9-item sequence, not datetime.datetime
>>> dt_obj = datetime(2008, 11, 10, 17, 53, 59)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'module' object is not callable
>>> from datetime import datetime
>>> dt_obj = datetime(2008, 11, 10, 17, 53, 59)
>>> type(dt_obj)
<type 'datetime.datetime'>
>>> authors[0].created_at > dt_obj


