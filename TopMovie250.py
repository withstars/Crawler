import requests
from lxml import html

k = 1
for page in range(10):
    url = 'https://movie.douban.com/top250?start={}&filter='.format(page*25)
    con = requests.get(url).content
    sel = html.fromstring(con)
    for i in sel.xpath('//div[@class="info"]'):
        title = i.xpath('div[@class="hd"]/a/span[@class="title"]/text()')[0]
        info = i.xpath('div[@class="bd"]/p[1]/text()')

        # 导演演员信息
        info_1 = info[0].replace(" ", "").replace("\n", "")
        # 上映日期
        date = info[1].replace(" ", "").replace("\n", "").split("/")[0]
        # 制片国家
        country = info[1].replace(" ", "").replace("\n", "").split("/")[1]
        # 影片类型
        geners = info[1].replace(" ", "").replace("\n", "").split("/")[2]

        rate = i.xpath('//span[@class="rating_num"]/text()')[0]
        comCount = i.xpath('//div[@class="star"]/span[4]/text()')[0]
        inq = i.xpath('//span[@class="inq"]/text()')[0]

        print("TOP %s" % str(k))
        print(info_1, date, country, geners, rate, comCount, inq)
        print("==========================================")

        with open("豆瓣电影 TOP 250.txt", "a", encoding='utf-8') as file:
            file.write("TOP%s\n影片名称：%s\n评分：%s %s\n上映日期：%s\n上映国家：%s\n%s\n简介: %s\n" % (k, title, rate, comCount, date, country, info_1, inq))

            file.write("=============================================\n")
        k = k + 1

