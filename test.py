import os
import re
import sys
import time
import json
import random
import requests
from requests.exceptions import ReadTimeout, ConnectionError, RequestException
import csv

from lxml import etree


from multiprocessing import Process



defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

# USER_AGENTS 随机头信息
USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
]

# 构造请求头
HEADER = {
    'User-Agent': random.choice(USER_AGENTS),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate',
}


# Get网页，返回内容
def get_html(url_path, payload='', cookies='', proxies=''):
    try:
        s = requests.Session()
        r = s.get(
            url_path,  # 路径
            headers=HEADER,  # 请求头
            params=payload,  # 传参 @payload 字典或者json
            cookies=cookies,  # cookies
            verify=True,  # SSL验证 @verify False忽略;True开启
            proxies=proxies,  # 代理
            timeout=30)  # @timeout 超时单位 秒
        r.raise_for_status()
        # print r.headers#获取响应头
        # print r.cookies#获取cookies
        return r.text
    except ReadTimeout:
        print('Timeout')
    except ConnectionError:
        print('Connection error')
    except RequestException:
        print('RequestException')


def get_codimg(html):
    datas = etree.HTML(html)
    # print(datas)
    # //*[@id="__next"]/div/div[2]
    info = datas.xpath('//*[@id="__next"]/div/div[2]//text()')
    # print(info)
    return info


def get_image(html):
    html = str(html)
    reg = r"src=\"(.*?)\""
    reger = re.compile(reg, re.S)
    data = re.findall(reger, html)
    return data


csv_data_file = 'D:/PDD_5_7.csv'

# 爬取商品信息ID在 50000000 ~ 100000000 的商品
n = 50000000
while n < 100000000:
    # get_proxies = {
    #     "http": random.choice(http_ip),
    #     "https": random.choice(https_ip),
    # }
    test1url = "https://youhui.pinduoduo.com/goods/goods-detail?goodsId=" + str(n)
    print("链接： " + test1url)
    print("ID ： " + str(n))
    # print(get_proxies)
    html_info = get_html(test1url)
    if "An unexpected error has occurred" in str(html_info) or "NaN" in str(html_info):
        # print("未找到商品信息")
        # print("***************************")
        pass
    else:

        cod_link = test1url
        print("商品链接： " + cod_link)
        # print(get_image(html_info))
        imgs = get_image(html_info)

        if imgs == []:
            continue

        cod_imglink = imgs[1]
        print("商品图片： " + cod_imglink)
        '''
        for src_img in imgs:
            print(src_img)
        '''
        cod_info = get_codimg(html_info)
        cod_name = cod_info[0]
        print("商品名称： " + cod_name)
        cod_pjiege = cod_info[4]
        print("商品价格： " + cod_pjiege)
        cod_xiaoliang = cod_info[6]
        print("商品销量： " + cod_xiaoliang)
        cod_shop = cod_info[9]
        print("店铺名称： " + cod_shop)
        # cod_shop = cod_info[10]
        print(cod_info[10] + ":" + cod_info[11])
        print(cod_info[12] + ":" + cod_info[13])
        print(cod_info[14] + ":" + cod_info[15])
        '''
        for cod_data in cod_info:
            print(cod_data)
        '''
        time_data = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        input_datas = ["拼多多", cod_name.replace("\'", ""), cod_link, cod_imglink, cod_pjiege, cod_xiaoliang,
                       cod_shop.replace("\'", ""), cod_info[10],
                       cod_info[11], cod_info[12], cod_info[13], cod_info[14], cod_info[15], time_data]
        # print('D:/py_test/yibiao_Auto/report/xyzg_data/tb_test1.csv')

        # input_datas = [cod_name1,cod_name2]
        with open(csv_data_file, 'a', newline='', encoding='utf-8') as f:
            try:
                csv_write = csv.writer(f, dialect='excel')
                csv_write.writerow(input_datas)
            except:
                print("获取内容编码不标准存在问题")
    print("\n")
    n += 1
