#

import requests
from bs4 import BeautifulSoup
from ghost import Ghost, Session
import threading

##################################################


# 测试并加入ip_list
def add_task(type, ip, port):
    a = threading.Thread(target=test_ip, args=(type, ip, port,))
    threads.append(a)
    a.start()

def test_ip(type, ip, port):
    test_url = 'http://api.ipaddress.com/myip'
    myip = s.get(test_url).text
    proxy = {type: "%s://%s:%s" %(type, ip, port)}
    count = 0
    for i in range(3):
        try:
            r = s.get(test_url, proxies=proxy, timeout=1)
            if r.text == myip:
                print('透明代理%s' % ip)
                break
        except:
            print('%s无法连接！' % ip)
            break
        else:
            count += 1
    if count == 3:
        if r.status_code == 200:
            print('%s加入列表！' % ip)
            ip_list.append((type, ip, port))



UA = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
header = {'User-Agent':UA,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate'
}
s = requests.session()
s.keep_alive = False
gh = Ghost()
se = Session(gh, user_agent=UA, wait_timeout=30, wait_callback=None, display=False, viewport_size=(800, 680), download_images=False)

#################################
# hidemy
def get_hidemy():
    url = 'https://hidemy.name/en/proxy-list/?country=US&type=h&anon=4#list'
    se.open(url)
    se.wait_for_selector('table.proxy__t')
    html = se.content
    soup = BeautifulSoup(html, "html.parser")
    sources = soup.select('tbody > tr')
    for i in sources:
        ip_info = hidemy_info(i)
        add_task(ip_info[0], ip_info[1], ip_info[2])

def hidemy_info(source):
    ip = source.select('td')[0].text
    port = source.select('td')[1].text
    type = 'http'
    return(type, ip, port)

threads = []
ip_list = []
get_hidemy()



s = requests.session()
r = s.get(url, headers=header)
html = r.content
soup = BeautifulSoup(html, "html.parser")