#! /usr/bin/python
#coding:utf-8
#Author:SW
#Date:09-02-2014 16:20
from bs4 import BeautifulSoup as bs
import urllib2
import socket
import json
import time
#Function
#Name:Crawl
#Discribe:根据url抓取网页，根据网页结构，使用BeautifulSoup解析网页，获取
#网页中诗文的标题以及诗文内容。
#Parameters:
#no:要抓取页面的编号
#array:获取到的诗文存放的数组，按size的大小，将每size首诗文存放在一个文件中
#bNeedSave:表示当前诗文需要被存入文件
def Crawl(no, array, bNeedSave, size):
	url = 'http://so.gushiwen.org/view_' + ("%d" % no) + '.aspx'
	f = None
	html = ''
	#try except用于捕获网页请求超时异常
	try:
		f = urllib2.urlopen(url,timeout = 5)
		if f == None:
			print "There is no this web page:%s"%url	
			return
		if f.getcode() != 200:
			return
		html = f.read()
	except urllib2.URLError as e:
		if isinstance(e.reason,socket.timeout):
			print "There is a timeout error in no %d:%r"%(no,e)
		else:
			print "There is an other error in %d:%r"%(no,e)
		return
	except Exception as e:
		if isinstance(e, socket.timeout):
			print "There is a timeout error!"
		return
	if html == '' or html == None:
		return
	#根据网页内容构建BeautifulSoup对象
	soup = bs(html)
	#找到class属性为son1的div标签，在该标签中有诗文的题目
	divs = soup.find_all("div",attrs = {"class":"son1"})
	if len(divs) == 0:
		return
	children =  divs[1].contents
	if len(children) == 0:
		return
	title = children[1].string
	#找到class属性为son2的div标签，诗文内容存放在该标签中，
	#但该网站模板不统一，有四种结构，但诗文内容都在包含
	#“原文：”的p标签的后面
	divs = soup.find_all("div",attrs = {"class":"son2"})
	if len(divs) == 0:
		return
	div = divs[1]
	ps = div.find_all("p")
	index = -1
	#获取包含“原文：”的p标签在class属性为son2的div标签中
	#所有p标签中的位置
	index = [ps.index(p) for p in ps if p.string == "原文："][0]
	if index == -1:
		print no,":something wrong!"
		return
	i = index  + 1
	string = ''
	#以下为对网页中四种模板的分别处理
	if i == len(ps):
		children = div.contents
		index = children.index(ps[len(ps)-1])
		if len(children) - index == 1:
			string += children[index]
		else:
			string += ''.join([children[x] for x in range(len(children)) \
				if x > index if type(children[x]) != type(children[1])])
			string += '\n'
	elif len(ps) - i == 1:
		contents = ps[i].contents
		if len(contents) > 1:
			stringList = [i for i in contents if type(i) != type(contents[1])]
			for s in range(len(stringList)):
				string += stringList[s] + '\n'
		else:
			string += contents[0] + '\n'
	else:
		while i < len(ps):
			brList = ps[i].find_all("br")
			if len(brList) == 0:
				string += ps[i].string + '\n'
			else:
				contents = ps[i].contents
				string += ''.join([x for x in contents \
						if type(x) != type(contents[1])]) + '\n' 
			i += 1
	#获取翻译及赏析部分文字
	comments = ''
	divs = soup.find_all("div", attrs = {"class":"son5"})
	if len(divs) > 0:
		comments = ''.join([div.find_all("p")[1].contents[0] \
			for div in divs if len(div.find_all("p")) > 1 \
				if len(div.find_all("p")[1].contents) > 0])
	#将获取到的内容存入一个字典结构中
	poetryDict = {"id" : no, "title" : title, "content" : string, "comment":comments}
	#将字典
	array.append(poetryDict)
	if no % size == 0 or bNeedSave:
		if no % size == 0:
			start = no - size + 1
		else:
			start = no - no % size + 1
		print no
		filename = "savepoetry%dto%d.json" % (start, no)
		jsonstr = json.dumps(array)
		saveAsTxt(filename, jsonstr)
		array = []

def saveAsTxt(fileName, str):
	f = open(fileName,"w")
	f.write(str)
	f.flush()
	f.close()

def main():
	array = []
	bNeedSave = 0
	for i in range(0, 10001):
		if i == 72393:
			bNeedSave = 1
		Crawl(i, array, bNeedSave, 10000)
		if i % 200 == 0:
			time.sleep(15)
if __name__ == "__main__":
	main()
	
