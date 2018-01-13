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

directory = '/Users/jessiewillms/Dropbox/shonda-dead-people/shonda/dead-bodies-2/shondaland-dead-bodies/csv/'

CharacterNameAndURL = csv.writer(file(directory + filename, 'a'),dialect='excel')
CharacterNameAndURL.writerow(top_columns)

# ------------------------------------------------------------------------------------------------------------------- # 
# Make the headers for each column
top_columns_character_details =  ['counter', 'name', 'diagnosis', 'actor', 'single_or_multiple_episodes', 'season_episode_code', 'first_episode_title_underscore', 'first_episode_title_text', 'last_episode_title_underscore', 'last_episode_title_text', 'seasons_array']

filename = str(date) + 'character-details.csv'
directory = '/Users/jessiewillms/Dropbox/shonda-dead-people/shonda/dead-bodies-2/shondaland-dead-bodies/csv/'

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
	# season_episode_code = []

	first_episode_title_underscore  = ""
	first_episode_title_text  = ""
	
	last_episode_title_underscore = ""
	last_episode_title_text = ""

	seasons_array = []

	# -----------------------------------------------------------------------------
	# Loop over every URL in the URL array
	# -----------------------------------------------------------------------------
	for url in url_array:
		# Only get 
		counter_test = 20
		counter_prod = 170
		if counter <= counter_prod:
			
			# print url
			print '-----------------------------------------------------------------------------------'
			print url
			
			
			# Open each page and get the contents
			url_page = urllib.urlopen(url).read()
			# print url_page

			# -----------------------------------------------------------------------------
			# Get the sidebar markup
			get_aside = re.search('<aside class="portable-infobox pi-background (.+?) pi-layout-default">(.+?)</aside>', url_page, re.S|re.DOTALL)
			get_aside = get_aside.group(0)
			# -----------------------------------------------------------------------------

			# -----------------------------------------------------------------------------
			# Character's name -- variable 1
			get_title_of_page = re.search('<h1 class="page-header__title">(.+?)</h1>', url_page, re.S|re.DOTALL)
			# get_character_name_box = re.search('', get_aside, re.S|re.DOTALL)
			character_name = '1',
			# get_character_name_box.group(1)
			print get_title_of_page.group(1)
			# -----------------------------------------------------------------------------
			# 
			# -----------------------------------------------------------------------------
			# Episode title for first episode
			get_appearances_box = re.search('<section class="pi-item pi-group pi-border-color"><h2 class="pi-item pi-header pi-secondary-font pi-item-spacing pi-secondary-background">Appearances</h2>(.+?)</section>', get_aside, re.S|re.DOTALL)
			if get_appearances_box is not None:
				# check_appearances = re.search('<div class="pi-item pi-data pi-item-spacing pi-border-color">(.+?)<h3 class="pi-data-label pi-secondary-font">(.+?)</h3>(.+?)</div>', get_appearances_box.group(1), re.S|re.DOTALL)
				# check_appearances = check_appearances.group(0)

				get_appearances_content = re.finditer('<div class="pi-item pi-data pi-item-spacing pi-border-color">(.+?)<h3 class="pi-data-label pi-secondary-font">(.+?)</h3>(.+?)<div class="pi-data-value pi-font"><a href="/wiki/(.+?)" title="(.+?)">(.+?)</a></div>(.+?)</div>', get_appearances_box.group(1), re.S|re.DOTALL)
				
				ep_loop = []
				for single in get_appearances_content:
					get_single = re.search('<div class="pi-item pi-data pi-item-spacing pi-border-color">(.+?)<h3 class="pi-data-label pi-secondary-font">(.+?)</h3>(.+?)<div class="pi-data-value pi-font"><a href="/wiki/(.+?)" title="(.+?)">(.+?)</a></div>(.+?)</div>', single.group(0), re.S|re.DOTALL)
					# print '--', get_single.group(3)
					
					# -----------------------------------------------------------------------------
					# Is it the only character appearance or first of a multi-episode arc
					is_first_or_only = single.group(2)
					# print is_first_or_only
					if is_first_or_only == "Only":
						single_or_multiple_episodes = "single"

						first_episode_title_underscore = single.group(4)
						first_episode_title_text = single.group(5)

						last_episode_title_underscore = single.group(4)
						last_episode_title_text = single.group(5)

						ep_loop = [first_episode_title_underscore]

					elif is_first_or_only == "First":

						# print 'first - therefor, multiple episode arc'.
						single_or_multiple_episodes = "multiple"

						first_episode_title_underscore = single.group(4)
						first_episode_title_text = single.group(5)

						if character_name == "Alexandra Caroline Grey":
							print 'lexie first name'

						ep_loop.append(first_episode_title_underscore)

					elif is_first_or_only == "Last":
						is_first_or_only == "Last"
						
						last_episode_title_underscore = single.group(4)
						last_episode_title_text = single.group(5)

						ep_loop.append(last_episode_title_underscore)
					# print 'ep_loop', ep_loop
						# print 'last_episode_title_text', last_episode_title_text
				
				# -----------------------------------------------------------------------------
				# Now go get the ep + season numbers, create the code
				# print 'ep_loop after for sinlge in appearance', ep_loop
				season_episode_code = []
				for single in ep_loop:
					make_url = 'http://greysanatomy.wikia.com/wiki/' + single
					episode_page_url = urllib.urlopen(make_url).read()
					
					print make_url
					# Find the ep title
					get_ep_number = re.search('<td class="pi-horizontal-group-item pi-data-value pi-font pi-border-color pi-item-spacing">Episode (.+?)</td>', episode_page_url, re.S|re.DOTALL)
					get_season_number = re.search('<td class="pi-horizontal-group-item pi-data-value pi-font pi-border-color pi-item-spacing">Season (.+?)</td>', episode_page_url, re.S|re.DOTALL)

					# Check that the season number is available
					if get_season_number is not None:
						get_season_number = get_season_number.group(1)
					else:
						get_season_number = "ERROR"

					# Check that the episode number is available
					if get_ep_number is not None:
						get_ep_number = get_ep_number.group(1)
					else:
						get_ep_number = "ERROR"

					code_season_number_episode_number = 'S-' + get_season_number + '-EP-' + get_ep_number
					season_episode_code.append(code_season_number_episode_number)

					# print 'season_episode_code', season_episode_code
					# -----------------------------------------------------------------------------
				
			else: 
				single_or_multiple_episodes = "no information available"
			# -----------------------------------------------------------------------------



				
			# -----------------------------------------------------------------------------

			











			

			# -----------------------------------------------------------------------------
			# Character's diagnosis -- variable 3
			# -----------------------------------------------------------------------------
			get_character_diagnosis = re.search('<section class="pi-item pi-group pi-border-color"><h2 class="pi-item pi-header pi-secondary-font pi-item-spacing pi-secondary-background">Medical Information</h2>(.+?)</section>', get_aside, re.S|re.DOTALL)
			if get_character_diagnosis is not None:
				get_diagnosis = re.search('<div class="pi-item pi-data pi-item-spacing pi-border-color">(.+?)<h3 class="pi-data-label pi-secondary-font">Diagnosis</h3>(.+?)<div class="pi-data-value pi-font">(.+?)</div>(.+?)</div>', get_character_diagnosis.group(1), re.S|re.DOTALL)

				# Multiple diagnosis -- 
				if get_diagnosis is not None:
					get_diagnosis = get_diagnosis.group(3)
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
			# ***Last step***  Write the rows for each variable
			# -----------------------------------------------------------------------------
			
			character_data = [counter, character_name, diagnosis, actor, single_or_multiple_episodes, season_episode_code, first_episode_title_underscore, first_episode_title_text, last_episode_title_underscore, last_episode_title_text, seasons_array]
			CharacterDeatils.writerow(character_data)

		# -----------------------------------------------------------------------------
		# Increment the number in the counter
		counter = counter + 1

		# Reduce calls to the site to every one (1) second
		time.sleep(1)
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