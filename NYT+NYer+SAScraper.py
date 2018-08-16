from bs4 import BeautifulSoup as bs
import urllib.request
import re
import os
import xml.etree.ElementTree as et
output = open('output.txt', 'w+')

email = False
output.write('THE NEW YORK TIMES\n')
nyt_page = urllib.request.urlopen('https://www.nytimes.com/section/books')
nyt_html = nyt_page.read()
nyt_page.close()
beau = bs(nyt_html, 'html.parser')
for article in beau.findAll('div', {'class':'story-body'}):
	if 'your favorite author here' in article.find('p', 'summary').get_text() or 'your favorite author here' in article.find('p', 'summary').get_text():
		if article.h2.a != None:
			email = True
			output.write(article.h2.a.get_text() + '\n')
			output.write(article.p.get_text() + '\n')
			output.write(article.h2.a.get('href') + '\n')

output.write('\nTHE NEW YORKER\n')
nyer_page = urllib.request.urlopen('https://www.newyorker.com/books')
nyer_html = nyer_page.read()
nyer_page.close()
beau = bs(nyer_html, 'html.parser')
class_name = re.compile('Card__content__')
for article in beau.findAll('div', {'class':class_name}):
	if 'your favorite author here' in article.find('p', re.compile('Card__dek___')).get_text() or 'your favorite author here' in article.find('p', re.compile('Card__dek___')).get_text():		
		email = True
		output.write(article.find('a', re.compile('Link__link___')).get_text() + '\n')
		output.write(article.p.get_text() + '\n')
		output.write('https://www.newyorker.com/' + article.find('a', re.compile('Link__link___')).get('href') + '\n')

output.write('\nSEEKING ALPHA\n')
request = urllib.request.Request('https://seekingalpha.com/sitemap_news.xml', headers={'User-Agent': 'Mozilla/5.0'})
sa_page = urllib.request.urlopen(request)
sa_unformed = sa_page.read()
sa_formed = sa_unformed.decode('utf-8')
root = et.fromstring(sa_formed)
sa_page.close()
for url in root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
	news = url.find('{http://www.google.com/schemas/sitemap-news/0.9}news')
	tickers = news.find('{http://www.google.com/schemas/sitemap-news/0.9}stock_tickers')
	if (tickers != None) and tickers.text != None and ('your stock here' in tickers.text or 'your stock here' in tickers.text):
		email = True
		output.write(news.find('{http://www.google.com/schemas/sitemap-news/0.9}title').text + '\n')
		output.write(tickers.text + '\n')
		output.write(url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text + '\n\n')
		
output.close()

#if email:
#	os.system('cat output.txt | mail "')
