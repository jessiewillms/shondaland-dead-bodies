# import libraries 
import time # wait commands (space out)
import re # regular expressions (text parser)
import urllib # Internet connection (socket connections, https)
import csv

date = time.time()

# ------------------------------------------------------------------------------------------------------------------- # 
# For the CSV of character names + URLs
top_columns = ['name', 'url']

filename = str(date) + 'character-name-url.csv'
directory = '/Users/cbcwebdev02/Dropbox/2018/2018-01-04-intro-to-python/csv/'

CharacterNameAndURL = csv.writer(file(directory + filename, 'a'),dialect='excel')
CharacterNameAndURL.writerow(top_columns)

# ------------------------------------------------------------------------------------------------------------------- # 
# For the CSV of *each character's name, cause of death, etc.*)
top_columns_character_details = ['character','date_of_death', 'episode_title', 'season_number']

filename = str(date) + 'character-details.csv'
directory = '/Users/cbcwebdev02/Dropbox/2018/2018-01-04-intro-to-python/csv/'

CharacterDeatils = csv.writer(file(directory + filename, 'a'),dialect='excel')
CharacterDeatils.writerow(top_columns_character_details)

# ------------------------------------------------------------------------------------------------------------------- # 
# Loop over every page
def scrape_character_pages(url_array):
	print 'scrape each page is called ... '

	counter = 0
	print counter

		
	for url in url_array:
		# print url
		if counter <= 10:
			url_page = urllib.urlopen(url).read()

			# Go into the url_page guts and find the aside div
			get_aside = re.search('<aside class="portable-infobox pi-background pi-theme-patient pi-layout-default">(.+?)</aside>', url_page, re.S|re.DOTALL)

			# If the aside is not empty, print the content (ie., what is in the .group())
			if get_aside is not None:
				get_aside = get_aside.group(1)
				character_died = re.search('<div class="pi-item pi-data pi-item-spacing pi-border-color">(.+?)<h3 class="pi-data-label pi-secondary-font">Died</h3>(.+?)<div class="pi-data-value pi-font">(.+?) <a href="/wiki/(.+?)" title="(.+?)">(.+?)</div>(.+?)</div>', get_aside, re.S|re.DOTALL)
				
				character_medical_info = re.search('<section class="pi-item pi-group pi-border-color"><h2 class="pi-item pi-header pi-secondary-font pi-item-spacing pi-secondary-background">Appearances</h2>(.+?)</section>', get_aside, re.S|re.DOTALL)

				# Gets *everything* from Appearances onward -> 
				if character_medical_info is not None:
					full_character_info = character_medical_info.group(1)
					print '! get season ----------------------------------!'	
					# print full_character_info

					get_episode_title = re.search('<div class="pi-item pi-data pi-item-spacing pi-border-color">(.+?)<h3 class="pi-data-label pi-secondary-font">Only</h3>(.+?)<div class="pi-data-value pi-font"><a href="/wiki/(.+?)" title="(.+?)">(.+?)</a>(.+?)</div>(.+?)</div>', full_character_info, re.S|re.DOTALL)

					get_season = re.search('<h3 class="pi-data-label pi-secondary-font">Seasons</h3>(.+?)<div class="pi-data-value pi-font"><b><a href="/wiki/Grey%27s_Anatomy" title="(.+?)">GA</a>:</b> <a href="/wiki/(.+?)" title="(.+?)">(.+?)</a></div>', full_character_info, re.S|re.DOTALL)

					if get_season is not None:
						season_number = get_season.group(5)
						print season_number
					
					if get_episode_title is not None:
						episode_title = get_episode_title.group(4)
						# print episode_title

				else:	
					print 'n/a'

				# Get the character name ----------------------------------------------------------------------
				character_name = re.search('<h2 class="pi-item pi-item-spacing pi-title">(.+?)</h2>', get_aside, re.S|re.DOTALL)
				if character_name is not None:
					name = character_name.group(1)
				else:
					name = ""

				if character_died is not None:
					time = character_died.group(3)
				else:
					time = ""

				# Make the array to push into the spreadsheet
				data = [name, time, episode_title, season_number]
				print data
				CharacterDeatils.writerow(data)
			counter = counter + 1

# Get initial page - get all names
def scrape_page(html_page):

	wrapper = re.search('<table width="100%">(.+?)</table>', html_page, re.S|re.DOTALL)
	table_content = wrapper.group(0)
	
	url_array = []

	for single in re.finditer('<li><a href="/wiki/(.+?)</li>', table_content, re.S|re.DOTALL):
		get_character_names = re.search('<a href="/wiki/(.+?)" title="(.+?)">(.+?)</a>', single.group(0), re.S|re.DOTALL)

		url = 'http://greysanatomy.wikia.com/wiki/' + get_character_names.group(1)
		url_array.append(url)
		character = get_character_names.group(3)

		# print url
		CharacterNameAndURL.writerow([character, url])

	scrape_character_pages(url_array)

# URLs to access
base_url = 'http://greysanatomy.wikia.com/wiki/Category:Deceased_Characters'
full_url = base_url

html_page = urllib.urlopen(base_url).read() # .urlopen() takes one value, the URL to open # .read() as a method to read returns
scrape_page(html_page)