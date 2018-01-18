# import libraries 
import time # wait commands (space out)
import re # regular expressions (text parser)
import urllib # Internet connection (socket connections, https)
import csv

date = time.time()

# ------------------------------------------------------------------------------------------------------------------- # 
# TODO:
# -- make new column that gets the *range* of episodes and seasons.
	# ie., Mark Sloan's season/episode code array should include every episode from every season
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
top_columns_character_details =  ['counter', 'name', 'diagnosis', 'actor', 'single_or_multiple_episodes', 'season_episode_code', 'first_episode_title_underscore', 'first_episode_title_text', 'last_episode_title_underscore', 'last_episode_title_text', 'seasons_array']

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
	lexiepedia = 0

	counter = 0
	character_name = "" # variable 1
	diagnosis = ""
	# actor = ""
	single_or_multiple_episodes = ""
	# season_episode_code = []

	first_episode_title_underscore  = ""
	first_episode_title_text  = ""
	
	last_episode_title_underscore = ""
	last_episode_title_text = ""

	# -----------------------------------------------------------------------------
	# Loop over every URL in the URL array
	# -----------------------------------------------------------------------------
	for url in url_array:
		# Only get 
		counter_test = 50
		counter_prod = 170
		if counter <= counter_prod:
			
			# print url
			print '-----------------------------------------------------------------------------------'
			print url
			
			# Open each page and get the contents
			url_page = urllib.urlopen(url).read()

			# -----------------------------------------------------------------------------
			# Get the sidebar markup
			get_aside = re.search('<aside class="portable-infobox pi-background (.+?) pi-layout-default">(.+?)</aside>', url_page, re.S|re.DOTALL)
			get_aside = get_aside.group(0)
			# -----------------------------------------------------------------------------
			# get_character_name_box = re.search('', get_aside, re.S|re.DOTALL)

			# -----------------------------------------------------------------------------
			# Character's name -- variable 1
			get_title_of_page = re.search('<h1 class="page-header__title">(.+?)</h1>', url_page, re.S|re.DOTALL)
			character_name = get_title_of_page.group(1)
			# -----------------------------------------------------------------------------
			# Episode title for first episode
			# -----------------------------------------------------------------------------
			get_appearances_box = re.search('<section class="pi-item pi-group pi-border-color"><h2 class="pi-item pi-header pi-secondary-font pi-item-spacing pi-secondary-background">Appearances</h2>(.+?)</section>', get_aside, re.S|re.DOTALL)
			if get_appearances_box is not None:
				
				get_appearances_content = re.finditer('<div class="pi-item pi-data pi-item-spacing pi-border-color">(.+?)<h3 class="pi-data-label pi-secondary-font">(.+?)</h3>(.+?)<div class="pi-data-value pi-font">(.+?)</div>(.+?)</div>', get_appearances_box.group(1), re.S|re.DOTALL)

				ep_loop = []

				for single in get_appearances_content:

					# -----------------------------------------------------------------------------
					# Is it the only character appearance or first of a multi-episode arc
					title_sdf = single.group(2)
					content_sdf = single.group(4)
					
					# print 'title: ', title_sdf, '| content: ', content_sdf

					actor = ""
					if title_sdf == "Portrayed by":
						
						print 'checking for actor name: ', content_sdf
						
						if '<a href=' not in content_sdf:
							actor = content_sdf
							print 'no link avail - actor', actor
						else:
							get_actor_name = re.search('<a href="/wiki/(.+?)" title="(.+?)">(.+?)</a>', content_sdf, re.S|re.DOTALL)
							actor = get_actor_name.group(3)
							print 'actor has url', actor
					else:
						actor = "No actor listed."
					
					# ---------------------------------------------------------------------------------------------------------------------------------------------
					# Only appearance 
					# ---------------------------------------------------------------------------------------------------------------------------------------------
					if title_sdf == "Only":
						only_appearence_in_pp = re.search('<b><a href="/wiki/Private_Practice" title="Private Practice">PP</a>:</b> <a href="/wiki/(.+?)" title="(.+?)">(.+?)</a>', content_sdf, re.S|re.DOTALL)
						
						if only_appearence_in_pp is not None:
							# print 'Only refers to an appearance on Private Practice: ', only_appearence_in_pp.group(0)
							pass
						else:
							# If the only text does not contain a reference to Private Practice
							# print 'Only refers to only Greys sighting: ', content_sdf

							single_or_multiple_episodes = "single"
								
							get_h3_title_text = re.search('<a href="/wiki/(.+?)" title="(.+?)">(.+?)</a>', content_sdf, re.S|re.DOTALL)
							
							first_episode_title_underscore = get_h3_title_text.group(1)
							first_episode_title_text = get_h3_title_text.group(2)

							last_episode_title_underscore = get_h3_title_text.group(1)
							last_episode_title_text = get_h3_title_text.group(2)

							ep_loop = [first_episode_title_underscore, last_episode_title_underscore]
							# print 'ep_loop for only - not including pp: ', ep_loop
					
					# ---------------------------------------------------------------------------------------------------------------------------------------------
					# First
					# ---------------------------------------------------------------------------------------------------------------------------------------------
					if title_sdf == "First":
						
						first_appearence_in_pp = re.search('<li><b><a href="/wiki/Private_Practice" title="Private Practice">PP</a>:</b> <a href="/wiki/(.+?)" title="(.+?)">(.+?)</a></li>', content_sdf, re.S|re.DOTALL)
						
						if first_appearence_in_pp is not None:
							# print 'First time in L.A. getting tan with new doctors: ', first_appearence_in_pp.group(0)
							pass
						else:
							single_or_multiple_episodes = "multiple"
							
							does_it_have_a_bold_tag = re.search('<b><a href="/wiki/Grey%27s_Anatomy" title="Grey\'s Anatomy">GA</a>:</b>(.+?)<a href="/wiki/(.+?)" title="(.+?)">(.+?)</a>', content_sdf, re.S|re.DOTALL)
							
							if does_it_have_a_bold_tag is not None:
								first_episode_title_underscore = does_it_have_a_bold_tag.group(2)
								first_episode_title_text = does_it_have_a_bold_tag.group(3)
								# print 'bold TAG ', first_episode_title_underscore, first_episode_title_text

								ep_loop.append(first_episode_title_underscore)

							else:
								get_h3_title_text = re.search('<a href="/wiki/(.+?)" title="(.+?)">(.+?)</a>', content_sdf, re.S|re.DOTALL)

								first_episode_title_underscore = get_h3_title_text.group(1)
								first_episode_title_text = get_h3_title_text.group(2)

								# print 'first episode title underscore', first_episode_title_underscore
								ep_loop.append(first_episode_title_underscore)
					
					# ---------------------------------------------------------------------------------------------------------------------------------------------
					# Last
					# ---------------------------------------------------------------------------------------------------------------------------------------------
					if title_sdf == "Last":
						last_appearence_in_pp = re.search('<li><b><a href="/wiki/Private_Practice" title="Private Practice">PP</a>:</b> <a href="/wiki/(.+?)" title="(.+?)">(.+?)</a></li>', content_sdf, re.S|re.DOTALL)

						if last_appearence_in_pp is not None:
							# print 'LAST time in L.A.: ', last_appearence_in_pp.group(0)
							pass
						else:
							single_or_multiple_episodes = "multiple"

							does_it_have_a_bold_tag = re.search('<b><a href="/wiki/Grey%27s_Anatomy" title="Grey\'s Anatomy">GA</a>:</b>(.+?)<a href="/wiki/(.+?)" title="(.+?)">(.+?)</a>', content_sdf, re.S|re.DOTALL)
							
							if does_it_have_a_bold_tag is not None:
								last_episode_title_underscore = does_it_have_a_bold_tag.group(2)
								last_episode_title_text = does_it_have_a_bold_tag.group(3)
								ep_loop.append(last_episode_title_underscore)
							else:
								get_h3_title_text = re.search('<a href="/wiki/(.+?)" title="(.+?)">(.+?)</a>', content_sdf, re.S|re.DOTALL)

								last_episode_title_underscore = get_h3_title_text.group(1)
								last_episode_title_text = get_h3_title_text.group(2)

								# print 'first episode title underscore', last_episode_title_underscore
								ep_loop.append(last_episode_title_underscore)

				# -----------------------------------------------------------------------------
				# Now go get the ep + season numbers, create the code
				season_episode_code = []
				seasons_array = []
				for single in ep_loop:
					# print 'single in ep_loop', single
					
					make_url = 'http://greysanatomy.wikia.com/wiki/' + single
					episode_page_url = urllib.urlopen(make_url).read()
					
					# print make_url
					# Find the ep title
					get_ep_number = re.search('<td class="pi-horizontal-group-item pi-data-value pi-font pi-border-color pi-item-spacing">Episode (.+?)</td>', episode_page_url, re.S|re.DOTALL)
					get_season_number = re.search('<td class="pi-horizontal-group-item pi-data-value pi-font pi-border-color pi-item-spacing">Season (.+?)</td>', episode_page_url, re.S|re.DOTALL)

					# Check that the season number is available
					if get_season_number is not None:
						get_season_number = get_season_number.group(1)

						# print 'get_season_number', get_season_number
						# print 'seasons_array', seasons_array

						if get_season_number in seasons_array:
							pass
						else:
							seasons_array.append(get_season_number)
					else:
						get_season_number = "ERROR"

					# Check that the episode number is available
					if get_ep_number is not None:
						get_ep_number = get_ep_number.group(1)
					else:
						get_ep_number = "ERROR"

					# print 'seasons_array', seasons_array
					code_season_number_episode_number = 'S-' + get_season_number + '-EP-' + get_ep_number
					season_episode_code.append(code_season_number_episode_number)

					# print 'season_episode_code', season_episode_code
					# -----------------------------------------------------------------------------
				
			else: 
				single_or_multiple_episodes = "no information available"
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
		# time.sleep(1)
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

		# Skip all the PP characters
		if get_character_names.group(1) != 'Bizzy_Forbes' and get_character_names.group(1) != 'Frances_Wilder' and get_character_names.group(1) != 'Dell_Parker' and get_character_names.group(1) != 'Anna_Wilder' and get_character_names.group(1) != 'Baby_Shepard' and get_character_names.group(1) != 'Pete_Wilder':
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