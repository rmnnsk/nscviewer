from bs4 import BeautifulSoup as bs
import requests
import re
import hashlib
import time
from selenium import webdriver
#import sys
import codecs


#sys.setdefaultencoding('utf8')

browser = webdriver.Firefox()
browser.set_window_size(1920,1080)

def getPassw(passwd,soup):
	"""Return PW and PW2 for your password"""
	sc = soup.find_all("script")[-3]
	num = re.findall(r"\d{9,12}",sc.text)[0]
	PW2 = hashlib.md5(str.encode(num+hashlib.md5(str.encode(passwd)).hexdigest())).hexdigest()
	PW = PW2[:len(passwd)]
	return PW,PW2

def enter(UN,passw,session):
	ts = session
	r = session.post('http://82.208.80.123/login1.asp',data = {
		'BSP': 0,
		'BST': 0,
		'CID': 2,
		'CN': 7,
		'LoginType': 1,
		'N': 3,
		'PID': -1,
		'SFT': 0,
		'SID': 52,
		'ER':''})
	soup = bs(r.text,"lxml")
	VER = soup.find('input',{'name':"VER"})['value']
	LT = soup.find('input',{'name':"LT"})['value']
	PW,PW2 = getPassw(passw,soup)
	rdata = {
		'BSP':'',
		'BST': 0,
		'CID': 2,
		'CN': 7,
		'LT': LT,
		'LoginType': 1,
		'N': 4,
		'PID': -1,
		'PW': PW,
		'PW2': PW2,
		'SCID': 2,
		'SFT': 2,
		'SID': 52,
		'UN': UN,
		'VER': VER
	}
	req = session.post('http://82.208.80.123/asp/postlogin.asp',data = rdata)
	if req.url != 'http://82.208.80.123/asp/postlogin.asp':
		print("Wrong login or password")
		return 0
	soup = bs(req.text,"lxml")
	AT = soup.find('input',{'name':"AT"})['value']
	VER = soup.find('input',{'name':"VER"})['value']
	rdata = {
		'AT':AT,
		'VER':VER
	}
	req = session.post('http://82.208.80.123/asp/Announce/ViewAnnouncements.asp',data = rdata)
	with codecs.open('tt.html', 'w', 'utf-8') as file:
		text = req.text
		#text = text.encode('utf8')
		file.write(text)
	browser.get('file:///C:/Users/ROMAN/Desktop/bs4test/tt.html')
	browser.save_screenshot('screen.png')
	browser.quit()
	soup = bs(req.text,"lxml")
	AT = soup.find('input',{'name':"AT"})['value']
	VER = soup.find('input',{'name':"VER"})['value']
	print("Войдено")
	return (AT,VER,ts)
	
def exit(datat,session):
	print(datat)
	#print(time.time())
	AT,VER = datat
	edata = {
		'AT': AT,
		'LoginType': 0,
		'MenuItem': 13,
		'TabItem': 25,
		'VER': VER,
		'optional':''
	}
	r = session.post('http://82.208.80.123/asp/logout.asp',data = edata)
	print("Выход комплитед")

def get_message(datat,session):
	AT, VER = datat
	mdata = {'AT':AT,'VER':VER}
	mreq = session.post('http://82.208.80.123/asp/Messages/MailBox.asp', data = mdata)
	mdata2 = {'AT':AT,'VER':VER,'MVT':'','MID':'57832','MBID':'1','A':''}
	mreq2 = s.post('http://82.208.80.123/asp/Messages/MailBox.asp',data = mdata2)
	print(mreq2.text)
	mdata3= {'AT':AT,'MID':'86400','MBID':'1'}
	mess = s.get('http://82.208.80.123/asp/Messages/readmessage.asp',params = mdata3)
	print(mess.url)

if __name__ == "__main__":
	s = requests.Session()
	data = enter('login','password',s)
	exit((data[0], data[1]), data[2])
