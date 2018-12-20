import requests
import re
import os

# GET web text
url = 'http://tu.duowan.com/tag/5037.html'
user_agent = 'Mozilla/5.0 (compatible; MSIE 5.5; Windows NT) Chrome/19.0.1063.0 Safari/536.3'
headers = {'user_agent': user_agent}
rsp = requests.get(url,headers = headers)
page_text = rsp.content.decode('utf-8')
#print(page_text)
#get url and title
re_match = r'<em><a href="(.*?)" target="_blank">(.*?)</a> .*?</em>'
patt = re.compile(re_match,re.S)
items = re.findall(patt,page_text)
print(items,len(items))
parent_links = []

for item in items:
    print(item)
    title = item.split(":")[-1]
    scroll_mode = item[0].replace('gallery','scroll')
    print(scroll_mode)
    parent_links.append(scroll_mode)
    scroll_mode = scroll_mode.replace('.html','')
    lists = [scroll_mode + '/' + str(n) +'.html' for n in range(2,4)]
    lists.insert(0,parent_links[0])
    #parent_links.extend([scroll_mode + '/' + str(n) +'.html' for n in range(2,4)])
    print('lists is: ',lists)
    x = 0
    for link in lists:
        print("每一页页面URL：",link)
        r = requests.get(link,headers = headers)
        gallery_page_text = r.content.decode('utf-8')
        #print(gallery_page_text)
        reg = r'<span class="pic-box-item" data-img="(.*?)" .*?class="comment">'
        #'<div class="pic-box"><a target="_blank" href=".*?"><span class="pic-box-item" data-img="(.*?)" data-mp4="" data-video=""></span></a><p class="comment">.*?</p><div class="note-comment"><div class="inner"><h3>.*?</h3><div class="content">'
        #'class="pic-box"><a target="_blank" href=".*?"><span.*?data-img="(.*?)" .*?span></a>'
        patt2 = re.compile(reg,re.S)
        img_url = re.findall(patt2,gallery_page_text)
        print("每一页所有图片的URL：",img_url)
        print("数量",len(img_url))
        
        for i in img_url:
            print("每张图URL: ",i)
            if os.path.exists('I:/IDM_Download/duowan_images/' + item[1]):
                break
            else:
                os.makedirs('I:/IDM_Download/duowan_images/' + item[1])
            #获取图片二进制数据
            print("获取图片二进制数据")
            img_data = requests.get(i,headers =headers).content

            #设置save路径
            x += 1
            img_path = 'I:/IDM_Download/duowan_images/' + item[1] + '/' + '[' +str(x) + ']' + '.jpg'
            #存储图片
            print("打开文件")
            f = open(img_path,'wb')
            f.write(img_data)
            f.close()
            print("关闭文件")
            print("saving done.")

print('All Done!')
