from bs4 import BeautifulSoup as bs
import urllib.request
import re

nyt_page = urllib.request.urlopen('https://www.nytimes.com/section/books')
nyt_html = nyt_page.read()
nyt_page.close()
output = open('output.txt', 'w+')

beau = bs(nyt_html, 'html.parser')
output.write('THE NEW YORK TIMES\n')
for article in beau.findAll('div', {'class':'story-body'}):
	if 'his' in article.find('p', 'summary').get_text() or 'Steinbeck' in article.find('p', 'summary').get_text():
		if article.h2.a != None:
			output.write(article.h2.a.get_text() + '\n')
			output.write(article.p.get_text() + '\n')
			output.write(article.h2.a.get('href') + '\n')

nyer_page = urllib.request.urlopen('https://www.newyorker.com/books')
nyer_html = nyer_page.read()
nyer_page.close()

beau = bs(nyer_html, 'html.parser')
output.write('\nTHE NEW YORKER\n')
class_name = re.compile('Card__content__')
for article in beau.findAll('div', {'class':class_name}):
	if 'the' in article.find('p', re.compile('Card__dek___')).get_text():		
		output.write(article.find('a', re.compile('Link__link___')).get_text() + '\n')
		output.write(article.p.get_text() + '\n')
		output.write('https://www.newyorker.com/' + article.find('a', re.compile('Link__link___')).get('href') + '\n')

output.close()