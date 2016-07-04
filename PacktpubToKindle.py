# https://www.packtpub.com/packt/offers/free-learning
# Works in Python ver. 3.5 and 2.7
# Dependencies : beautifulsoup4, requests, configparser, html5lib

from bs4 import BeautifulSoup
from time import sleep
import urllib
import requests
import platform

version_major = platform.python_version()[0]
url_base='https://www.packtpub.com'
url_login='/packt/offers/free-learning'
url_account='/account/my-ebooks'

try: import configparser as CP
except ImportError:
	import ConfigParser as CP

import os, sys

def isPython2():
	if version_major == '2':
		return True
	else:
		return False

def parseStatus(code):
		if code == 200:
			status = "Good"
		else:
			status = "Bad (" + str(code) + ")"
		return status

def printRespCode(sentence, response):
	status_code = parseStatus(response.status_code)
	print(">> {0}... {1}".format(sentence, status_code))

class PacktpubToKindle(object):
	def __init__(self, config):
		self.config = config
		self.headers = self.initHeaders()
		self.session = requests.Session()
		self.info = {}
		print(">> PacktPub session has been created.")

	def initHeaders(self):
		return {
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	        'Accept-Encoding': 'gzip, deflate',
	        'Connection': 'keep-alive',
	        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
	    }

	def getSoup(self, response):
		status = parseStatus(response.status_code)

		soup = BeautifulSoup(response.text, 'html5lib')
		return soup

	def syncKindle(self):
		url = self.info['url_claim']
		
		response = self.session.get(url, headers = self.headers)
		printRespCode("Claim the latest free-ebook", response)
		soup = self.getSoup(response)
		div_target = soup.find('div', {'id': 'product-account-list'})

		# Choose the latest book just claimed
		div_claimed_book = div_target.select('.product-line')[0]
		title = div_claimed_book.select('.title')[0]
		nid = div_claimed_book['nid']
		print(">> Book title : {0}".format(title.string.strip()))

		# if isPython2() is True:
		# 	answer = raw_input(">> Do you want to synchronize it? (y/n)  ");
		# else:
		# 	answer = input(">> Do you want to synchronize it? (y/n)  ");

		# answer_low = answer.lower();
		# if answer_low == 'yes' or answer_low == 'y':
		# 	pass
		# else:
		# 	print(">> Choose to stop.");
		# 	return;
		


		print(">> Sync \"" + title.string.strip() + " (" + nid + ")\" to your Kindle...")

		kindle_form = soup.find('form', {'id': 'packt-kindle-edit-address-form'})
		data = {
			'form_build_id': []
		}

		data['form_build_id'] = kindle_form.find('input', attrs={'name': 'form_build_id'})['value']
		data['form_token'] = kindle_form.find('input', attrs={'name': 'form_token'})['value']
		data['form_id'] = kindle_form.find('input', attrs={'name': 'form_id'})['value']
		data['book_nid'] = nid
		data['address'] = self.config.get('user', 'user.kindle')
		data['action'] = 'kindle'
		data['op'] = 'Send eBook'
		data['type'] = 'mobi'

		url = url_base + url_account;
		response = self.session.post(url, headers=self.headers, data=data);
		printRespCode("Request sending ebooks in kindle format", response)


		# Here we can get the notice from content if the book has been successfully sent.
		# response = self.session.get(url, headers=self.headers)


	def claimLatestBook(self):
		url_auth = url_base + url_login

		response = self.session.get(url_auth, headers = self.headers)
		printRespCode("Fetching free-ebooks URL", response)		

		soup = self.getSoup(response)

		# Need these user login form to post..
		form = soup.find('form', {'id': 'packt-user-login-form'})
		self.info['form_build_id'] = form.find('input', attrs={'name': 'form_build_id'})['value']
		self.info['form_id'] = form.find('input', attrs={'name': 'form_id'})['value']

		data = self.info.copy()
		data['email'] = self.config.get('user', 'user.email')
		data['password'] = self.config.get('user', 'user.password')
		data['op'] = 'Login'

		response = self.session.post(url_auth, headers = self.headers, data = data)
		printRespCode("Getting authentication", response)

		soup = self.getSoup(response)
		div_target = soup.find('div', {'id': 'deal-of-the-day'})

		title = div_target.select('div.dotd-title > h2')[0].text.strip()

		self.info['title'] = title
		self.info['description'] = div_target.select('div.dotd-main-book-summary > div')[2].text.strip()
		self.info['url_claim'] = url_base + div_target.select('a.twelve-days-claim')[0]['href']


	def run(self):
		self.claimLatestBook()
		self.syncKindle()

def getConfigs(path):
	if not os.path.exists(path):
		raise IOError('File not found')

	config = CP.ConfigParser()
	config.read(path)
	return config

def main():

	print("""
		[Packtpub Free e-Books Synchronizer for Kindle]
		Last update\t: Jun 24 2016
		Written by\t: ins7itia <https://github.com/ins7itia/PacktpubToKindle>
		""")
	config = getConfigs('./config/user')
	pp = PacktpubToKindle(config);

	pp.run()
	print(">> Done")


main()
