# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import os, re, time
import requests
from random import uniform

head = 'http://dantri.com.vn'
ref = head
headers = {
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'Accept-Encoding':'gzip, deflate',
	'Accept-Language':'en-US,en;q=0.9,vi;q=0.8',
	'Connection':'keep-alive',
	'Cookie':'ASP.NET_SessionId=lrsx4rlrewz0dwwf13kdin4v',
	'Host':'dantri.com.vn',
	'Referer': ref,
	'Upgrade-Insecure-Requests':'1',
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
}
topic_links = []

def sleep():
	time.sleep(uniform(0.5, 2))

def get_topic_link(head):
	links = []
	req = requests.get(head)
	soup = BeautifulSoup(req.text, 'lxml')
	for tit in soup.find_all('ul', 'nav'):
		for topic in tit.find_all('a'):
			name = topic['href']
			if '/' == name or 'video' in name or 'su-kien' in name:
				continue
			if name.startswith('http'):
				links.append(name)
			else:
				links.append(head + name)
	return links

def get_content(link, headers):
	content = u''
	req = requests.get(link, headers=headers)
	soup = BeautifulSoup(req.text, 'lxml')
	title = soup.find('h1', 'fon31 mgb15').text.strip()
	description = soup.find('h2', 'fon33 mt1 sapo').text.strip()
	content += title + ' ' + description + ' '
	for main in soup.find_all('div', {'id': 'divNewsContent'}):
		for ly in main.find_all('p'):
			if '<p>' in str(ly) and '''<p>
<style''' not in str(ly):
				content += ly.text.strip() + ' '
	content = re.sub('[0-9;:,\-\.\?!%&\*\$\>\<\(\)\[\]\{\}\'\'\"\"/\=\=#\^\~\`]', '', content.strip()).lower()
	content = re.sub("\s\s+" , " ", content)
	return content



topic_links = get_topic_link(head)
print (topic_links)
def get_topic_name(topic_link):
	if 'dulich' not in topic_link:
		return topic_link.split('/')[3].split('.')[0]
	else:
		return'du-lich'

max_page = 2

save_file = open('E:\\dat.txt', 'w', encoding='utf-8')
for topic in topic_links:
	topic_name = get_topic_name(topic)
	for num in range(max_page):
		print ('REF PAGE = ', ref)
		init_url = topic[:len(topic) - 4] + '/' + 'trang-' + str(num) + '.htm'
		headers = {
			'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'Accept-Encoding':'gzip, deflate',
			'Accept-Language':'en-US,en;q=0.9,vi;q=0.8',
			'Connection':'keep-alive',
			'Cookie':'ASP.NET_SessionId=lrsx4rlrewz0dwwf13kdin4v',
			'Host':'dantri.com.vn',
			'Referer': ref,
			'Upgrade-Insecure-Requests':'1',
			'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
		}
		print ('page:', init_url)
		sleep()
		req = requests.get(init_url, headers=headers)
		soup = BeautifulSoup(req.text, 'lxml')
		for li in soup.find_all('div', {'data-boxtype':'timelineposition'}):
			if 'ico-newstype-autoplayvideo' in str(li) or 'ico-newstype-photo' in str(li) or 'tuyensinh' in str(li):
				continue
			tlink = li.div.h2.a['href']
			if tlink.startswith('http'):
				link = tlink
			else:
				link = head + tlink
			print (link)
			content = get_content(link, headers)
			# print (content)
			content = content.strip() + ',' + topic_name + '\n'
			# print ('topic name:', topic_name)
			print (content)
			save_file.write(content)
		print ('\n\n')
		ref = init_url
save_file.close()
