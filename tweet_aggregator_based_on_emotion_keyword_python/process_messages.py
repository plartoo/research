#!/u/pthiha/.local/bin/python2.7

from my_utils import *

print "\nRunning process_messages.py\t" + get_current_time()
print "===================================================="

#accnt_name = raw_input("Account name: ")
accnt_name = 'rochcitest'
api = authenticate(accnt_name)
data = load_databases(accnt_name)

lst_msg_id = retrieve_last_processed_id('last_processed_msg_id', data)

to_reply = []
my_print("==>Collecting recent DMs to be processed")
for m in api.direct_messages(since_id=lst_msg_id): #tweepy.Cursor():
	sender_id = m.sender.id_str
	created_at = time_to_str(m.created_at)

	msgobj = form_message_object(created_at, m.text, False)
	data = store_message(data, 'msgfrom', sender_id, msgobj)
	to_reply.append([sender_id, msgobj])

	if m.id > long(lst_msg_id):
		data['misc'] = {'last_processed_msg_id' : m.id_str}

if to_reply:
	print "Saving recently received DMs to database"
	write_databases(accnt_name, data)

my_print("==>Processing recent DMs")
for m in to_reply:				# REFACTOR
	uid = m[0]
	created_at = m[1].keys().pop()
	msg = m[1][created_at]['text']

	try:
		print "orig message---> " + msg
		msg = compose_reply_msg(msg)
		print "we replied---> " + msg
		api.send_direct_message(user_id=uid, text=msg)
		print "sent DM to user_id: " + uid

		# set replied flag to true for msgfrom
		data['msgfrom'][uid][created_at]['replied'] = True

		# log database for msgto
		time_sent = get_current_time()
		msgobj = form_message_object(time_sent, msg, False)
		data = store_message(data, 'msgto', uid, msgobj)
	except tweepy.error.TweepError, e:
		print m
		print e
		matchObj = re.match( r'You already said that', str(e), re.I)
		if matchObj:
			data['msgfrom'][uid][created_at]['replied'] = True
		pass

write_databases(accnt_name, data)



#for f in api.followers_ids(screen_name = accnt_name): # those you're following
#	print api._lookup_users(user_id = f)[0].__dict__
#	print api.show_friendship(source_screen_name = accnt_name, target_id = f)[0].__dict__
#	print api.show_friendship(source_screen_name = accnt_name, target_id = f)[1].__dict__
# for f in api.friends_ids(screen_name = accnt_name): # those you're following

