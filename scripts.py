# import libraries 
import time # wait commands (space out)
import re # regular expressions (text parser)
import urllib # Internet connection (socket connections, https)
import csv

top_columns = ['Price','Number of bedrooms', 'Square footage', 'Avg. price']

MacFile = csv.writer(file('apartmentsToronto.csv', 'a'),dialect='excel')
MacFile.writerow(top_columns)

def scrape_page(html_page):

	for every_apt in re.finditer('<li class="result-row"(.+?)</li>', html_page, re.S|re.DOTALL):
		apt_price = re.search('<span class="result-price">(.+?)</span>', every_apt.group(0))
		apt_price = apt_price.group(1)

		apt_size = re.search('<span class="housing">(.+?)</span>', every_apt.group(0), re.S|re.DOTALL)
		
		if apt_size is not None:
			apt_size = apt_size.group(1)
			# print apt_size

			# if there is a br, then put it into a variable
			if re.search('(\d)br', apt_size):
				bedroom_num = re.search('(\d)br', apt_size)
				bedroom_num = bedroom_num.group(1)
			else:
				bedroom_num = ""

			# if there is a ft, then put it into a variable
			if re.search('<sup>', apt_size, re.S|re.DOTALL):
				sq_ft = re.search('(.+?)ft', apt_size)
				sq_ft = sq_ft.group(1)
				sq_ft = re.sub(' ', '', sq_ft) # search and replace (substitute) - searching for, replacing with, doing to (x)

				make_avg = bedroom_num / sq_ft
			else:
				sq_ft = ""

		data = [apt_price, bedroom_num, sq_ft, make_avg]
		MacFile.writerow(data)
		print data

# variables for function 
start_value = 0
base_url = 'https://toronto.craigslist.ca/search/apa?s='

while start_value < 601:
	full_url = base_url + str(start_value)

	html_page = urllib.urlopen(full_url).read() # .urlopen() takes one value, the URL to open # .read() as a method to read returns
	scrape_page(html_page)

	start_value = start_value + 120
	time.sleep(2)