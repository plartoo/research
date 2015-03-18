#!/usr/bin/env python

import json

fname = 'rochcitest2'
f = open(fname,'w')

data = {'consumer_key':'ZNSslnGZGELPTMVwMtg',
	'consumer_secret':'d9z0YQd3tnAb9skMw9h5mF0rCN6g1jNRNFMPW3SeB8',
	'access_key':'701603239-lc1eg9Z3cESvYsMgh2xKMJWviwgOepZHMz9684Fo',
	'access_secret':'xI3pFCgRcCOTOeFOPEvbb2WocsJyY7blFYzuQYog'}

json.dump(data,f)

f.close()
print "data written and file closed"


f = open(fname,'r')
print json.load(f)
f.close()
