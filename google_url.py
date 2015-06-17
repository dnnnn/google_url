import re,requests,BeautifulSoup
from bs4 import BeautifulSoup
import socket,urlparse,argparse
from termcolor import colored

USAGE = "python google_url.py [-p proxy]"
DESC  = "Use PROXY to google some url"
epilog = "david,david,david"
parser = argparse.ArgumentParser(usage=USAGE, description=DESC, epilog=epilog)
parser.add_argument('-p', dest='proxy',
                    help="proxy,support:socks4,socks5,http eg: socks5://127.0.0.1:1234 ")
args = parser.parse_args()

#PROXY CODE START
if args.proxy:
	try:
		proxy = urlparse.urlparse(args.proxy)
		(scheme,host,port) = (proxy.scheme,proxy.hostname,proxy.port)
		print "[ PROXY ]\t"+ scheme + "://" + host + ":" + str(port)
		try:
			import socks
		except ImportError:
		    print("For Proxy Support, Please Download socks.py From Sockipy Project.")
		    sys.exit(1)
		if proxy.scheme == "socks5":
			proxy_type = socks.PROXY_TYPE_SOCKS5
		elif proxy.scheme == "socks4":
			proxy_type = socks.PROXY_TYPE_SOCKS4
		elif proxy.scheme == "http":
			proxy_type = socks.PROXY_TYPE_HTTP
		else:
			print "Unsupported proxy type!"
			sys.exit(1)
		socks.setdefaultproxy(proxy_type, host, port)
		socket.socket = socks.socksocket
	except Exception as e:
		print e
#PROXY CODE END

keyword = "site:gov.cn inurl:aspx?id"
start_mark = "&start="+str(30)
page_urls_num = "&num="+str(20)
search_url = "https://www.google.co.jp/search?q="+keyword+"&ie=utf-8&oe=utf-8&"+start_mark+page_urls_num


try:
	r = requests.get(search_url,timeout=25,verify=False)
except Exception, e:
	print colored("[!]Can't Connect!",'yellow')

soup = BeautifulSoup(r.text)
pre_urls = soup.findAll(attrs={'class':'g'})
print colored("[-]Find Urls Count:"+str(len(pre_urls)),'green')

re_string = r'q=.*?"'
waiting_google_query_url = []

for i in pre_urls:
    tmp_url = re.findall(re_string,str(i))
    for j in tmp_url:
    	waiting_google_query_url.append(j[2:-1])

for i in waiting_google_query_url:
	try:
		tmp_request = requests.get("https://www.google.co.jp/url?q="+i,timeout=25)
	except Exception, e:
		print colored("[!]Can't Connect!",'yellow')
			
	tmp_response_soup = BeautifulSoup(tmp_request.text)
	tmp_href = tmp_response_soup.a['href']
	if ('googleusercontent' not in tmp_href) and len(tmp_href)>8:
		print tmp_href










