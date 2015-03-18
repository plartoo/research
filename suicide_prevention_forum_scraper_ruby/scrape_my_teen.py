#!/u/pthiha/.local/bin/python2.7

import urllib2
from BeautifulSoup import BeautifulSoup

"""
h = {}
# Step 1 - scraping Group Blog <http://myteenblog.com/blog/group/10961/all>
url = "http://myteenblog.com/blog/group/10961/all"
c = urllib2.urlopen(url)
soup = BeautifulSoup(c.read())

for tag in soup('h3')[2:]: # take out the first two tags
	h[tag.contents[0]['href']] = True

# Step 2 - scraping Group Discussion <http://myteenblog.com/discussion/owner/10961>
url = "http://myteenblog.com/discussion/owner/10961"
c = urllib2.urlopen(url)
soup = BeautifulSoup(c.read())

for tag in soup('h3')[1:]: # take out the first tag
	h[tag.contents[0]['href']] = True

all_urls = h.keys()
print all_urls
"""

f = open('results', 'w')

all_urls = [u'http://myteenblog.com/blog/view/66849/has-anyone-else-suffered-like-me', u'http://myteenblog.com/blog/view/66918/what-all-could-happen-in-the-life-of-i-dont-care', u'http://myteenblog.com/blog/view/64193/surviving-made-me-stronger', u'http://myteenblog.com/discussion/view/76416/drink-the-pain-away', u'http://myteenblog.com/blog/view/29714/feeling-lonely-and-unloved', u'http://myteenblog.com/blog/view/75998/for-everyone', u'http://myteenblog.com/blog/view/104470/trapped', u'http://myteenblog.com/blog/view/67935/my-two-cents-on-life', u'http://myteenblog.com/blog/view/60680/he-took-it-all-from-me', u'http://myteenblog.com/blog/view/50532/question']

for url in all_urls:
	print url
	c = urllib2.urlopen(url)
	s = BeautifulSoup(c.read())
	ts = s.findAll("div", "elgg-output")
	for t in ts:
		#print t.contents[0:]
		for p in t.contents[0:]:
			unicode_string = unicode(p.string)
			#print unicode_string
			f.write(unicode_string)



f.close()
