import sys,os
import urllib2
from BeautifulSoup import BeautifulSoup
import re

sys.path.append('/home/ortelius/projects')
os.environ['DJANGO_SETTINGS_MODULE'] ='bme.settings'

from bme.web.models import *

def slugify(inStr):
    removelist = ["a", "an", "as", "at", "before", "but", "by", "for","from","is", "in", "into", "like", "of", "off", "on", "onto","per","since", "than", "the", "this", "that", "to", "up", "via","with"];
    for a in removelist:
        aslug = re.sub(r'\b'+a+r'\b','',inStr)
    aslug = re.sub('[^\w\s-]', '', aslug).strip().lower()
    aslug = re.sub('\s+', '-', aslug)
    return aslug


def process_page(url):
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page)
	brs = soup.findAll('br')
	for br in brs:
		br.extract()

	installations = soup.findAll('span', { "class": "subhead" })

	for installation in installations:
		try:
			title = installation.next.next
			artists = installation.findNextSibling(text=True)
			description = artists.next

			xyear = year.objects.get(year='2006')
			newart = art_installation(name = title.strip(),
					year = xyear,
					artist = artists.strip(),
					slug = slugify(title),
					description = description.strip())
			newart.save()
			print newart
		except:
			print title
			print "Unexpected error:", sys.exc_info()

pages = ['http://www.burningman.com/whatisburningman/2006/06_art_pavilion.html',
	'http://www.burningman.com/whatisburningman/2006/06_art_funded.html',
	'http://www.burningman.com/whatisburningman/2006/06_art_theme.html',
	'http://www.burningman.com/whatisburningman/2006/06_art_playa.html',
	'http://www.burningman.com/whatisburningman/2006/06_art_cafe.html']
	
	#'http://www.burningman.com/whatisburningman/2006/06_art_manbase.html',
	#'http://www.burningman.com/whatisburningman/2006/06_exhibitions.html',

for page in pages:
	process_page(page)
