import requests
import sys
import re
import pymysql

class product:
	type="历史"
	name=""
	author=""
	desciption=""
	pic1=""
	languages=""
	press=""

def getProUrl():
	urlList = []
	headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
	session = requests.Session()
	furl="https://www.amazon.cn/gp/search/ref=sr_adv_b/?search-alias=stripbooks&field-binding_browse-bin=2038564051&sort=relevancerank&page="
	for i in range(1,7):
		html=""
		print(furl+str(i)) 
		html = session.post(furl+str(i)+'&node=658418051',headers = headers)
		html.encoding = 'utf-8'
		s=html.text.encode('gb2312','ignore').decode('gb2312')
		url=r'</li><li id=".*?" data-asin="(.+?)" class="s-result-item celwidget">'
		reg=re.compile(url,re.M)
		items = reg.findall(html.text)
		for i in range(0,len(items)):
			urlList.append(items[i])
	urlList=set(urlList)
	return urlList

def getProData(url):
	pro = product()
	headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
	session = requests.Session()
	zurl="https://www.amazon.cn/dp/"
	html = session.get(zurl+url,headers = headers)
	html.encoding = 'utf-8'
	s=html.text.encode('gb2312','ignore').decode('gb2312')
	pro.pic1=getProPic(html)
	pro.name=getProName(html)
	pro.author=getProAuthor(html)
	pro.desciption=getProDescrip(html)
	pro.press=getProPress(html)
	pro.languages=getProLanguages(html)
	return pro

def getProPic(html):
	pic=r'id="imgBlkFront" data-a-dynamic-image="{&quot;(.+?)&quot;.*?}"'
	reg=re.compile(pic,re.M)
	items = reg.findall(html.text)
	if len(items)==0:
		return ""
	else:
		return items[0]
	
def getProName(html):
	name=r'<div class="ma-title"><p class="wraptext goto-top">(.+?)<span'
	reg=re.compile(name,re.M)
	items = reg.findall(html.text)
	if len(items)==0:
		return ""
	else:
		return items[0]
	
def getProAuthor(html):
	author=r'<span class="author.{0,20}" data-width="".{0,30}>.*?<a class="a-link-normal" href=".*?books">(.+?)</a>.*?<span class="a-color-secondary">(.+?)</span>'
	reg=re.compile(author,re.S)
	items = reg.findall(html.text)
	au=""
	for i in range(0,len(items)):
		au=au+items[i][0]+items[i][1]
	return au
	
def getProDescrip(html):
	Descrip=r'<noscript>.{0,30}<div>(.+?)</div>.{0,30}<em></em>.{0,30}</noscript>.{0,30}<div id="outer_postBodyPS"'
	reg=re.compile(Descrip,re.S)
	items = reg.findall(html.text)
	if len(items)==0:
		return ""
	else:
		position = items[0].find('海报：')
		descrip=items[0]
		if position != -1:
			descrip=items[0][0:position]
		return descrip.strip()

def getProPress(html):
	press=r'<li><b>出版社:</b>(.+?)</li>'
	reg=re.compile(press,re.M)
	items = reg.findall(html.text)
	if len(items)==0:
		return ""
	else:
		return items[0].strip()
	
	
def getProLanguages(html):
	languages=r'<li><b>语种：</b>(.+?)</li>'
	reg=re.compile(languages,re.M)
	items = reg.findall(html.text)
	if len(items)==0:
		return ""
	else:
		return items[0].strip()
	
def getConnection():
	config = {
          'host':'121.42.57.36',
          'port':3306,
          'user':'root',
          'password':'xsys@123',
          'db':'bb_home_work',
          'charset':'utf8',
          'cursorclass':pymysql.cursors.DictCursor,
          }
	connection = pymysql.connect(**config)
	return connection
	
urlList = getProUrl()
i = 0
for d in urlList:
	i = i + 1
	print (i)
	connection = getConnection()
	pro = getProData(d)
	try:
		with connection.cursor() as cursor:
			sql='INSERT INTO books (type,name,author,desciption,pic1,languages,press) VALUES (%s,%s,%s,%s,%s,%s,%s)'
			cursor.execute(sql,(pro.type,pro.name,pro.author,pro.desciption,pro.pic1,pro.languages,pro.press))
		connection.commit()
	finally:
		connection.close();























