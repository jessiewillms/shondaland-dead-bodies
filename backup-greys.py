

# print top_columns
# top_columns2 = ['status', 'title']

# MacFile = csv.writer(file('greysanatomy.csv', 'a'),dialect='excel')
# MacFile.writerow(top_columns)

filename = str(date) + '-greys-anatomy .csv'
directory = '/Users/cbcwebdev02/Dropbox/2018/2018-01-04-intro-to-python/csv/'

MacFile_Greys = csv.writer(file(directory + filename, 'a'),dialect='excel')
MacFile_Greys.writerow(top_columns)

def scrape_character_pages(url_array):
	# print url_array

	pages_array = []
	for url in url_array:
		url_page = urllib.urlopen(url).read()
		print 'url'
		
		get_aside = re.search('<aside class="portable-infobox pi-background pi-theme-patient pi-layout-default">(.+?)</aside>', url_page, re.S|re.DOTALL)

		if get_aside is not None:
			get_aside = get_aside.group(1)
			character_died = re.search('<div class="pi-item pi-data pi-item-spacing pi-border-color">(.+?)<h3 class="pi-data-label pi-secondary-font">Died</h3>(.+?)<div class="pi-data-value pi-font">(.+?) <a href="/wiki/(.+?)" title="(.+?)">(.+?)</div>(.+?)</div>', get_aside, re.S|re.DOTALL)
			character_name = re.search('<h2 class="pi-item pi-item-spacing pi-title">(.+?)</h2>', get_aside, re.S|re.DOTALL)
			if character_name is not None:
				name = character_name

			if character_died is not None:
				# 3, 4, 
				# 5 - place
				time = character_died.group(6)
				place = character_died.group(5)
			else:
				character_died = ""
				# print character_died

		data = [name, time, place]
		MacFile_Greys.writerow(data)
		pages_array.append(data)

	print pages_array

def scrape_page(html_page):
	# print html_page;

	wrapper = re.search('<table width="100%">(.+?)</table>', html_page, re.S|re.DOTALL)

	# print wrapper
	# print wrapper.group(0)
	table_content = wrapper.group(0)
	# print wrapper.group(1)
	
	url_array = []
	for single in re.finditer('<li><a href="/wiki/(.+?)</li>', table_content, re.S|re.DOTALL):
		# print single.group(0)
		# print 'single'

		get_character_names = re.search('<a href="/wiki/(.+?)" title="(.+?)">(.+?)</a>', single.group(0), re.S|re.DOTALL)

		url = 'http://greysanatomy.wikia.com/wiki/' + get_character_names.group(1)
		url_array.append(url)

		character = get_character_names.group(3)

		# data = [url, character]
		# MacFile.writerow(data)

	scrape_character_pages(url_array)
	# print url_array

base_url = 'http://greysanatomy.wikia.com/wiki/Category:Deceased_Characters'

# while start_value < 101:
full_url = base_url

html_page = urllib.urlopen(base_url).read() # .urlopen() takes one value, the URL to open # .read() as a method to read returns
scrape_page(html_page)

# start_value = start_value + 10
# time.sleep(2)