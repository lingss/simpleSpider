#-*- coding:utf-8 -*-
from lxml import html
import pymysql
import requests
import time
import SMTP
import re

nowmonth = time.strftime('%Y%m',time.localtime(time.time())) #现在月份
conn = pymysql.connect(host='localhost',
			    user='',
			    password='',
			    db='test',
			    charset='utf8mb4',
			    cursorclass=pymysql.cursors.DictCursor,)
MAXCONT  = 10 #每天爬取网页数量
item = {}

def spider():
	try:
		insertcontent=0
		# 爬取第一个网站
		today = "%d年%d月%d日"%(time.localtime().tm_year,time.localtime().tm_mon,time.localtime().tm_mday)
		result = requests .get('http://www.0daybank.org/?m=%s'%(nowmonth))
		dom = html.fromstring(result.text)
		contents = dom.xpath("//article[@id='content']/ul/li")
		with conn.cursor() as cursor:
			for i in range(0,MAXCONT):
				time2 = contents[i].xpath("time/text()")[0]
				print(str(time2))
				if str(time2) != today:
					continue
				print("yes")
				item['title'] = contents[i].xpath("a/text()")[0]
				item['link'] ="http://www.0daybank.org"+contents[i].xpath("a/@href")[0]
				flag = cursor.execute("SELECT title FROM message where link = '%s'"%(item['link']))
				if(flag != 0):
					continue
				cursor.execute("INSERT INTO message(title,link) value('%s','%s')"%(item['title'],item['link']))
				insertcontent =insertcontent+1
				print(insertcontent)

			#如果没有爬取到足够的网页开始爬取第二个网站
			if insertcontent < MAXCONT:
				today = "%d-\d?%d-\d?%d[ ]"%(time.localtime().tm_year,time.localtime().tm_mon,time.localtime().tm_mday)
				i = insertcontent
				result = requests.get("http://www.freebuf.com/vuls")
				dom = html.fromstring(result.text)
				contents = dom.xpath("//div[@id='timeline']/div")
				for i in range(i,MAXCONT) :	#max  7item
					time2 = contents[i].xpath("div[@class='news-info']/dl/dd/span[@class='time']/text()")[0]
					if re.match(today,str(time2)) is None:
						continue
					item['title'] = contents[i].xpath("div[@class='news-info']/dl/dt/a/text()")[0]
					item['link'] = contents[i].xpath("div[@class='news-info']/dl/dt/a/@href")[0]
					flag = cursor.execute("SELECT title FROM message where link = '%s'"%(item['link']))
					if(flag != 0):
						continue
					cursor.execute("INSERT INTO message(title,link) value('%s','%s')"%(item['title'],item['link']))
					insertcontent =insertcontent+1
				print(insertcontent)

			#最后第三个网站
			if insertcontent <MAXCONT:
				today = "%d-\d?%d-\d?%d"%(time.localtime().tm_year,time.localtime().tm_mon,time.localtime().tm_mday)
				i = insertcontent
				result = requests.get("http://www.dbsec.cn/about_dbsec/aqzx/zx.html")
				dom = html.fromstring(result.text)
				contents = dom.xpath("//div[@class='main']/ul/li")
				for i in range(i,MAXCONT):
					time2 = contents[i].xpath("span/text()")[0]
					if re.match(today,time2) is None:
						continue
					item['title'] = contents[i].xpath("a/text()")[0]
					item['link'] = "http://www.dbsec.cn"+contents[i].xpath("a/@href")[0]
					flag = cursor.execute("SELECT title FROM message where link = '%s'"%(item['link']))
					if(flag != 0):
						continue
					cursor.execute("INSERT INTO message(title,link) value('%s','%s')"%(item['title'],item['link']))
					insertcontent =insertcontent+1
				print(insertcontent)
		conn.commit()
		mailMessage = ("今天抓取了%d个网页"%(insertcontent))
		if insertcontent < MAXCONT:
			mailSubject = "警告！今天没有抓取到指定数量的网页"
		else:
			mailSubject = "抓取成功"
	except Exception as e:
		insertcontent = 0
		mailSubject = "错误！爬虫运行出错"
		mailMessage = ("今天抓取了%d个网页"%(insertcontent))
		print(e)
	# 开始发送邮件
	mail = SMTP.MailFormat()
	mail.setMessage(cont=mailMessage,
					subject=mailSubject,
					mimetype="plain")
	mail.sendMessage("")

if __name__ == "__main__":
	spider()
