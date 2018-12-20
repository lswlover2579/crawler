import requests
import re
import os
from lxml import etree

#get the webpage content
url = ['https://movie.douban.com/top250?start=%d&filter='%(x*25) for x in range(10)]
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'Referer':'https://movie.douban.com/chart'

}

num = 1
msg = ''
for link in url:
    response = requests.get(link,headers = headers)
    #print(response.content)
    html = etree.HTML(response.text)

    #从所有影片信息div中循环提取
    for i in html.xpath('//div[@class="info"]'): 
        # 影片名称 
        title = i.xpath('div[@class="hd"]/a/span[@class="title"]/text()')[0]
        print(title) 
        #影片简介（包括导演，演员，年代，地区，类型）
        info = i.xpath('div[@class="bd"]/p[1]/text()')

        #导演,演员
       # print(info[0])
        director_actor = info[0].strip()
        
        #年代
        date = info[1].split('/')[0].strip()
        #print(date)
        
        #地区
        country = info[1].split('/')[1].strip()

        #type
        geners = info[1].split('/')[2].strip()

        #评分
        rate = i.xpath('div[@class="bd"]/div[@class="star"]/span[@class = "rating_num"]/text()')[0]
        
        #评分人数
        comcount = i.xpath('div[@class="bd"]/div[@class="star"]/span[4]/text()')[0]
        #print(rate)
        #ratenum.extend(rate)

        #movie.append(title+director_actor+date+country+geners)
        msg +='\n' + 'Top' + str(num) + ' : ' + title + "\n" +  director_actor + "\n" + date + "  " + country + "  " + geners + "\n" + '评分: ' + rate +'   评分人数:  ' + comcount + '\n'

        num += 1

with open('text.txt','w',encoding='UTF-8') as f:

    f.write(msg + '\n')
