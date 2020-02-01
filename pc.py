#!/usr/bin/python

import requests,sys,re
from bs4 import BeautifulSoup as bs

def banner():
	print('''
 *********************** ******************
 *     PasteCrawl      * *** By FilthyRoot ********
 * Pastebin DB Crawler * ** Jogjakarta Hacker Link **
 *********************** **************************
''')

def pb_get(pb_id,log):
	r = requests.get("https://pastebin.com/raw/" + pb_id)
	f = open("loot/" + pb_id + "_" + log,"w")
	f.write(r.text)
	f.close()
	return r.text

def pb_arch():
	r = requests.get("https://pastebin.com/archive")
	return r.text

if len(sys.argv) < 3:
	banner()
	print("Usage : pc.py [keyword] [log.txt]")
else:
	f = open(sys.argv[2],"w")
	f.write("")
	f.close()
	banner()
	while True:
		file = open(sys.argv[2],"r")
		file_log = file.read().split("\n")

		scrap = bs(pb_arch(), 'html.parser').find_all('table',attrs={'class':'maintable'})
		soup = bs(str(scrap),'html.parser').find_all('a')
		for i in soup:
			if len(i.get('href')) == 9:
				x = pb_get(i.get('href')[1:], sys.argv[2])
				if re.search(sys.argv[1], x) and i.get('href')[1:] not in file_log:
					print("[+] Found : http://pastebin.com/raw/" + i.get('href')[1:])
					fh = open(sys.argv[2],"a")
					fh.write(i.get('href')[1:] + "\n")
					fh.close()
