# !/Python

import requests
import sqlite3
import threading
from bs4 import BeautifulSoup

#################################
UA = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
header = {'User-Agent':UA}
s = requests.session()
s.keep_alive = False

def get_page():
    global ip_list
    ip_list = []
    for i in range(1, 9):
        url = 'http://www.goubanjia.com/free/isp/%E7%A7%BB%E5%8A%A8/index' + str(i) + '.shtml'
        r = s.get(url, headers=header)
        html = r.content
        soup = BeautifulSoup(html, "html.parser")
        hidden_tags = soup.select('p')
        for tag in hidden_tags:
            tag.extract()
        source = soup.select('tbody > tr')
        for i in source:
            ip_info = info(i)
            if ip_info[3] != '透明':
                if ip_info[0] != 'socks5':
                    test_ip(ip_info[0], ip_info[1], ip_info[2])


def info(string):
    ipp = string.td.text
    ip = ipp.split(':')[0]
    port = ipp.split(':')[1]
    anmy = string.select('td')[1].text
    type = string.select('td')[2].text
    return(type, ip, port, anmy)


def test_ip(type, ip, port):
    proxy = {type: "%s://%s:%s" %(type, ip, port)}
    try:
        r = requests.get('http://ip.cn', proxies=proxy, timeout=3)
    except:
        print('111')
    else:
        if r.status_code == 200:
            print('%s加入列表' % ip)
            ip_list.append((type, ip, port))


get_page()

http://www.goubanjia.com/free/isp/%E7%A7%BB%E5%8A%A8/index1.shtml
