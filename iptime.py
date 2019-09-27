
import requests
import sys
import re
from colorama import Fore

#iptime IP, ID, pwd, 변경할 SSID 입력
if len(sys.argv) is not 5:
   print(Fore.YELLOW+"[-] Example: python iptime.py <Target IP> <ID> <Password> <ssid>"+Fore.RESET)
   sys.exit()

target=sys.argv[1]
ID=sys.argv[2]
Password=sys.argv[3]
SSID=sys.argv[4]


data = 'init_status=1&captcha_on=0&captcha_file=&username=' + ID + '&passwd=' + Password + '&default_passwd=Password+is+%27admin%27.+Change+the+password.&captcha_code='
url = 'http://' + target + '/sess-bin/login_handler.cgi'
#burpsuite 를 위한 프록시 설정
proxies = {'http':'http://localhost:8080', 'https':'http://localhost:8080'}

#Login
s=requests.Session()
req=s.post(url, data=data, proxies=proxies)

#cookie 값 추출
script = re.search('(\'.*\')', req.text, re.I|re.S)
script = script.group()
cookie = re.sub('\'', '', script)

cookies = {'efm_session_id' : cookie}

#SSID 변경
data = 'tmenu=iframe&smenu=hiddenwlsetup&wlmode=0&wlmodetxt=2g&action=allsubmit&sidx=0&uiidx=0&ssid=' + SSID + '&autochannel=1&ctlchannel=9&cntchannel=11&ch_no_change=1&chandisable=0&rwarning=l&dfswarning=l&run=1&mbsspolicy=0&txrate=0&rxrate=0&qosenable=0&useenterprise=0&radiusserver=&radiussecret=&radiusport=1812&enterpriselist=wpa2_aes&personallist=nouse&wpapsk=&wepkey=&broadcast=1&lpchannel=36%3A*%2C40%3A*%2C44%3A*.48%3A*&txpower=100&beacon=100&wpsmode=1&ldpc=1&wmm=1&dynchannel=0&dcsperiodhour=2&wirelessmode=6&country=KR&channelwidth=40&muflag=0&realchanwidth=40'
req=s.get('http://' + target + '/sess-bin/login.cgi', cookies=cookies, proxies=proxies)
req=s.post('http://' + target + '/sess-bin/timepro.cgi', cookies=cookies, data=data, proxies=proxies)
