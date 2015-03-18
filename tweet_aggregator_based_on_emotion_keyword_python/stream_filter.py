#!/u/pthiha/.local/bin/python2.7

# regarding blocking IPs https://dev.twitter.com/discussions/921

from tweepy import OAuthHandler
from tweepy import Stream

from my_utils import *	# REFACTOR because this guy has to be imported AGAIN in "my_listener.py"
from my_listener import MyListener

FILTER_WORD_FILE = "filter_words"
DATA_FILE_PATH = "/localdisk/filter_data/"
#DATA_FILE_PATH = "./sample_data/"


# */15 * * * * $HOME/Downloads/roc_tweet/stream_filter.py >> $HOME/Downloads/roc_tweet/logs/filter_log 2>&1
"""
from tweepy.streaming import StreamListener

class StreamListener(tweepy.StreamListener):
	def on_status(self, status):
		print "Hello"
		try:
			print status.text
		except Exception, e:
			print e
			# Catch any unicode errors while printing to console
			# and just ignore them to avoid breaking application.
			pass

	def on_error(self, status):
		print "ERROR in my_listener: " + str(status)
"""
if __name__ == '__main__':
	account_name = "rochcitest3"
	keys = load_keys(account_name)
	auth = set_auth(keys)

	"""
	l = StreamListener()
	streamer = tweepy.Stream(auth=auth, listener=l, timeout=3000000000 )
	setTerms = ['hello', 'goodbye', 'goodnight', 'good morning']
	streamer.filter(None,setTerms)
	"""

	filter_words = load_json_file(FILTER_WORD_FILE).keys()

	#print filter_words[0:3]
	filter_words = ['hello']
	#quit()
	l = MyListener(DATA_FILE_PATH)
	stream = Stream(auth, l)
	stream.filter(None, track=filter_words)

	end_time = get_current_time(timestmp=True)
	print "\nRunning stream_filter.py\t" + get_current_time()
	print "===================================================="
	print "Filtered 1000 tweets in (sec):\t" + str(float(end_time) - float(l.start_time))

	# https://dev.twitter.com/docs/streaming-apis/parameters
	#stream.filter(track=['feel%20blue']) # EXACT MATCH DOES NOT WORK. e.g., 'feel blue', '"feel blue"'

