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
# top_columns_character_details = ['character','date_of_death', 'episode_title', 'season_number', 'diagnosis', 'first_ep', 'last_ep', 'seasons_array']
top_columns_character_details =  ['counter', 'name', 'actor', 'single_or_multiple_episodes', 'first_ep', 'last_ep', 'seasons_array']

filename = str(date) + 'character-details.csv'
directory = '/Users/cbcwebdev02/Dropbox/2018/2018-01-04-intro-to-python/csv/'

CharacterDeatils = csv.writer(file(directory + filename, 'a'),dialect='excel')
CharacterDeatils.writerow(top_columns_character_details)

# ------------------------------------------------------------------------------------------------------------------- # 
# Loop over every page
def scrape_character_pages(url_array):
	# print 'scrape each page is called ... '

	counter = 0
	# print counter
	for url in url_array:
		print '-----------------------------------------------------------------------------------'
		print url
		if counter <= 200:
			# print counter
			url_page = urllib.urlopen(url).read()

			# Go into the url_page guts and find the aside div
			# portable-infobox pi-background pi-theme-attending pi-layout-default
			get_aside = re.search('<aside class="portable-infobox pi-background (.+?) pi-layout-default">(.+?)</aside>', url_page, re.S|re.DOTALL)
			get_aside_content = get_aside.group(2)


			# If the aside is not empty, print the content (ie., what is in the .group())
			if get_aside_content is not None:
				get_aside = get_aside_content
				# print get_aside
				#  ..group(2)
				
				character_died = re.search('<div class="pi-item pi-data pi-item-spacing pi-border-color">(.+?)<h3 class="pi-data-label pi-secondary-font">Died</h3>(.+?)<div class="pi-data-value pi-font">(.+?) <a href="/wiki/(.+?)" title="(.+?)">(.+?)</div>(.+?)</div>', get_aside, re.S|re.DOTALL)
				
				# Character medical information
				character_medical_info = re.search('<section class="pi-item pi-group pi-border-color"><h2 class="pi-item pi-header pi-secondary-font pi-item-spacing pi-secondary-background">Medical Information</h2>(.+?)</section>', get_aside, re.S|re.DOTALL)
				
				# If there is medical information
				if character_medical_info is not None:
					get_full_medical_info = character_medical_info.group(1)
					get_diagnosis = re.search('<div class="pi-item pi-data pi-item-spacing pi-border-color">(.+?)<h3 class="pi-data-label pi-secondary-font">Diagnosis</h3>(.+?)<div class="pi-data-value pi-font">(.+?)</div>(.+?)</div>', character_medical_info.group(1), re.S|re.DOTALL)

					diagnosis = []
					if get_diagnosis is not None:
						get_diagnosis = get_diagnosis.group(3)

						get_multiple_diagnosis = re.search('<ul><li>(.+?)</li></ul>', get_diagnosis, re.S|re.DOTALL)

						# Check if there are multiple reasons someone died
						if get_multiple_diagnosis:
							get_multiple_diagnosis = get_multiple_diagnosis.group(1)
							each_diagnosis = get_multiple_diagnosis.split('</li><li>')
							diagnosis = each_diagnosis
						else:
							diagnosis = get_diagnosis

					else: 
						get_diagnosis = "No Diagnosis"
				
				# Get the name of the character
				get_name_box = re.search('<h2 class="pi-item pi-item-spacing pi-title">(.+?)</h2>', get_aside, re.S|re.DOTALL)
				name = get_name_box.group(1)

				# Get the ep/season information - season number + episode title
				get_appearances_box = re.search('<section class="pi-item pi-group pi-border-color"><h2 class="pi-item pi-header pi-secondary-font pi-item-spacing pi-secondary-background">Appearances</h2>(.+?)</section>', get_aside, re.S|re.DOTALL)
				if get_appearances_box is not None:
					get_appearances_content = get_appearances_box.group(1)
					# print get_appearances_content

					# Appearances box
					# -----------------------------------------------------------------------------
					check_appearances = re.search('<div class="pi-item pi-data pi-item-spacing pi-border-color">(.+?)<h3 class="pi-data-label pi-secondary-font">(.+?)</h3>(.+?)</div>', get_appearances_content, re.S|re.DOTALL)

					check_only_or_first = check_appearances.group(2)

					# -----------------------------------------------------------------------------
					# Build some empty variables 
					single_or_multiple_episodes = ""
					first_ep = ""
					last_ep = ""
					seasons_array = ""
					# -----------------------------------------------------------------------------

					if check_only_or_first == "Only":
						get_only_appearance = re.search('<div class="pi-item pi-data pi-item-spacing pi-border-color">(.+?)<h3 class="pi-data-label pi-secondary-font">(.+?)</h3>(.+?)<div class="pi-data-value pi-font"><a href="/wiki/(.+?)" title="(.+?)">(.+?)</a></div>', get_appearances_content, re.S|re.DOTALL)
						first_ep = get_only_appearance.group(5)

						get_guts = re.finditer('<div class="pi-item pi-data pi-item-spacing pi-border-color">(.+?)<h3 class="pi-data-label pi-secondary-font">(.+?)</h3>(.+?)</div>', get_appearances_content, re.S|re.DOTALL)
						# get_actor_name = re.search('<div class="pi-item pi-data pi-item-spacing pi-border-color">(.+?)<h3 class="pi-data-label pi-secondary-font">Portrayed by</h3>(.+?)<div class="pi-data-value pi-font"><a href="/wiki/(.+?)" title="(.+?)">(.+?)</a></div>(.+?)</div>', get_appearances_content, re.S|re.DOTALL)

						# print 'Only -- get single actor name'
						for single in get_guts:
							
							# print 'single.group(2)'
							
							get_text = single.group(2)

							if get_text == "Portrayed by":
								# print "yes"
								get_text_field = single.group(3)
								
								great = re.search('<a href="/wiki/(.+?)" title="(.+?)">(.+?)</a>', get_text_field, re.S|re.DOTALL)
								if great is not None:
									print 'great'
									print great.group(3)
									# get_text_field_text = re.search('<a href="/wiki/(.+?)" title="(.+?)">(.+?)</a>', get_text_field, re.S|re.DOTALL)
									# actor =  get_text_field_text.group(3)
								else:
									print 'no url'
								# print 'no'
# /								get_actor_link = single.group(0)
 # .								print get_actor_link
							# 	# Sometimes the actor name is not a link (anchor tag)
							# 	if "</a>" not in get_actor_link: 
							# 		actor = get_actor_link
							# 		print 'no url for actor'
							# 		print actor
							# 	else:
							# 		get_actor_link_text = re.search('<a href="/wiki/(.+?)" title="(.+?)">(.+?)</a>', get_actor_link, re.S|re.DOTALL)
							# 		# print 'get_actor_link_text'
							# 		actor = get_actor_link_text.group(2)
							# 		print 'has a link for the actor'
							# 		print actor
							# else:
							# 	actor = "no 'Portrayed by' text for character"
							# 	print 'no actor box'
							# 	print actor
						actor = "123"
						single_or_multiple_episodes = "single"
						last_ep = ""
						seasons_array = ""
					
					# If there are multiple episodes
					elif check_only_or_first == "First":
						# print check_only_or_first
						single_or_multiple_episodes = "multiple"

						# --------------------------------------------------------------------
						# Get content from the appearances div/box
						get_first_appearance = re.search('<div class="pi-item pi-data pi-item-spacing pi-border-color">(.+?)<h3 class="pi-data-label pi-secondary-font">(.+?)</h3>(.+?)<div class="pi-data-value pi-font">(.+?)</div>(.+?)</div>', get_appearances_content, re.S|re.DOTALL)
						
						# Get the guts of the box (ie., all the content in the div)
						get_guts = re.finditer('<div class="pi-item pi-data pi-item-spacing pi-border-color">(.+?)<h3 class="pi-data-label pi-secondary-font">(.+?)</h3>(.+?)</div>', get_appearances_content, re.S|re.DOTALL)
						# print dir(get_guts) # check what is in the array created by .finditer

						# --------------------------------------------------------------------
						# Loop over the get_guts array (ie., content in Appearances) and create
						# the necessary variables for the ep. titles and season numbers
						for single in get_guts:
							# print single.group(0)

							# Search each item in get_guts to look for content pattern(s)
							single_we = re.search('<div class="pi-item pi-data pi-item-spacing pi-border-color">(.+?)<h3 class="pi-data-label pi-secondary-font">(.+?)</h3>(.+?)<div class="pi-data-value pi-font">(.+?)</div>', single.group(0), re.S|re.DOTALL)

							# If the <h3> tag is for the first appearance (ie., they have a multi-episode arc)
							if single_we.group(2) == "First":
								first = single_we.group(4)
								first_ep = re.search('<a href="/wiki/(.+?)" title="(.+?)">(.+?)</a>', first, re.S|re.DOTALL)
								first_ep = first_ep.group(3)
								# print first_ep

							# When did they last appear
							elif single_we.group(2) == "Last":
								last = single_we.group(4)
								last_ep = re.search('<a href="/wiki/(.+?)" title="(.+?)">(.+?)</a>', last, re.S|re.DOTALL)
								last_ep = last_ep.group(2)
								# print last.group(0)
							# In what season(s) did they appear?
							elif single_we.group(2) == "Seasons":
								seasons = single_we.group(4)
								
								# print seasons
								get_seasons_nums = re.finditer('<a href="/wiki/(.+?)" title="(.+?) \(Grey\'s Anatomy\)">(.+?)</a>', seasons, re.S|re.DOTALL)
								seasons_array = []
								for single in get_seasons_nums:
									# print single.group(2)
									# Check that the season information relates to Grey's - not Private Practice (ie., crossovers)
									if single.group(3) != "GA" and single.group(3) != "PP": 
										seasons = single.group(3)
										seasons_array.append(seasons)
								# print seasons_array
							elif single_we.group(2) == "Portrayed by":
								get_actor = single_we.group(4)
								# get the actor's name
								get_actor_name = re.search('<a href="/wiki/(.+?)" title="(.+?)">(.+?)</a>', get_actor, re.S|re.DOTALL)
								actor = get_actor_name.group(2)
								# print actor
					else:
						single_or_multiple_episodes = "error"
						print single_or_multiple_episodes

					# Make the array to push into the spreadsheet
					# print 'print single_or_multiple_episodes'
					# print single_or_multiple_episodes
					# print 'print actor'
					# print actor
					character_data = [counter, name, actor, single_or_multiple_episodes, first_ep, last_ep, seasons_array]
					CharacterDeatils.writerow(character_data)
					
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

			
			else:
				print 'no aside'
				# print url
				# print name
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