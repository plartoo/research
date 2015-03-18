#!/u/pthiha/.local/bin/python2.7

import tweepy
from tweepy.utils import parse_datetime
from email.mime.text import MIMEText
import smtplib

import sys
import os.path
import json
import re
import datetime

"""
Collection of util functions used in roc_tweet scripts.
Note:
	- update 'MY_PATH' variable to appropriate value so that cronjob
	  can call the script without 'file_not_found' errors
	- update 'FILTER_WORDS' variable if you'd like to use different
	  set of filter words
"""

MY_PATH = "/Downloads/roc_tweet/"
VERBOSE = False

def get_dir_name():
	return os.getenv("HOME") + MY_PATH

def get_filename(accnt_name, database_name):
	fname = accnt_name + '_' + database_name
	full_path = get_dir_name() + fname
	return full_path

def my_print(msg):
	if VERBOSE:
		print msg

def load_keys(accnt_name):
	try:
		fname = get_dir_name() + accnt_name
		f= open(fname, 'r')
		keys= json.load(f)
		f.close()
	except Exception, e:
		print e
		print "-----"
		print "Note: You must have a file that stores consumer key,secret"
		print "and access key,secret in JSON and have the same name"
		print "as the account name provided at the prompt"
		quit()

	return keys

def set_auth(keys):
	auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
	auth.set_access_token(keys['access_key'], keys['access_secret'])
	return auth

def authenticate(accnt_name):
	"""
	Authenticates the user with oauth credentials that are stored in a
	file with the same label as twitter account name.
	"""
	keys = load_keys(accnt_name)
	auth = set_auth(keys)
	api = tweepy.API(auth)
	return api

def load_databases(accnt_name):
	my_print("Loading databases")

	data = {'pending':{}, 'invited':{}, 'msgto':{}, 'msgfrom':{}, 'mentions':{},
		'to_follow':{}, 'misc':{}}

	try:
		for k,v in data.items():
			fname = get_filename(accnt_name, k)

			if (os.path.exists(fname)):
				f = open(fname, 'r')
				data[k] = json.load(f)
				f.close()
			else:
				data[k] = {}
	except Exception, e:
		print e
		print '-----'
		print "Note: Follower and following user information must"
		print "be saved as JSON in a file"
		quit()
	return data

# separated from load_databases because we don't want/need
# to rewrite this often as we do to other databases
def load_json_file(full_file_path):

	if (os.path.exists(full_file_path)):
		f = open(full_file_path, 'r')
		data = json.load(f)
		f.close()
	else:
		data = {}

	return data

def write_json_file(full_file_path, data):
	f = open(full_file_path, 'w')
	json.dump(data, f)
	f.close()

def write_databases(accnt_name, data):
	backup_data = load_databases(accnt_name)

	for k, v in data.iteritems():
		fname = get_filename(accnt_name, k)
		try:
			f = open(fname, 'w')
			json.dump(v, f)
			f.close()
			my_print('file written: ' + fname)

		except Exception, e:
			print e
			print '-----'
			print 'backup data is restored'
			f.close()
			f = open(fname, 'w')
			json.dump(backup_data[k], f)
			f.close()
			quit()

def store_message(data, key, user_id, msgobj):
	if user_id in data[key]:
		data[key][user_id].update(msgobj)
	else:
		data[key][user_id] = msgobj

	return data

def form_message_object(created_at, text, replied):
	return {created_at : {'text':text, 'replied':replied}}

def compose_reply_msg(orig_msg):		# TODO
	msg =  "parroting101: " + orig_msg
	return msg

def compose_reply_mention(screen_name, orig_msg):
	msg =  "@" + screen_name + " Please follow me on twitter so that you and I can communicate privately"
	return msg

def retrieve_last_processed_id(key, data):
	if not key in data['misc']:
		lst_msg_id = 0L
	else:
		lst_msg_id = data['misc'][key]

	return lst_msg_id

def get_current_time(timestmp=False):
	cur_time = datetime.datetime.now()
	cur_time = cur_time.strftime('%a %b %d %H:%M:%S +0000 %Y')
	cur_time = parse_datetime(cur_time)

	if timestmp == True:				# REFACTOR
		cur_time = cur_time.strftime("%s")
	else:
		cur_time = str(cur_time)

	return cur_time

def time_to_str(dateobj):
	t = dateobj.strftime('%a %b %d %H:%M:%S +0000 %Y')
	return str(parse_datetime(t))

def str_to_time(date_str):
	# REVERSE: date string to datetime object
	# date_str = "2008-11-10 17:53:59"
	return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

def get_list_difference(l1, l2):
	intersection = set(l1).intersection(set(l2))

	return set(l1).difference(intersection)

def send_email(sender, receipient, msg):
	s = smtplib.SMTP("smtp.gmail.com", 587)
	s.ehlo()
	s.starttls()
	s.ehlo()
	s.login("rochciresearch", "rocpass1")

	s.sendmail(sender, [receipient], msg.as_string())
	s.close()

def notify_pending_requests(user_count):
	sender = "rochciresearch@gmail.com"
	receipient = "rochciresearch@gmail.com"

	msg = "You have " + str(user_count) + " users waiting to follow you on Twitter.\n"
	msg = MIMEText(msg)
	msg['Subject'] = "New follow request on Twitter"
	msg['From'] = sender
	msg['To'] = receipient
	send_email(sender, receipient, msg)

