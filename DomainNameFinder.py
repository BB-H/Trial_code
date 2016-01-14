#!/usr/bin/python
'''
Description:
Find valuable domain name and mail me if found.
  
'''

import urllib2
import re
import time
import random
import thread
import threading

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

proxy_list=[
		#"23.94.37.50:3128",
		#"24.143.198.188:80",
		"121.193.143.249:80",
		"120.195.194.10:80",
		"120.195.194.149:80",
	]
allChars = [chr(i) for i in range(97,123)]
allChars.extend(range(1,10))
URL_TEMPLATE = r"http://checkdomain.xinnet.com/domainCheck?searchRandom=5&prefix=%s&suffix=.%s"
MATCH_TEMPLATE = r"### MATCHED AT %s ###    DOMAIN NAME:%s"
domainKeywords = []
TARGET_DOMAINS=["cn","com"]


def checkDomainAvaliabilityRemotely(userAgent,url,fileHandler,domainName):
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent',userAgent)]
	result = opener.open(url).read()
	#result = urllib2.urlopen(url).read()
	print(result)
	if pattern.match(result):
		myLock.acquire()
		fileHandler.write(MATCH_TEMPLATE %(time.ctime(),domainName))
		myLock.release()
		print ("\a")#play a voice notification
		print ("\a")
		hasMatched = True

########## MAIN #########
f=open('domainFinderResult.txt','w')

for i in allChars:
	char1 = str(i)
	for j in allChars:
		char2 = str(j)
		#url =  URL_TEMPLATE %(char1+char2,domain)
		domainKeywords.append(char1+char2)
		for k in allChars:
			char3 = str(k)
			#url =  URL_TEMPLATE %(char1+char2+char3,domain)
			domainKeywords.append(char1+char2+char3)


url_amount = len(domainKeywords)*len(TARGET_DOMAINS)
index = 0
matched = 0
pattern = re.compile(r'.*"yes":\[.+\],"no"')

for domain in TARGET_DOMAINS:
	for keyword in domainKeywords:
		url =  URL_TEMPLATE %(keyword,domain)
		ag = random.choice(USER_AGENT_LIST)
		proxy = random.choice(proxy_list)
		print "PROXY:"+proxy
		urlhandle = urllib2.ProxyHandler({'http':proxy})
		index+=1
		print "CURRENT:(%s/%s), HAS MATCHED:%s" %(index,url_amount,matched)
		opener = urllib2.build_opener(urlhandle)
		opener.addheaders = [('User-agent',ag )]
		result = opener.open(url).read()
		print(result)
		if pattern.match(result):
			f.write(MATCH_TEMPLATE %(time.ctime(),keyword+"."+domain))
			f.write('\n')
			matched+=1
		
f.close()

