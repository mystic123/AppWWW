from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
import urllib
from bs4 import BeautifulSoup
from pkw.models import *
from threading import Thread

class ParseComm(Thread):
	link = "http://prezydent2010.pkw.gov.pl/PZT/PL/WYN/W/"

	def __init__(self,url,d):
		self.url = url
		self.d = d
		super(ParseComm,self).__init__()

	@transaction.atomic
	def run(self):
		dist = urllib.urlopen(self.link + self.url)
		dist_soup = BeautifulSoup(dist)
		okreg_tab = dist_soup.find(id = 's0')
		for row in okreg_tab.find('tbody'):
			if row.find('a') != -1 and not row.find('a') is None:
				com = Commission()
				com.name = row.find('a').contents[0]
				com.dist = self.d; 
				com.nr = row.find('td').contents[0]
				com.save()
				#processed_com+=1
				#print(".."+row.find('td').contents[0]+com.name).encode('utf8')

class ParseCounty(Thread):
	link = "http://prezydent2010.pkw.gov.pl/PZT/PL/WYN/W/"
	threads = []

	def __init__(self,url,d):
		self.url = url
		self.d = d
		super(ParseCounty,self).__init__()

	#@transaction.atomic
	def run(self):
		county = urllib.urlopen(self.link + self.url)
		county_soup = BeautifulSoup(county)
		county_tab = county_soup.find(id = 's0')
		for row in county_tab.find('tbody'):
			if row.find('a') != -1:
				cnty = County()
				cnty.name = row.find('a').contents[0]
				cnty.city = self.d
				cnty.save()
				t = ParseComm(row.find('a').get('href'),cnty)
				self.threads.append(t)
				t.start()
	#	for t in self.threads:
	#		t.join()
	
class Command(BaseCommand):
	args = ''
	help = 'Downloads data from PKW website'

	#@transaction.atomic
	def handle(self, *args, **options):
		retries = 100
		threads = []
		processed_com = 0
		link = "http://prezydent2010.pkw.gov.pl/PZT/PL/WYN/W/"
		page = urllib.urlopen(link+"index.htm")
		soup = BeautifulSoup(page)
		table = soup.find(id = 's0')
		for row in table.find('tbody'):
			if row.find('a') != -1:
				v = Voivodeship()
				v.name = row.find('a').contents[0]
				v.save()
				print(row.find('a').contents[0]).encode('utf8')
				voiv = urllib.urlopen(link+row.find('a').get('href'))
				voiv_soup = BeautifulSoup(voiv)
				powiaty_tab = voiv_soup.find(id = 's0')
				for row in powiaty_tab.find('tbody'):
					if row.find('a') != -1:
						c = City()
						c.name = row.find('a').contents[0]
						c.voiv = v
						c.save()
#						print("."+row.find('a').contents[0]).encode('utf8')
						if (" m." in row.find('a').contents[0] or "Zagranica" in row.find('a').contents[0] or "Statki" in row.find('a').contents[0]):
							t = ParseComm(row.find('a').get('href'),c)
							threads.append(t)
							t.start()
#							city = urllib.urlopen(link+row.find('a').get('href'))
#							city_soup = BeautifulSoup(city)
#							okreg_tab = city_soup.find(id = 's0')
#							for row in okreg_tab.find('tbody'):
#								if row.find('a') != -1 and not row.find('a') is None:
#									com = Commission()
#									com.name = row.find('a').contents[0]
#									com.dist = c; 
#									com.save()
#									processed_com+=1
#									print(str(processed_com)+" .."+com.name).encode('utf8')

						else:
							t = ParseCounty(row.find('a').get('href'),c)
							threads.append(t)
							t.start()
							county = urllib.urlopen(link+row.find('a').get('href'))
#							county_soup = BeautifulSoup(county)
#							county_tab = county_soup.find(id = 's0')
#							for row in county_tab.find('tbody'):
#								if row.find('a') != -1:
#									cnty = County()
#									cnty.name = row.find('a').contents[0]
#									cnty.city = c
#									cnty.save()
#									print(".."+cnty.name).encode('utf8')
#									appendix = row.find('a').get('href')
#									cn = urllib.urlopen(link+appendix)
#									cn_soup = BeautifulSoup(cn)
#									cn_tab = cn_soup.find(id = 's0')
#									for row in cn_tab.find('tbody'):
#										if row.find('a') != -1:
#											com = Commission()
#											com.name = row.find('a').contents[0]
#											com.dist = cnty
#											com.save()
#											processed_com+=1
#											print(str(processed_com)+" ..."+com.name).encode('utf8')
		for t in threads:
			t.join()
