# !/Python

import requests
import sqlite3
import threading
from bs4 import BeautifulSoup
from ghost import Ghost, Session

#################################
UA = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14'
header = {'User-Agent':UA,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate'
}
s = requests.session()
s.keep_alive = False
gh = Ghost()
se = Session(gh, user_agent=ua, wait_timeout=30, wait_callback=None, display=False, viewport_size=(800, 680), download_images=False)

#####################################
def get_guobanjia():
    for i in range(1, 9):
        url = 'http://www.goubanjia.com/free/isp/%E7%A7%BB%E5%8A%A8/index' + str(i) + '.shtml'
        r = s.get(url, headers=header)
        if r.status_code == 200:
            print('正在载入第%s页' %i)
        html = r.content
        soup = BeautifulSoup(html, "html.parser")
        hidden_tags = soup.select('p')
        for tag in hidden_tags:
            tag.extract()
        source = soup.select('tbody > tr')
        for i in source:
            ip_info = guobanjia_info(i)
            if ip_info[3] != '透明':
                if ip_info[0] != 'socks5':
                    add_task(ip_info[0], ip_info[1], ip_info[2])

def guobanjia_info(string):
    ipp = string.td.text
    ip = ipp.split(':')[0]
    port = ipp.split(':')[1]
    anmy = string.select('td')[1].text
    type = string.select('td')[2].text
    return(type, ip, port, anmy)

######################################
def get_kuaidaili():
    for i in range(2, 10):
        url = 'http://www.kuaidaili.com/free/inha/%s/' % i
        r = s.get(url, headers=header)
        if r.status_code == 200:
            print('正在载入第%s页' %i)
        else:
            print('载入第%s页失败' %i)
        html = r.content
        soup = BeautifulSoup(html, "html.parser")
        source = soup.select('tbody > tr')
        for i in source:
            ip_info = kuaidaili_info(i)
            add_task(ip_info[0], ip_info[1], ip_info[2])

def kuaidaili_info(string):
    ip = string.select('td')[0].text
    port = string.select('td')[1].text
    type = string.select('td')[3].text.lower()
    return(type, ip, port)

#################################################

def get_kunpeng():
    url = 'http://www.site-digger.com/html/articles/20110516/proxieslist.html'
    se.open(url)
    html = se.content
    soup = BeautifulSoup(html, "html.parser")
    source = soup.select('tbody > tr')
    for i in source:
        ip_info = kunpeng_info(i)
        type = 'http'
        if ip_info[2] == 'Anonymous':
            add_task(type, ip_info[0], ip_info[1])

def kunpeng_info(string):
    ipp = string.select('td')[0].text.split(';')[1]
    ip = ipp.split(':')[0]
    port = ipp.split(':')[1]
    anmy = string.select('td')[1].text
    return(ip, port, anmy)

##################################################





##################################################

def add_task(type, ip, port):
    a = threading.Thread(target=test_ip, args=(type, ip, port,))
    threads.append(a)
    a.start()

def test_ip(type, ip, port):
    proxy = {type: "%s://%s:%s" %(type, ip, port)}
    try:
        r = requests.get('http://ip.cn', proxies=proxy, timeout=3)
    except:
        print('%s无法连接！' % ip)
    else:
        if r.status_code == 200:
            print('%s加入列表！' % ip)
            ip_list.append((type, ip, port))


ip_list = []
threads = []
get_guobanjia()
get_kuaidaili()
get_kunpeng()

http://www.goubanjia.com/free/isp/%E7%A7%BB%E5%8A%A8/index1.shtml
http://www.kuaidaili.com/free/
