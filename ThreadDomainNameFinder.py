#!/usr/bin/python
'''
Description:
Find valuable domain name and mail me if found.
  
'''

import socket, time, thread
import urllib2
import re
import time
import random
import threading
from multiprocessing.dummy import Pool as ThreadPool

USER_AGENT_LIST = [\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",\
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",\
		"Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; Windows NT 5.1; SV1; .NET CLR 1.0.3705; .NET CLR 1.1.4322; Media Center PC 3.1)",\
		"Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; Windows NT 5.1; SV1; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",\
		"Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; Windows NT 5.1; SV1)",\
		"Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1; SV1; .NET CLR 1.1.4322; InfoPath.1)",\
		"Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; GTB7.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)",\
		"Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)",\
		"Mozilla/5.0 (X11; U; Linux; cs-CZ) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.4 (Change: 333 41e3bc6)",\
		"Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.4 (Change: )",\
		"Mozilla/5.0 (Windows; U; Windows NT 6.0; de-DE) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.4 (Change: )",\
		"Mozilla/5.0 (Windows; U; Windows NT 5.2; pt-BR) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.4 (Change: )",\
		"Mozilla/5.0 (Windows; U; Windows NT 5.1; de-DE) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.4 (Change: )",\
		]

all_proxy_list=[
		"23.94.37.50:3128",
		"24.143.198.188:80",
		"121.193.143.249:80",
		"120.195.194.10:80",
		"120.195.194.149:80",
		"27.46.52.31:9797",
		"58.251.47.101:8081",
		"120.195.199.240:80",
		"120.195.198.6:80",
		"120.195.203.132:80",
		"218.92.227.165:29037",
		"120.195.192.83:80",
		"60.191.153.75:3128",
		"218.92.227.166:15275",
		"120.195.195.71:80",
		"110.73.1.241:8123",
		"182.90.80.80:8123",
		"123.72.99.94:8118",
		"117.135.250.138:8080",
		"122.193.14.102:80",
		"122.193.14.114:80",
		"122.193.14.85:80",
		"202.123.106.26:80",
		"115.28.7.20:81",
		"218.213.166.218:81",
		"122.193.14.110:80",
		"118.189.69.34:3128",
		"58.248.137.228:80",
		"110.73.36.236:8123",
		"125.117.44.16:8888",
		"121.69.23.134:8118",
		"171.37.135.214:8123",
		"110.72.28.64:8123",
		"182.90.0.140:80",
		"110.72.46.48:8123",
	]
proxy_list = []
total_url_amount = 0

allChars = [chr(i) for i in range(97,123)]
allChars.extend(range(1,10))
URL_TEMPLATE = r"http://checkdomain.xinnet.com/domainCheck?searchRandom=5&prefix=%s&suffix=.%s"
MATCH_TEMPLATE = r"### MATCHED AT %s ###    DOMAIN NAME:%s"
HAS_MATCHED = False
queryIndex = 0
domainKeywords = []
TARGET_DOMAINS=["cn","com"]
pattern = re.compile(r'.*"yes":\[.+\],"no"')

def isPortAvailable(ip,port):
	socket.setdefaulttimeout(2)
	try:
		if port>=65535:
			return False
		s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		result=s.connect_ex((ip,port))
		if result==0:
			return True
		else:
			return False
	except:
		return False
	finally:
		s.close()

def isProxyAvailable(ipAndPort):
	(ip,port) = ipAndPort.split(":")
	if(len(port)>0):
		return isPortAvailable(ip,int(port))
	else:
		return False

def checkDomainName(inputVal):
	global queryIndex,total_url_amount,HAS_MATCHED,fileHandler
	(keyword,url) = inputVal
	ag = random.choice(USER_AGENT_LIST)
	while(True):
		enableProxy = random.choice([True,True,True,True,True,False])
		if(enableProxy):
			proxy = random.choice(proxy_list)
			urlhandle = urllib2.ProxyHandler({'http':proxy})
			opener = urllib2.build_opener(urlhandle)
		else:
			proxy="NO PROXY"
			opener = urllib2.build_opener()
		opener.addheaders = [('User-agent',ag )]
		try:
			result = opener.open(url).read()
			break
		except:
			print("[DEBUG:] Fail with proxy:%s" %(proxy))
	if pattern.match(result):
		lock.acquire()
		HAS_MATCHED = True
		f.write(MATCH_TEMPLATE %(time.ctime(),keyword))
		f.write('\n')
		lock.release()
	
	lock.acquire()
	queryIndex+=1
	print("[DEBUG:] proxy:%s, agent:%s" %(proxy,ag))
	print "[%s/%s] HAS MATCHED:%s, Current domain:%s" %(queryIndex,total_url_amount,str(HAS_MATCHED),keyword)
	lock.release()

def initialize():
	for proxy in all_proxy_list:
		if isProxyAvailable(proxy):
			proxy_list.append(proxy)
	print("[DEBUG:] all accessible proxy is:"+str(len(proxy_list)))

####### Main #######
initialize()
fileHandler=open('domainFinderResult.txt','w')
lock = threading.Lock()
#Put all domains I'm interested in into domainKeywords
for i in allChars:
	char1 = str(i)
	for j in allChars:
		char2 = str(j)
		domainKeywords.append(char1+char2)
		for k in allChars:
			char3 = str(k)
			domainKeywords.append(char1+char2+char3)
total_url_amount = len(domainKeywords)*len(TARGET_DOMAINS)
pool = ThreadPool(5)
querySet = []
for domain in TARGET_DOMAINS:
	for keyword in domainKeywords: 
		url =  URL_TEMPLATE %(keyword,domain)
		querySet.append((keyword+"."+domain,url))
		#url =  URL_TEMPLATE %(keyword,domain)
		#checkDomainName(keyword+"."+domain,url)
results = pool.map(checkDomainName, querySet)
pool.close() 
pool.join() 
fileHandler.close()
