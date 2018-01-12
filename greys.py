# import libraries 
import time # wait commands (space out)
import re # regular expressions (text parser)
import urllib # Internet connection (socket connections, https)
import csv

date = time.time()

# ------------------------------------------------------------------------------------------------------------------- # 
# TODO:
# -- update the structure of the ep. title information to first loop over the data instead of first checking for First/Only
# 	-- move *if single_we.group(2) == "First":* to inside the loop
# ------------------------------------------------------------------------------------------------------------------- # 

# ------------------------------------------------------------------------------------------------------------------- # 
# For the CSV of character names + URLs
top_columns = ['name', 'url']

filename = str(date) + 'character-name-url.csv'
directory = '/Users/cbcwebdev02/Dropbox/2018/2018-01-04-intro-to-python/csv/'

CharacterNameAndURL = csv.writer(file(directory + filename, 'a'),dialect='excel')
CharacterNameAndURL.writerow(top_columns)

# ------------------------------------------------------------------------------------------------------------------- # 
# Make the headers for each column
top_columns_character_details =  ['counter', 'name', 'diagnosis', 'actor', 'single_or_multiple_episodes', 'episode_numbers', 'first_episode_title_underscore', 'first_episode_title_text', 'last_episode_title_underscore', 'last_episode_title_text', 'last_ep', 'seasons_array']

filename = str(date) + 'character-details.csv'
directory = '/Users/cbcwebdev02/Dropbox/2018/2018-01-04-intro-to-python/csv/'

CharacterDeatils = csv.writer(file(directory + filename, 'a'),dialect='excel')
CharacterDeatils.writerow(top_columns_character_details)

# ------------------------------------------------------------------------------------------------------------------- # 
# Loop over every page
# ------------------------------------------------------------------------------------------------------------------- # 

def scrape_character_pages(url_array):
	# -----------------------------------------------------------------------------
	# Set up empty variables -- top level variables 
	# -----------------------------------------------------------------------------
	counter = 0
	character_name = "" # variable 1
	diagnosis = ""
	actor = ""
	single_or_multiple_episodes = ""
	episode_numbers = []

	first_episode_title_underscore  = ""
	first_episode_title_text  = ""
	
	last_episode_title_underscore = ""
	last_episode_title_text = ""

	last_ep = ""
	seasons_array = []

	# -----------------------------------------------------------------------------
	# Loop over every URL in the URL array
	# -----------------------------------------------------------------------------
	for url in url_array:
		print '-----------------------------------------------------------------------------------'
		
		# Only get 
		if counter <= 25:
			
			# Open each page and get the contents
			url_page = urllib.urlopen(url).read()

			# -----------------------------------------------------------------------------
			# Get the sidebar markup
			get_aside = re.search('<aside class="portable-infobox pi-background (.+?) pi-layout-default">(.+?)</aside>', url_page, re.S|re.DOTALL)
			get_aside = get_aside.group(0)
			# -----------------------------------------------------------------------------

			# -----------------------------------------------------------------------------
			# Episode title for first episode
			get_appearances_box = re.search('<section class="pi-item pi-group pi-border-color"><h2 class="pi-item pi-header pi-secondary-font pi-item-spacing pi-secondary-background">Appearances</h2>(.+?)</section>', get_aside, re.S|re.DOTALL)
			if get_appearances_box is not None:
				# check_appearances = re.search('<div class="pi-item pi-data pi-item-spacing pi-border-color">(.+?)<h3 class="pi-data-label pi-secondary-font">(.+?)</h3>(.+?)</div>', get_appearances_box.group(1), re.S|re.DOTALL)
				# check_appearances = check_appearances.group(0)

				get_appearances_content = re.finditer('<div class="pi-item pi-data pi-item-spacing pi-border-color">(.+?)<h3 class="pi-data-label pi-secondary-font">(.+?)</h3>(.+?)<div class="pi-data-value pi-font"><a href="/wiki/(.+?)" title="(.+?)">(.+?)</a></div>(.+?)</div>', get_appearances_box.group(1), re.S|re.DOTALL)
				
				for single in get_appearances_content:
					# single = single

					# print single.group(0)

					get_single = re.search('<div class="pi-item pi-data pi-item-spacing pi-border-color">(.+?)<h3 class="pi-data-label pi-secondary-font">(.+?)</h3>(.+?)<div class="pi-data-value pi-font"><a href="/wiki/(.+?)" title="(.+?)">(.+?)</a></div>(.+?)</div>', single.group(0), re.S|re.DOTALL)
					print '--', get_single.group(3)
					
					# -----------------------------------------------------------------------------
					# Is it the only character appearance or first of a multi-episode arc
					is_first_or_only = single.group(2)
					if is_first_or_only == "Only":
						single_or_multiple_episodes = "single"

						first_episode_title_underscore = single.group(4)
						first_episode_title_text = single.group(5)

						last_episode_title_underscore = single.group(4)
						last_episode_title_text = single.group(5)

					elif is_first_or_only == "First":
						single_or_multiple_episodes = "multiple"

						first_episode_title_underscore = single.group(4)
						first_episode_title_text = single.group(5)

						last_episode_title_underscore = single.group(4)
						last_episode_title_text = single.group(5)

						# print first_episode_title_underscore
						# print first_episode_title_text
						# print last_episode_title_underscore
						# print last_episode_title_text

						
					# 	# Get the name of the first episode a character appeared in
					# 	get_title_text = re.search('<a href="/wiki/(.+?)" title="(.+?)">(.+?)</a>', check_appearances, re.S|re.DOTALL)
					# 	get_title_underscore = get_title_text.group(1)
					# 	get_title_text = get_title_text.group(2)

					# 	# print 'single_or_multiple_episodes', single_or_multiple_episodes
					# 	# print 'check_appearances', check_appearances

					elif is_first_or_only == "Last":
						is_first_or_only == "Last"
					
			else: 
				single_or_multiple_episodes = "no information available"
			# -----------------------------------------------------------------------------

				







				
			# -----------------------------------------------------------------------------

			











			# -----------------------------------------------------------------------------
			# Character's name -- variable 1
			get_character_name_box = re.search('<h2 class="pi-item pi-item-spacing pi-title">(.+?)</h2>', get_aside, re.S|re.DOTALL)
			character_name = get_character_name_box.group(1)
			# -----------------------------------------------------------------------------

			# -----------------------------------------------------------------------------
			# Character's diagnosis -- variable 3
			# -----------------------------------------------------------------------------
			get_character_diagnosis = re.search('<section class="pi-item pi-group pi-border-color"><h2 class="pi-item pi-header pi-secondary-font pi-item-spacing pi-secondary-background">Medical Information</h2>(.+?)</section>', get_aside, re.S|re.DOTALL)
			if get_character_diagnosis is not None:
				get_diagnosis = re.search('<div class="pi-item pi-data pi-item-spacing pi-border-color">(.+?)<h3 class="pi-data-label pi-secondary-font">Diagnosis</h3>(.+?)<div class="pi-data-value pi-font">(.+?)</div>(.+?)</div>', get_character_diagnosis.group(1), re.S|re.DOTALL)
				get_diagnosis = get_diagnosis.group(3)

				# Multiple diagnosis -- 
				check_for_single_multiple = re.search('<ul><li>(.+?)</li></ul>', get_diagnosis, re.S|re.DOTALL)
				if check_for_single_multiple is not None:
					split_diagnosis_on_list_item = check_for_single_multiple.group(1).split('</li><li>')
					diagnosis = split_diagnosis_on_list_item
				# Single diagnosis --
				else:
					diagnosis = [get_diagnosis]
			else:
				diagnosis = ["No diagnosis available"]
			# -----------------------------------------------------------------------------


			# -----------------------------------------------------------------------------
			# ***Last step***) Write the rows for each variable
			# -----------------------------------------------------------------------------
			
			character_data = [counter, character_name, diagnosis, actor, single_or_multiple_episodes, episode_numbers, first_episode_title_underscore, first_episode_title_text, last_episode_title_underscore, last_episode_title_text, last_ep, seasons_array]
			CharacterDeatils.writerow(character_data)

		# -----------------------------------------------------------------------------
		# Increment the number in the counter
		counter = counter + 1
		# -----------------------------------------------------------------------------



# ------------------------------------------------------------------------------------------------------------------- # 
# Get initial page - get all names
# ------------------------------------------------------------------------------------------------------------------- # 

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