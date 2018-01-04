# import libraries 
import time # wait commands (space out)
import re # regular expressions (text parser)
import urllib # Internet connection (socket connections, https)
import csv

top_columns = ['url', 'character']

MacFile = csv.writer(file('greysanatomy.csv', 'a'),dialect='excel')
MacFile.writerow(top_columns)

def scrape_page(html_page):
	# print html_page;

	wrapper = re.search('<table width="100%">(.+?)</table>', html_page, re.S|re.DOTALL)

	# print wrapper
	# print wrapper.group(0)
	table_content = wrapper.group(0)
	# print wrapper.group(1)

	for single in re.finditer('<li><a href="/wiki/(.+?)</li>', table_content, re.S|re.DOTALL):
		# print single.group(0)

		get_character_names = re.search('<a href="/wiki/(.+?)" title="(.+?)">(.+?)</a>', single.group(0), re.S|re.DOTALL)
		url = 'http://greysanatomy.wikia.com/wiki/' + get_character_names.group(1)
		character = get_character_names.group(3)
		# print url
		# apt_price = apt_price.group(1)

		# apt_size = re.search('<span class="housing">(.+?)</span>', single.group(0), re.S|re.DOTALL)
		
		# if apt_size is not None:
		# 	apt_size = apt_size.group(1)
		# 	# print apt_size

		# 	# if there is a br, then put it into a variable
		# 	if re.search('(\d)br', apt_size):
		# 		bedroom_num = re.search('(\d)br', apt_size)
		# 		bedroom_num = bedroom_num.group(1)
		# 	else:
		# 		bedroom_num = ""

		data = [url, character]
		MacFile.writerow(data)
		print data

# variables for function 
# start_value = 1
base_url = 'http://greysanatomy.wikia.com/wiki/Category:Deceased_Characters'

# while start_value < 101:
full_url = base_url

html_page = urllib.urlopen(full_url).read() # .urlopen() takes one value, the URL to open # .read() as a method to read returns
scrape_page(html_page)

# start_value = start_value + 10
# time.sleep(2)