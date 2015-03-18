#!/u/pthiha/.local/bin/python2.7

from tweepy import OAuthHandler
from tweepy import Stream

from my_utils import *	# REFACTOR because this guy has to be imported AGAIN in "my_listener.py"
from my_listener import MyListener

DATA_FILE_PATH = "/localdisk/sample_data/"
#DATA_FILE_PATH = "./sample_data/"

if __name__ == '__main__':
	account_name = "rochcitest1"
	keys = load_keys(account_name)
	auth = set_auth(keys)

	l = MyListener(DATA_FILE_PATH)
	stream = Stream(auth, l)
	stream.sample()
	
	end_time = get_current_time(timestmp=True)
	print "\nRunning stream_sample.py\t" + get_current_time()
	print "===================================================="
	print "Collected 1000 sample tweets in (sec):\t" + str(float(end_time) - float(l.start_time))

