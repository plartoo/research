#!/u/pthiha/.local/bin/python2.7

# this is intended to be used with "search"
# I need to do one for Stream <https://dev.twitter.com/docs/api/1/get/statuses/sample>
# https://dev.twitter.com/docs/api/1/get/search
# https://dev.twitter.com/docs/using-search
# https://groups.google.com/forum/?fromgroups=#!topic/tweepy/jDRIsYHbCxM
# http://packages.python.org/tweepy/html/cursor_tutorial.html

import time

from my_utils import *

DATA_FILE_PATH = "/localdisk/search_data/"
FILTER_WORD_FILE = "./filter_words"

if __name__ == '__main__':

	accnt_name = 'rochcitest2'
	api = authenticate(accnt_name)
	filter_words = load_json_file(FILTER_WORD_FILE) # 153 as of August 24

	#lst_msg_id = retrieve_last_processed_id('last_processed_public_tweet', data)
	#sss = "%22am%20chilling%22%20OR%20%22feel%20blue%22"
	#sss = '"am chilling"OR"feel Blue"'

	print "\nRunning collect_samples.py\t" + get_current_time()
	print "===================================================="

	while True:
		for word,last_id in filter_words.items():
			count = 0
			quoted = '"'+ word +'"' # put quotes around for exact search

			full_file_path = DATA_FILE_PATH + word.replace(' ', '')
			collection = load_json_file(full_file_path)

			try:
				for m in tweepy.Cursor(api.search, q=quoted, lang='en', since_id=last_id, show_user=True, include_entities=True).items(1500):

					if m.id > last_id:
						filter_words[word] = m.id

					collection[m.id] = m.text
					count = count+1

				print "Count =>\t" + word + "\t=>\t" + str(count)
				write_json_file(full_file_path, collection)
				write_json_file(FILTER_WORD_FILE, filter_words)
				time.sleep(300)	# wait 5 minutes

			except Exception, e:
				print e
				continue


