import requests
from lxml import html
import os
from multiprocessing.dummy import Pool as ThreadPool

def header():
    headers = {
    'accept': 'text/html, application/xhtml+xml, application/xml q = 0.9, image/webp, image/apng, */*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN, zh;q = 0.9',
    'cache-control': 'max - age = 0',
    'if-modified-since': 'Tue, 24 May 2016 06: 11:42 GMT upgrade - insecure - requests:1 user-agent:Mozilla/5.0(Windows NT 10.0;WOW64) AppleWebKit/537.36(KHTML, like Gecko) Chrome / 65.0.3325.162 Safari / 537.36',
    }
    return headers;

def getMainPage(num):
    baseUrl = 'http://desk.zol.com.cn/fengjing/{}.html'.format(num)
    selector = html.fromstring(requests.get(baseUrl).content)
    urls = []
    for i in selector.xpath('//ul[@class = "pic-list2  clearfix"]/li[@class = "photo-list-padding"]/a/@href'):
        i="http://desk.zol.com.cn"+i
        urls.append(i)
        print(i)
    return urls

def getPic(url):
    sel = html.fromstring(requests.get(url).content)
    total = sel.xpath('//div[@class= "photo-list-box"]/ul[@id = "showImg"]/li[last()]/i/em/text()')[0]
    title = sel.xpath('//a[@id = "titleName"]/text()')[0]
    pageLinks = []
    for i in sel.xpath('//div[@class= "photo-list-box"]/ul[@id = "showImg"]/li/a/@href'):
        i = "http://desk.zol.com.cn" + i
        pageLinks.append(i)
    dirName = u"[{}Pics]{}".format(total, title)
    os.makedirs(dirName)
    print(pageLinks)
    k = 1
    for i in pageLinks:
        try:
            s = html.fromstring(requests.get(i).content)
            picLink = s.xpath('//img[@id = "bigImg"]/@src')
            print(picLink)
            filename = '%s/%s/%s.jpg' % (os.path.abspath('.'), dirName, k)
            print(u"开始下载图片:%s 第%s张" % (dirName, k))
            with open(filename, "wb") as pic:
                pic.write(requests.get(picLink).content.encode('utf-8'))
            k += 1
        except:
            pass

if __name__ == '__main__':
    pageNum = input("请输入页号")
    p= getMainPage(pageNum)
    with ThreadPool(5) as pool:
        pool.map(getPic, p)





