#!/u/pthiha/.local/bin/python2.7

import langid
from tweepy.streaming import StreamListener

from my_utils import *

class MyListener(StreamListener):
	""" 
	This is a listener that collects tweets in English
	for approximately one minute and write them out to a flat file.
	"""

	def __init__(self, data_file_path):
		self.tweets = []
		self.start_time = get_current_time(timestmp=True)
		self.fpath = data_file_path

	def langid_verdict(self,tweet):
		result = langid.classify(tweet)
		if (result[0] == 'en') and (result[1] > 0.95):
			return True
		return False

	def is_in_english(self,tweetobj):
		twitter_lang = tweetobj["user"]["lang"]
		langid_result = self.langid_verdict(tweetobj['text'])
		if twitter_lang == "en" and langid_result:
			return True
		return False		

	def not_a_spammer(self,tweetobj):
		if tweetobj["user"]["friends_count"] > 0:
			return True
		return False
		
	def comply_with_rules(self,tweetobj):
		if self.not_a_spammer(tweetobj) and self.is_in_english(tweetobj):
			return True
		return False

	def is_queue_full(self):
		if len(self.tweets) == 1000:
			return True
		return False

	def get_file_name(self):
		return (self.fpath + self.start_time)

	def write_tweets_to_file(self):
		f = open(self.get_file_name(), 'w')
		json.dump(self.tweets, f)
		f.close()

	def on_data(self, data):
		tweetobj =  json.loads(data)
		if ("text" in tweetobj) and self.comply_with_rules(tweetobj):
			if not self.is_queue_full():
				self.tweets.append(tweetobj['text'])
			else:
				self.write_tweets_to_file()
				return False

		return True

	def on_error(self, status):
		print "ERROR in my_listener: " + str(status)
		if status == 420:
			print "In order to not make Twitter mad, quitting"
			quit()

