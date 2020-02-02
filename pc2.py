#!/usr/bin/python

import requests,sys,re
from bs4 import BeautifulSoup as bs
def get_proxies():
	data = []
	r = requests.get("https://free-proxy-list.net/")
	x = bs(r.text, 'html.parser').find('tbody')
	for i in x.find_all('tr'):
		ip   = i.find_all('td')[0].string 
		port = i.find_all('td')[1].string
		data.append(ip + ":" + port)
	return data

def banner():
	print('''
 *********************** ******************
 *     PasteCrawl      * *** By FilthyRoot ********
 * Pastebin DB Crawler * ** Jogjakarta Hacker Link **
 *********************** **************************
''')

def pb_get(pb_id, proxy):
	r = requests.get("https://pastebin.com/raw/" + pb_id, proxies={'http':proxy, 'https':proxy}, timeout=10)
	return r.text

def pb_arch(proxy):
	r = requests.get("https://pastebin.com/archive", proxies={'http':proxy,'https':proxy}, timeout=10)
	return r.text

if len(sys.argv) < 3:
	banner()
	print("Usage : pc.py [keyword] [log.txt]")
else:
	banner()
	while True:
		proxy = get_proxies()
		for ip in proxy:
			try:
				print("[*] Trying " + ip + " ...")
				r = requests.get("https://pastebin.com/", proxies={'http': ip, 'https': ip}, timeout=1)
				print("[+] Got it! " + ip)
			
				f = open(sys.argv[2],"a")
				f.write("{" + ip + "}\n")
				f.close()

				file = open(sys.argv[2],"r")
				file_log = file.read().split("\n")

				scrap = bs(pb_arch(ip), 'html.parser').find_all('table',attrs={'class':'maintable'})
				soup = bs(str(scrap),'html.parser').find_all('a')
				for i in soup:
					if len(i.get('href')) == 9:
						x = pb_get(i.get('href')[1:], ip)
						print("\t[*] Checking " + i.get('href')[1:] + " ...")
						if re.search(sys.argv[1], x) and i.get('href')[1:] not in file_log:
							print("\t\t[+] Found : http://pastebin.com/raw/" + i.get('href')[1:])
							fh = open(sys.argv[2],"a")
							fh.write(i.get('href')[1:] + "\n")
							fh.close()
							f = open("loot/" + i.get('href')[1:] + "_" + sys.argv[2],"wb")
							f.write(pb_get(i.get('href')[1:], ip).encode('utf-8'))
							f.close()

			except:
				pass