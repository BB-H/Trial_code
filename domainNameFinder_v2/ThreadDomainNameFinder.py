#!/usr/bin/python
'''
Description:
Find valuable domain name and mail me if found.
  
'''

import socket, time, thread,sys
import urllib2
import re
import time
import random
import threading
from ProxyManager import ProxyManager as HttpProxyManager
from ProxyManager import ProxyInfo
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


proxy_list = []
total_url_amount = 0
lock = threading.Lock()
httpProxyManager = HttpProxyManager()
allChars = [chr(i) for i in range(97,123)]
allChars.extend(range(1,10))
URL_TEMPLATE = r"http://checkdomain.xinnet.com/domainCheck?searchRandom=5&prefix=%s&suffix=.%s"
MATCH_TEMPLATE = r"### MATCHED AT %s ###    DOMAIN NAME:%s"
HAS_MATCHED = False
queryIndex = 0
domainKeywords = []
TARGET_DOMAINS=["cn","com"]
pattern = re.compile(r'.*"yes":\[.+\],"no"')

def checkDomainName(domainInfo):
	global queryIndex,total_url_amount,HAS_MATCHED
	(keyword,url) = domainInfo
	ag = random.choice(USER_AGENT_LIST)
	while(True):
		enableProxy = random.choice([True,True,True,True,True,True,True,True,True,False])
		validProxyAmount = httpProxyManager.getValidProxyAmount()
		if validProxyAmount < 1:
			enableProxy=False
		opener = None
		if(enableProxy):
			proxyInfo = httpProxyManager.getRandomProxyInfo()
			if(proxyInfo is not None):
				urlhandle = urllib2.ProxyHandler({'http':proxyInfo.getProxy()})
				opener = urllib2.build_opener(urlhandle)
		if opener is None:
			proxyInfo = ProxyInfo("NO PROXY",-1)
			opener = urllib2.build_opener()
		opener.addheaders = [('User-agent',ag )]
		try:
			result = opener.open(url).read()
			break
		except:
			lock.acquire()
			#print("[DEBUG:] Fail with proxy:%s at %s times" %(proxyInfo.getProxy(),proxyInfo.getFailedTimes()))
			if validProxyAmount>=1:
				httpProxyManager.onProxyFailure(proxyInfo)
			else:
				print "!!! Network failed without any valide proxy !!! "
				sys.exit("Program stoped.")
			lock.release()
			
	if pattern.match(result):
		lock.acquire()
		HAS_MATCHED = True
		f.write(MATCH_TEMPLATE %(time.ctime(),keyword))
		f.write('\n')
		lock.release()
	
	lock.acquire()
	queryIndex+=1
	print("[DEBUG:] proxy:%s, agent:%s" %(proxyInfo.getProxy(),ag))
	print "[INFO:] (%s/%s) HAS MATCHED:%s, Current domain:%s" %(queryIndex,total_url_amount,str(HAS_MATCHED),keyword)
	lock.release()

def initialize():
	'''
	print("[DEBUG] Checking availability of HTTP proxies, please waiting for few minutes...")
	threadAmount = max(len(all_proxy_list)/5,2)
	pool = ThreadPool(threadAmount)
	pool.map(checkProxyAvailable,all_proxy_list)
	pool.close() 
	pool.join()
	print("[DEBUG:] all accessible proxy is:"+str(len(proxy_list)))'''

####### Main #######
print("Start at %s." %time.ctime())
#initialize()
fileHandler=open('domainFinderResult.txt','w')
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
maxThreadCount = max(2,httpProxyManager.getValidProxyAmount()/3)
threadCount = min(maxThreadCount,30)
pool = ThreadPool(threadCount)
print("[DEBUG] Open %s threads for domain name scanning" %threadCount)
querySet = []
for domain in TARGET_DOMAINS:
	for keyword in domainKeywords: 
		url =  URL_TEMPLATE %(keyword,domain)
		querySet.append((keyword+"."+domain,url))
		#url =  URL_TEMPLATE %(keyword,domain)
		#checkDomainName(keyword+"."+domain,url)
pool.map(checkDomainName, querySet)
pool.close() 
pool.join() 
print("Complete at %s." %time.ctime())
fileHandler.close()
