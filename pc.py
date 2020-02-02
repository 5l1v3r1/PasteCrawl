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

def pb_get(pb_id, proxy):
	r = requests.get("https://pastebin.com/raw/" + pb_id, proxies={'http':proxy, 'https':proxy}, timeout=5)
	return r.text

def pb_arch(proxy):
	r = requests.get("https://pastebin.com/archive", proxies={'http':proxy,'https':proxy}, timeout=5)
	return r.text

if len(sys.argv) < 3:
	banner()
	print("Usage : pc.py [keyword] [log.txt] [proxy]")
else:
	proxy = sys.argv[3]
	#for i in proxy:
	#	try:
	#		r = requests.get("https://httpbin.org/ip", proxies={'http': i, 'https': i}, timeout=1)
	#		print(r.text)
	#	except:
	#		print("skip")

	f = open(sys.argv[2],"a")
	f.write("")
	f.close()
	banner()
	while True:
		try:
			file = open(sys.argv[2],"r")
			file_log = file.read().split("\n")

			scrap = bs(pb_arch(proxy), 'html.parser').find_all('table',attrs={'class':'maintable'})
			soup = bs(str(scrap),'html.parser').find_all('a')
			for i in soup:
				if len(i.get('href')) == 9:
					x = pb_get(i.get('href')[1:],proxy)
					print("[*] Checking " + i.get('href')[1:] + " ...")
					if re.search(sys.argv[1], x) and i.get('href')[1:] not in file_log:
						print("[+] Found : http://pastebin.com/raw/" + i.get('href')[1:])
						fh = open(sys.argv[2],"a")
						fh.write(i.get('href')[1:] + "\n")
						fh.close()
						f = open("loot/" + i.get('href')[1:] + "_" + sys.argv[2],"wb")
						f.write(pb_get(i.get('href')[1:],proxy).encode('utf-8'))
						f.close()
		except:
			pass