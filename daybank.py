import pymysql
import requests
import time
from lxml import html
nowmonth = time.strftime('%Y%m',time.localtime(time.time()))
conn = pymysql.connect(host='localhost',
			    user='root',
			    password='Aas:L2@$@!kdfjW',
			    db='test',
			    charset='utf8mb4',
			    cursorclass=pymysql.cursors.DictCursor,)
MAXCONT  = 5 #max item
item = {}

def spider():
	# first spider
	insertcontent=0
	result = requests .get('http://www.0daybank.org/?m=%s'%(nowmonth))
	dom = html.fromstring(result.text)
	contents = dom.xpath("//article[@id='content']/ul/li")
	with conn.cursor() as cursor:
		for i in range(0,MAXCONT):
			item['title'] = contents[i].xpath("a/text()")[0]
			item['link'] ="http://www.0daybank.org"+contents[i].xpath("a/@href")[0]
			flag = cursor.execute("SELECT title FROM message where link = '%s'"%(item['link']))
			if(flag != 0):
				continue
			cursor.execute("INSERT INTO message(title,link) value('%s','%s')"%(item['title'],item['link']))
			insertcontent =insertcontent+1
		print(insertcontent)

		if insertcontent < MAXCONT:
			i = insertcontent
			result = requests.get("http://www.freebuf.com/vuls")
			dom = html.fromstring(result.text)
			contents = dom.xpath("//div[@id='timeline']/div")
			
			for i in range(i,MAXCONT) :	#max  7item
				item['title'] = contents[i].xpath("div[@class='news-info']/dl/dt/a/text()")[0]
				item['link'] = contents[i].xpath("div[@class='news-info']/dl/dt/a/@href")[0]
				flag = cursor.execute("SELECT title FROM message where link = '%s'"%(item['link']))
				if(flag != 0):
					continue
				cursor.execute("INSERT INTO message(title,link) value('%s','%s')"%(item['title'],item['link']))
				insertcontent =insertcontent+1
			print(insertcontent)
		if insertcontent <MAXCONT:
			i = insertcontent
			result = requests.get("http://news.91.com/it/")
			dom = html.fromstring(result.text)
			contents = dom.xpath("//div[@class='main_list']/div[@class='m_one']")
			for i in range(i,MAXCONT):
				item['title'] = contents[i].xpath("h4/a/text()")[0]
				item['link'] = contents[i].xpath("h4/a/@href")[0]
				flag = cursor.execute("SELECT title FROM message where link = '%s'"%(item['link']))
				if(flag != 0):
					continue
				cursor.execute("INSERT INTO message(title,link) value('%s','%s')"%(item['title'],item['link']))
				insertcontent =insertcontent+1
			print(insertcontent)
	conn.commit()	


if __name__ == "__main__":
	spider()