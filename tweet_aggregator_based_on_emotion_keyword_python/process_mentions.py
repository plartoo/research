#!/u/pthiha/.local/bin/python2.7

from my_utils import *

print "\nRunning process_mentions.py\t" + get_current_time()
print "===================================================="

#accnt_name = raw_input("Account name: ")
accnt_name = 'rochcitest'
api = authenticate(accnt_name)
data = load_databases(accnt_name)

to_reply = []
my_print("==>Collecting recent mentions to be processed")
for m in tweepy.Cursor(api.mentions).items():
	if m.id_str not in data['mentions']:
		data['mentions'][m.id_str] = {'replied':False}
		data['mentions'][m.id_str]['id'] = m.author.id_str
		data['mentions'][m.id_str]['text'] = m.text
		data['mentions'][m.id_str]['follow_request_sent'] = m.author.follow_request_sent
		data['mentions'][m.id_str]['screen_name'] = m.author.screen_name
		data['mentions'][m.id_str]['following'] = m.author.following
		to_reply.append([m.id_str, data['mentions'][m.id_str]])

print "mentions to respond to: " + str(to_reply)
write_databases(accnt_name, data)

my_print("==>Processing recent mentions")
for m in to_reply:
	mention_id = m[0]
	msg_obj = m[1]
	uid = msg_obj['id']
	screen_name = msg_obj['screen_name']
	orig_msg = msg_obj['text']

	# already my follower? --> yes
	if msg_obj['following']:
		try:
			msg = compose_reply_msg(orig_msg)	# TODO
			api.send_direct_message(user_id=uid, text=msg)
			print "sent DM reply to the mention from user_id: " + uid

			# update database for msgto
			time_sent = get_current_time()
			msgobj = form_message_object(time_sent, msg, False)
			data = store_message(data, 'msgto', uid, msgobj)
		except tweepy.error.TweepError, e:
			print m
			print e
			matchObj = re.match( r'You already said that', str(e), re.I)
			if matchObj:
				data['mentions'][mention_id]['replied'] = True
			pass

	else:	# not a follower yet, then send a mention to tell him/her to follow me
		try:
			msg = compose_reply_mention(screen_name, orig_msg)
			api.update_status(msg)
			print "sent mention reply to the mention from user_id: " + uid
		except tweepy.error.TweepError, e:
			print m
			print e
			matchObj = re.match( r'.*duplicate.*', str(e), re.I)
			if matchObj:
				data['mentions'][mention_id]['replied'] = True
			pass


	if not data['mentions'][mention_id]['follow_request_sent']:
		print "added to database so that we can send them follow\
		request IF needed to --> " + uid
		data['to_follow'][uid] = False

	data['mentions'][mention_id]['replied'] = True

write_databases(accnt_name, data)
