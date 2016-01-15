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
		"218.95.80.93:9000",
		"182.101.221.0:9000",
		"112.195.108.9:9000",
		"218.87.116.152:9000",
		"125.119.218.245:9000",
		"101.206.17.161:9000",
		"220.176.66.246:9000",
		"115.208.152.8:8090",
		"218.95.50.72:9000",
		"183.130.79.92:9000",
		"183.23.218.100:8090",
		"112.195.81.12:9000",
		"218.65.67.185:9000",
		"27.220.54.206:9000",
		"112.195.83.255:9000",
		"120.195.198.49:80",
		"120.195.193.43:80",
		"125.40.224.24:9000",
		"1.60.157.5:9000",
		"59.62.36.71:9000",
		"171.38.42.114:8123",
		"115.223.249.204:9000",
		"120.195.196.167:80",
		"221.227.38.59:8090",
		"120.52.73.26:8080",
		"115.150.14.52:9000",
		"221.131.114.45:80",
		"116.27.105.56:8090",
		"117.25.72.99:8090",
		"114.224.147.221:8090",
		#------
		"195.154.231.43:3128",
		"198.169.246.30:80",
		"81.94.162.140:8080",
		"181.48.0.173:8081",
		"81.95.182.31:80",
		"64.26.95.14:8080",
		"80.83.18.250:8080",
		"43.243.112.79:3128",
		"103.251.14.2:8080",
		"189.15.13.80:3128",
		"125.99.100.10:8080",
		"200.213.158.51:8080",
		"31.192.134.174:8080",
		"200.113.19.21:8080",
		"94.200.231.130:8080",
		"187.49.112.38:8080",
		"189.41.222.171:3128",
		"1.255.102.4:3128",
		"189.15.13.187:3128",
		"177.223.12.121:8080",
		#-----------
		"182.253.37.219:8080",
		"109.163.241.38:3128",
		"182.253.123.23:8080",
		"202.70.86.249:8080",
		"181.198.62.115:8888",
		"210.57.214.46:3128",
		"46.219.116.2:8081",
		"78.8.51.195:8080",
		"89.251.43.19:8080",
		"178.33.191.53:3128",
		"185.5.222.121:8080",
		"187.49.114.33:8080",
		"180.248.18.93:8080",
		"61.19.82.138:8080",
		"69.143.93.173:3128",
		"186.46.2.214:8080",
		"180.250.99.52:8080",
		"177.128.224.242:3128",
		"74.93.239.90:8080",
		"45.115.175.244:80",
		"14.102.41.51:8080",
		"201.65.70.183:3128",
		"37.157.142.7:8080",
		"50.232.32.3:3129",
		"202.146.237.218:80",
		"92.38.126.149:8080",
		"95.46.0.53:8080",
		"177.70.95.162:3128",
		"182.253.130.29:8080",
		"49.228.205.185:8080",
		"45.115.173.12:80",
		"177.200.82.186:8080",
		"176.106.145.122:8080",
		"41.162.48.12:3128",
		"137.135.166.225:8118",
		"41.42.229.235:8080",
		"110.172.146.4:8080",
		"36.73.62.58:80",
		"177.72.81.56:8080",
		"58.27.132.50:8080",
		"112.143.5.152:80",
		"66.23.230.117:3128",
		"36.85.77.159:8080",
		"200.60.24.42:8080",
		"195.140.157.138:443",
		"183.88.120.177:8080",
		"36.76.101.156:8080",
		"36.81.91.184:8080",
		"113.53.84.5:8080",
		"36.80.235.16:8080",
		"36.70.182.160:8080",
		"118.173.108.65:8080",
		"216.68.91.2:8080",
		"36.72.127.135:8080",
		"36.84.116.65:8080",
		"177.223.168.155:8080",
		"200.119.222.130:8080",
		"177.75.232.13:8080",
		"36.66.193.250:80",
		"110.139.93.144:80",
		"182.253.177.132:3128",
		"101.128.120.237:8080",
		"45.117.75.81:8080",
		"89.163.129.222:3128",
		"125.25.81.4:8080",
		"202.162.42.108:8080",
		"177.15.72.142:8080",
		"36.73.207.14:8080",
		"201.132.162.38:8080",
		"177.206.175.46:8080",
		"182.253.180.72:8080",
		"177.75.232.8:8080",
		"49.228.194.194:8080",
		"202.162.42.104:8080",
		"188.243.111.179:8080",
		"61.19.30.198:8080",
		"202.78.206.83:8080",
		"95.158.139.48:8080",
		"180.250.57.227:8080",
		"190.85.155.172:8080",
		"203.24.76.70:80",
		"212.250.159.3:8080",
		"122.102.45.106:80",
		"200.76.191.213:3128",
		#----------
		"217.15.140.158:8080",
		"101.128.100.72:8080",
		"92.222.201.209:8080",
		"213.149.10.98:8080",
		"36.80.199.84:8080",
		"46.23.51.77:8080",
		"125.24.79.190:8080",
		"36.80.114.9:8080",
		"180.248.102.65:8080",
		"36.83.0.194:8080",
		"60.254.32.1:8080",
		"177.85.92.136:3128",
		"116.213.51.90:8080",
		"200.1.181.126:8080",
		"36.78.26.4:8080",
		"190.121.148.247:8080",
		"156.99.125.181:9090",
		"202.129.29.130:8080",
		"187.0.183.69:3128",
		"111.221.105.87:3128",
		"202.162.200.9:8080",
		"110.77.217.71:8888",
		"212.108.129.22:3128",
		"176.100.119.26:80",
		"186.67.193.194:8081",
		"27.131.47.132:8080",
		"85.10.53.90:8080",
		"118.97.191.206:8080",
		"188.138.89.172:701",
		"177.128.225.193:8080",
		"85.143.164.100:81",
		"213.147.119.246:8080",
		"213.147.119.242:8080",
		"213.147.124.84:8080",
		"190.54.44.204:3128",
		"103.249.91.1:8080",
		"212.126.99.42:8080",
		"190.223.56.50:80",
		"1.0.246.156:8080",
		"74.143.193.83:3128",
		"111.90.189.118:8080",
		"87.106.60.13:3128",
		"210.1.81.48:8888",
		"187.114.138.9:8080",
		"176.237.224.60:8080",
		"190.121.158.114:8080",
		"200.164.85.12:80",
		"190.144.92.82:8080",
		"178.211.182.111:8080",
		"188.56.147.158:8080",
		"201.19.32.231:8080",
		"201.151.151.222:8080",
		"202.152.148.116:8080",
		"190.166.230.2:80",
		"101.51.209.182:8080",
		"27.254.47.203:80",
		"180.242.1.93:8080",
		"110.77.211.226:8080",
		"177.223.0.27:8080",
		"180.246.77.65:8080",
		"192.118.77.187:80",
		"85.159.224.91:8080",
		"177.23.85.202:8080",
		"187.49.114.1:8080",
		"93.183.155.39:8080",
		"45.115.175.198:80",
		"177.194.145.79:8080",
		"110.77.217.132:8080",
		"98.226.154.95:8080",
		"177.85.7.126:8080",
		"84.22.46.25:8080",
		"81.219.209.1:8080",
		"36.73.177.144:3128",
		"94.23.199.127:4444",
		"101.108.158.222:8080",
		"202.159.43.105:8080",
		"186.109.215.190:8080",
		"119.42.115.114:8080",
		#--------
		"186.109.215.190:8080",
		"119.42.115.114:8080",
		"177.57.155.202:8080",
		"163.53.186.218:8080",
		"74.208.221.242:3128",
		"190.31.141.74:8080",
		"36.80.50.223:3128",
		"1.4.212.253:8080",
		"189.201.242.101:8080",
		"190.167.243.14:8080",
		"187.33.48.165:8080",
		"110.77.182.169:8080",
		"190.82.90.230:3128",
		"117.211.21.167:8080",
		"36.80.210.232:80",
		"217.150.52.221:8123",
		"180.249.157.44:3128",
		"36.74.132.251:8080",
		"36.80.59.234:1080",
		"92.115.163.219:8080",
		"189.48.64.22:8080",
		"87.98.221.137:4050",
		"202.21.183.118:8080",
		"188.166.213.49:3128",
		"49.1.244.139:3128",
		"181.15.150.10:3128",
		"121.119.185.45:3128",
		"190.40.19.48:3128",
		"45.115.174.245:80",
		"116.58.254.207:8080",
		"125.163.232.64:8080",
		"222.124.201.189:8080",
		"182.253.223.140:8080",
		"186.103.222.196:8080",
		"186.235.174.243:8080",
		"47.88.139.96:3128",
		"125.99.100.13:8080",
		"192.118.77.186:80",
		"190.117.181.60:8080",
		"182.253.177.29:8080",
		"36.81.39.220:8080",
		"201.16.244.227:3128",
		"36.72.103.159:8080",
		"177.70.94.150:3128",
		"180.252.95.100:80",
		"185.28.193.95:8080",
		"45.116.174.168:8888",
		"36.80.239.195:80",
		"198.96.90.157:3128",
		"36.80.112.41:80",
		"176.239.120.28:8080",
		"182.253.177.86:8080",
		"110.138.38.14:8080",
		"201.48.0.61:3128",
		"222.124.142.108:8080",
		"177.223.173.128:80",
		"45.78.25.214:3128",
		"177.124.175.222:3130",
		"36.73.18.28:8080",
		"190.0.59.246:8080",
		"36.68.40.17:8080",
		"182.253.154.80:8080",
		"200.46.94.202:3128",
		"200.229.225.185:8080",
		"182.30.224.74:8080",
		"36.73.19.39:8080",
		"201.175.48.28:8080",
		"103.15.62.113:8080",
		"122.255.120.250:8080",
		"213.27.152.15:3128",
		"125.24.111.6:8080",
		"36.74.129.118:8080",
		"36.74.221.132:8080",
		"36.74.136.233:8080",
		"95.65.116.73:8118",
		"202.72.215.170:9876",
		"94.100.49.2:8080",
		"1.179.185.253:8080",
		"58.180.45.119:3128",
		"177.85.7.252:8080",
		"120.89.95.211:80",
		"110.77.208.9:3128",
		"174.142.210.197:3128",
		"181.48.158.10:12345",
		"180.246.75.243:8080",

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
lock = threading.Lock()

def isPortAvailable(ip,port):
	socket.setdefaulttimeout(1)
	try:
		if port>=65535:
			return False
		s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		result=s.connect_ex((ip,port))
		if result==0:
			return True
	except:
		return False
	finally:
		s.close()

def checkProxyAvailable(ipAndPort):
	global proxy_list,lock
	(ip,port) = ipAndPort.split(":")
	if(len(port)>0):
		if isPortAvailable(ip,int(port)):
			lock.acquire()
			proxy_list.append(ipAndPort)
			lock.release()
	

def checkDomainName(domainInfo):
	global queryIndex,total_url_amount,HAS_MATCHED,fileHandler
	(keyword,url) = domainInfo
	ag = random.choice(USER_AGENT_LIST)
	while(True):
		enableProxy = random.choice([True,True,True,True,True,True,True,True,True,False])
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
			lock.acquire()
			print("[DEBUG:] Fail with proxy:%s" %(proxy))
			lock.release()
	if pattern.match(result):
		lock.acquire()
		HAS_MATCHED = True
		f.write(MATCH_TEMPLATE %(time.ctime(),keyword))
		f.write('\n')
		lock.release()
	
	lock.acquire()
	queryIndex+=1
	print("[DEBUG:] proxy:%s, agent:%s" %(proxy,ag))
	print "[INFO:] (%s/%s) HAS MATCHED:%s, Current domain:%s" %(queryIndex,total_url_amount,str(HAS_MATCHED),keyword)
	lock.release()

def initialize():
	print("[DEBUG] Checking availability of HTTP proxies, please waiting for few minutes...")
	threadAmount = max(len(all_proxy_list)/5,2)
	pool = ThreadPool(threadAmount)
	pool.map(checkProxyAvailable,all_proxy_list)
	pool.close() 
	pool.join()
	print("[DEBUG:] all accessible proxy is:"+str(len(proxy_list)))

####### Main #######
print("Start at %s." %time.ctime())
initialize()
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
threadCount = len(proxy_list)/3
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
