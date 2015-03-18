#!/u/pthiha/.local/bin/python2.7

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from my_utils import *

class StdOutListener(StreamListener):
	""" 
	A listener handles tweets are the received from the stream.
	This is a basic listener that just prints received tweets to stdout.
	"""
	def on_data(self, data):
		print "\n\n"
		jj =  json.loads(data)
		try:
			print jj['text']
		except Exception, e:
			print jj
			print e
			print "-----"
			quit()
		
		return True

	def on_error(self, status):
		print status

if __name__ == '__main__':
	l = StdOutListener()
	account_name = "rochcitest1"
	keys = load_keys(account_name)
	auth = set_auth(keys)

	stream = Stream(auth, l)
	stream.sample()
	# https://dev.twitter.com/docs/streaming-apis/parameters
	#stream.filter(track=['feel%20blue']) # DOESNOT WORK 'feel blue', '"feel blue"'

