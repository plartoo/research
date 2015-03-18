#!/u/pthiha/.local/bin/python2.7

from my_utils import *

print "\nRunning manage_account.py\t" + get_current_time()
print "===================================================="

#accnt_name = raw_input("Account name: ")
accnt_name = 'rochcitest'
api = authenticate(accnt_name)
data = load_databases(accnt_name)


my_print("==>Checking pending follow requests")
friends_incoming = tweepy.Cursor(api.friendships_incoming).items()
for f in friends_incoming:
	if str(f) not in data['pending']:
		data['pending'][str(f)] = {'time':get_current_time(), 'email':False}
		print "pending follow request FROM user id: " + str(f)


my_print("==>Collecting recently approved followers and purging them from pending list")
recently_approved = []
followers = api.followers_ids(screen_name=accnt_name)
for follower in followers:
	follower = str(follower)
	if data['pending'].has_key(follower):
		print "recently approved user id: " + follower
		recently_approved.append(follower)
		del data['pending'][follower]

write_databases(accnt_name, data)


# This MUST come after collecting recently approved follow requests
email_them = []
for k,v in data['pending'].items():
	if not v['email']:	# if we have not sent the email reminder
		email_them.append(k)

pending_user_count = len(email_them)
if pending_user_count > 0:
	my_print("==>Sending notification email to rochciresearch.AT.gmail.com")
	notify_pending_requests(pending_user_count)
	for i in email_them:
		data['pending'][i]['email'] = True

write_databases(accnt_name, data)


my_print("Loading users who mentioned our account into recently_approved")
from_mention = data['to_follow'].keys()
recently_approved = recently_approved + from_mention
print "from_mention: " + str(from_mention)
print "recently_approved: " + str(recently_approved)

my_print("==>Processing recently approved and mentions")
for f in recently_approved:
	friendship = api.show_friendship(source_screen_name=accnt_name,target_id=f)[1]
	print friendship.__dict__

	if friendship.followed_by == False:
		try:
			api.create_friendship(id = f)
			print "sent follow invite TO new follower with id: " + str(f)
			data['invited'][str(f)] = str(get_current_time())
		except Exception, e:
			print e
			print '-----'

		if friendship.following == True:
			try:
				msg = "Hi there, I am now following you on \
					Twitter so that we may converse \
					privately via direct messages if \
					you'd like to"
				api.send_direct_message(user_id = usr_id, text = msg)
				print "sent intro message to new follower with id: " + str(f)
				data['msgto'][str(f)][get_current_time()] = 'Intro' #msg
			except Exception, e:
				print e
				print '-----'

	# remove them from 'to_follow' list so that we don't invite them again
	if str(f) in data['to_follow']:
		del data['to_follow'][str(f)]

write_databases(accnt_name, data)
