#!/usr/bin/python
'''
Description:
Find valuable domain name and mail me if found.
  
'''

import urllib2
import re
import time
import random

USER_AGENT_LIST = [\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",\
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",\
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",\
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",\
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",\
		"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB6; Acoo Browser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",\
		"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)",\
		"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",\
		"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; GTB5; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",\
		"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)",\
		"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Acoo Browser; InfoPath.2; .NET CLR 2.0.50727; Alexa Toolbar)",\
		"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Acoo Browser; .NET CLR 2.0.50727; .NET CLR 1.1.4322)",\
		"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Acoo Browser; .NET CLR 1.0.3705; .NET CLR 1.1.4322; .NET CLR 2.0.50727; FDM; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; InfoPath.2)",\
		"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; Acoo Browser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",\
		"Mozilla/4.0 (compatible; MSIE 7.0; America Online Browser 1.1; rev1.5; Windows NT 5.1; .NET CLR 1.1.4322)",\
		"Mozilla/4.0 (compatible; MSIE 7.0; America Online Browser 1.1; rev1.5; Windows NT 5.1; .NET CLR 1.0.3705; .NET CLR 1.1.4322; Media Center PC 4.0; InfoPath.1; .NET CLR 2.0.50727; Media Center PC 3.0; InfoPath.2)",\
		"Mozilla/4.0 (compatible; MSIE 7.0; America Online Browser 1.1; rev1.2; Windows NT 5.1; SV1; .NET CLR 1.1.4322)",\
		"Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; Windows NT 5.1; SV1; HbTools 4.7.0)",\
		"Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; Windows NT 5.1; SV1; FunWebProducts; .NET CLR 1.1.4322; InfoPath.1; HbTools 4.8.0)",\
		"Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; Windows NT 5.1; SV1; FunWebProducts; .NET CLR 1.0.3705; .NET CLR 1.1.4322; Media Center PC 3.1)",\
		"Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; Windows NT 5.1; SV1; .NET CLR 1.1.4322; HbTools 4.7.1)",\
		"Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; Windows NT 5.1; SV1; .NET CLR 1.1.4322)",\
		"Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; Windows NT 5.1; SV1; .NET CLR 1.0.3705; .NET CLR 1.1.4322; Media Center PC 3.1)",\
		"Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; Windows NT 5.1; SV1; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",\
		"Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; Windows NT 5.1; SV1)",\
		"Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; Windows NT 5.1; FunWebProducts; (R1 1.5); HbTools 4.7.7)",\
		"Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; Windows NT 5.1; FunWebProducts)",\
		"Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; Windows NT 5.1)",\
		"Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; Windows NT 5.0)",\
		"Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; Windows 98)",\
		"Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1; SV1; FunWebProducts; .NET CLR 1.1.4322)",\
		"Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; rev1.5; Windows NT 5.1; SV1; .NET CLR 1.1.4322; InfoPath.1)",\
		"Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; GTB7.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)",\
		"Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)",\
		"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.7; AOLBuild 4343.19; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)",\
		"Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.6; AOLBuild 4340.130; Windows NT 5.1; Trident/4.0; FunWebProducts; GTB6.6; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; yie8)",\
		"Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.6; AOLBuild 4340.12; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)",\
		"Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.6; AOLBuild 4340.12; Windows NT 5.1; Trident/4.0; GTB6.3)",\
		"Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.6; AOLBuild 4340.124; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)",\
		"Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.6; AOLBuild 4340.122; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; MS-RTC LM 8)",\
		"Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.6; AOLBuild 4340.122; Windows NT 5.1; Trident/4.0; FunWebProducts)",\
		"Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.6; AOLBuild 4340.111; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)",\
		"Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.6; AOLBuild 4340.110; Windows NT 5.1; Trident/4.0; .NET CLR 1.0.3705; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)",\
		"Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.6; AOLBuild 4340.104; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.5.30729)",\
		"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.6; AOLBuild 4340.128; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022)",\
		"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.42; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)",\
		"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.40; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30618)",\
		"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.40; Windows NT 6.0; FunWebProducts; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506; .NET CLR 1.1.4322)",\
		"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.40; Windows NT 5.1; Trident/4.0; GTB6; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 1.1.4322)",\
		"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.40; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 1.1.4322)",\
		"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.36; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.30618; .NET CLR 3.5.30729)",\
		"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.36; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30618; .NET CLR 1.1.4322)",\
		"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.36; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30618)",\
		"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.1; AOLBuild 4334.36; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",\
		"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.1; AOLBuild 4334.34; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506; .NET CLR 1.1.4322)",\
		"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.1; AOLBuild 4334.34; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 3.0.04506; .NET CLR 1.1.4322)",\
		"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.1; AOLBuild 4334.34; Windows NT 5.1; .NET CLR 1.1.4322)",\
		"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.1; AOLBuild 4334.34; Windows NT 5.1; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",\
		"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.1; AOLBuild 4334.27; Windows NT 6.0; WOW64; SLCC1; .NET CLR 2.0.50727; .NET CLR 3.0.04506; Media Center PC 5.0); UnAuth-State",\
		"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.1; AOLBuild 4334.27; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 3.0.04506); UnAuth-State",\
		"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.1; AOLBuild 4334.27; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; InfoPath.1); UnAuth-State",\
		"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.1; AOLBuild 4327.65535; Windows NT 5.1; .NET CLR 1.0.3705; .NET CLR 1.1.4322; .NET CLR 2.0.50727); UnAuth-State",\
		"Mozilla/4.0 (compatible; MSIE 6.0; AOL 9.1; AOLBuild 4334.5006; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)",\
		"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.0; Windows NT 6.0; FunWebProducts; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506; Seekmo 10.0.341.0)",\
		"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.0; Windows NT 6.0; FunWebProducts; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; SLCC1; .NET CLR 2.0.50727; .NET CLR 3.0.04506)",\
		"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.0; Windows NT 5.1; Trident/4.0; GTB6; FunWebProducts; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)",\
		"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.0; Windows NT 5.1; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322)",\
		"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.0; Windows NT 5.1; InfoPath.1)",\
		"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.0; Windows NT 5.1; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.0.3705; .NET CLR 1.1.4322; Media Center PC 4.0)",\
		"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.0; Windows NT 5.1; GTB5; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)",\
		"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.0; Windows NT 5.1; GTB5; .NET CLR 1.1.4322; .NET CLR 2.0.50727; OfficeLiveConnector.1.3; OfficeLivePatch.0.0)",\
		"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.0; Windows NT 5.1; GTB5; .NET CLR 1.1.4322)",\
		"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.0; Windows NT 5.1; GTB5; .NET CLR 1.0.3705; .NET CLR 2.0.50727)",\
		"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.0; Windows NT 5.1; FunWebProducts; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) )",\
		"Mozilla/4.0 (compatible; MSIE 6.0; AOL 8.0; Windows NT 5.1; SV1; (R1 1.3); .NET CLR 1.1.4322)",\
		"Mozilla/4.0 (compatible; MSIE 6.0; AOL 8.0; Windows NT 5.1; SV1)",\
		"Mozilla/4.0 (compatible; MSIE 6.0; AOL 8.0; Windows NT 5.1; Q312461)",\
		"Mozilla/4.0 (compatible; MSIE 6.0; AOL 8.0; Windows NT 5.1; FunWebProducts; SV1; .NET CLR 1.0.3705)",\
		"Mozilla/4.0 (compatible; MSIE 6.0; AOL 8.0; Windows NT 5.1; FunWebProducts; SV1)",\
		"Mozilla/4.0 (compatible; MSIE 6.0; AOL 8.0; Windows NT 5.1; FunWebProducts)",\
		"Mozilla/4.0 (compatible; MSIE 6.0; AOL 8.0; Windows NT 5.1; .NET CLR 1.1.4322)",\
		"Mozilla/4.0 (compatible; MSIE 6.0; AOL 8.0; Windows NT 5.1; .NET CLR 1.0.3705)",\
		"Mozilla/4.0 (compatible; MSIE 6.0; AOL 8.0; Windows NT 5.1; (R1 1.3))",\
		"Mozilla/4.0 (compatible; MSIE 6.0; AOL 8.0; Windows NT 5.1)",\
		"Mozilla/4.0 (compatible; MSIE 6.0; AOL 8.0; Windows NT 5.0)",\
		"Mozilla/4.0 (compatible; MSIE 6.0; AOL 7.0; Windows NT 5.1; Hotbar 4.2.8.0)",\
		"Mozilla/4.0 (compatible; MSIE 6.0; AOL 7.0; Windows NT 5.1; Hotbar 4.1.7.0)",\
		"Mozilla/4.0 (compatible; MSIE 6.0; AOL 7.0; Windows NT 5.1; .NET CLR 1.0.3705)",\
		"Mozilla/4.0 (compatible; MSIE 6.0; AOL 7.0; Windows NT 5.1)",\
		"Mozilla/4.0 (compatible; MSIE 6.0; AOL 7.0; Windows NT 5.0)",\
		"Mozilla/4.0 (compatible; MSIE 6.0; AOL 7.0; Windows 98; Win 9x 4.90; .NET CLR 1.1.4322)",\
		"Mozilla/4.0 (compatible; MSIE 6.0; AOL 7.0; Windows 98; Win 9x 4.90; (R1 1.3))",\
		"Mozilla/4.0 (compatible; MSIE 6.0; AOL 7.0; Windows 98; Win 9x 4.90)",\
		"Mozilla/5.0 (X11; U; Linux; en-GB) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.4 (Change: 388 835b3b6)",\
		"Mozilla/5.0 (X11; U; Linux; en-GB) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.4",\
		"Mozilla/5.0 (X11; U; Linux; de-DE) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.4",\
		"Mozilla/5.0 (X11; U; Linux; cs-CZ) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.4 (Change: 333 41e3bc6)",\
		"Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.4 (Change: )",\
		"Mozilla/5.0 (Windows; U; Windows NT 6.0; de-DE) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.4 (Change: )",\
		"Mozilla/5.0 (Windows; U; Windows NT 5.2; pt-BR) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.4 (Change: )",\
		"Mozilla/5.0 (Windows; U; Windows NT 5.1; de-DE) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.4 (Change: )",\
		]

allChars = [chr(i) for i in range(97,123)]
allChars.extend(range(1,10))
URL_TEMPLATE = r"http://checkdomain.xinnet.com/domainCheck?searchRandom=5&prefix=%s&suffix=.%s"
MATCH_TEMPLATE = r"### MATCHED AT %s ###\n DOMAIN NAME:%s\n"
domainKeywords = []
TARGET_DOMAINS=["cn","com"]


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
index = 1
matched = 0
pattern = re.compile(r'.*"yes":\[.+\],"no"')

for domain in TARGET_DOMAINS:
	for keyword in domainKeywords:
		url =  URL_TEMPLATE %(keyword,domain)
		print "CURRENT:(%s/%s), MATCHED:%s" %(index,url_amount,matched)
		
		ag = random.choice(USER_AGENT_LIST)
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent',ag )]
		result = opener.open(url).read()
		#result = urllib2.urlopen(url).read()
		print(result)
		index+=1
		if pattern.match(result):
			f.write(MATCH_TEMPLATE %(time.ctime(),keyword+"."+domain))
			matched+=1
			print ("\a")#play a voice notification
			print ("\a")

f.close()

