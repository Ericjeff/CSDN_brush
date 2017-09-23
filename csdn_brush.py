#!/usr/bin/python
# -*- encoding:utf-8 -*-

import urllib2
import urllib
import threading
from bs4 import BeautifulSoup
'''
   首先pip install  BeautifulSoup4
'''
class CSDN:

    '''
    
        url_all:刷整个博客的文章的地址
        url_single:刷单个文章的地址
        headers:request的头部，伪装成浏览器
        number:刷的数量
    '''
    def __init__(self,url_all,url_single,headers,number):
        self.url_all = url_all
        self.url_single = url_single
        self.headers = headers
        self.number = number


    #获取这个博客的URLS
    def getURLS(self,url,headers):
        req = urllib2.Request(url=url,headers=headers)
        resp = urllib2.urlopen(req)
        html =  resp.read()

        soup = BeautifulSoup(html)
        div = soup.find("div",id="papelist")
        links =  div.find_all("a")
        urls = []
        urlheader = "http://blog.csdn.net"
        urls.append(url)
        for link in links:
             urls.append(urlheader+link["href"])

        return urls



    #多线程执行的方法
    def threadtest(self,url,urlheader,headers):
        print "执行我的线程名:%s"%threading.current_thread().name
        req = urllib2.Request(url=url,headers=headers)
        resp = urllib2.urlopen(req)
        html = resp.read()
        soup = BeautifulSoup(html)
        links = soup.find_all("span",class_="link_title")
        for link in links:
            urll =  urlheader+link.find("a")["href"]
            req = urllib2.Request(url=urll,headers=headers)
            resp = urllib2.urlopen(req)
            print "=========%s=================="%url


    #开始刷文章
    def getflushTitle(self,urls,headers):
        urlheader = "http://blog.csdn.net"
        for url in urls:
            #threadtest(url,urlheader)
            t = threading.Thread(target=self.threadtest,name="我的名字:%s"%url,args=(url,urlheader,headers))
            t1 = threading.Thread(target=self.threadtest,name="我的名字:%s"%url,args=(url,urlheader,headers))
            t2 = threading.Thread(target=self.threadtest,name="我的名字:%s"%url,args=(url,urlheader,headers))
            t3 = threading.Thread(target=self.threadtest,name="我的名字:%s"%url,args=(url,urlheader,headers))
            t.start()
            t1.start()
            t2.start()
            t3.start()
            t.join()
            t1.join()
            t2.join()
            t3.join()



    #刷整个博客的文章
    def start_all(self):

        urls = self.getURLS(self.url_all,self.headers)
        print urls

        for i in range(200):
            self.getflushTitle(urls,self.headers)


    #刷单篇文章
    def start_single(self):

        for i in range(self.number):
            req = urllib2.Request(url=self.url_single,headers=self.headers)
            urllib2.urlopen(req)
            print "刷单篇博客，，这是第%d次........"%(i+1)




user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
headers = {"User_agent":user_agent}


url_single = "http://blog.csdn.net/etails/8235255"
#将你的博客名替换xxxxxxxxx
url_all = "http://blog.csdn.net/xxxxxxxxxx/article/list/1"

c = CSDN(url_all,url_single,headers,200)
#刷单篇博客
c.start_single()
#刷整个博客的文章
c.start_all()