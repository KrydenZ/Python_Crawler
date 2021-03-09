'''
Python原生爬虫
'''
import re
from urllib import request

class Spider():

    url = 'https://safebooru.org/index.php?page=tags&s=list'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}  
    root_pattern = '<tr><td>([\s\S]*?)</td></tr>'
    tag_pattern = '">(?!<a)([\s\S]*?)</a></span>'
    num_pattern = '([\s\S]*?)</td><td><span'

    #获取网页内容
    def __fetch_content(self):

        #加入headers伪装成浏览器避免网站反爬虫
        req = request.Request(url=Spider.url, headers=Spider.headers)  
        r = request.urlopen(req) 
        htmls = r.read()
        htmls = str(htmls, encoding='utf-8')

        return htmls

    #分析内容
    def __analysis(self, htmls):

        root_html = re.findall(Spider.root_pattern, htmls)
        anchors = []

        for html in root_html:
            tag = re.findall(Spider.tag_pattern, html)
            num = re.findall(spider.num_pattern, html)
            anchor = {'name': tag, 'number':num}
            anchors.append(anchor)  
        
        return anchors
   
    #数据精炼
    def __refine(self, anchors):

        l = lambda anchor : {
            #strip函数去掉可能的空格
            'name':anchor['name'][0].strip(),
            'number':anchor['number'][0]
        }

        return map(l, anchors)

    #数据排序
    def __sort(self, anchors):

        #filter
        anchors = sorted(anchors, key=self.__sort_seed, reverse = True)
        
        return anchors

    #排序的依据
    def __sort_seed(self, anchor):

        #提取所有数字
        r = re.findall('\d*', anchor['number'])
        number = float(r[0])

        if 'million' in anchor['number']:
           number = number * 1000000 

        return number

    #数据展示
    def __show(self, anchors):

        for rank in range(0, len(anchors)):
            print('rank  ' + str(rank + 1) 
            + ':' + anchors[rank]['name']
            + '     ' + anchors[rank]['number']
            )


    #入口主方法
    def go(self):

        htmls = self.__fetch_content()
        anchors = self.__analysis(htmls)
        anchors = list(self.__refine(anchors))
        anchors = self.__sort(anchors)
        self.__show(anchors)

spider = Spider()
spider.go()