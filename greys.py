
# import libraries 
import time # wait commands (space out)
import re # regular expressions (text parser)
import urllib # Internet connection (socket connections, https)
import csv

date = time.time()

# ------------------------------------------------------------------------------------------------------------------- 
# For the CSV of character names + URLs
top_columns = ['name', 'url']

filename = str(date) + 'character-name-url.csv'

directory = '/Users/jessiewillms/Dropbox/shonda-greys-db/shondaland-dead-bodies/csv/character_list/'
# directory = '/Users/cbcwebdev02/Dropbox/2018/2018-01-04-intro-to-python/csv/'

CharacterNameAndURL = csv.writer(file(directory + filename, 'a'),dialect='excel')
CharacterNameAndURL.writerow(top_columns)

# ------------------------------------------------------------------------------------------------------------------- # 
# Make the headers for each column
top_columns_character_details =  ['counter', 'name', 'image', 'character_type','diagnosis', 'cause_of_death', 'treatment', 'actor', 'single_or_multiple_episodes', 'season_episode_code', 'first_episode_title_underscore', 'first_episode_title_text', 'last_episode_title_underscore', 'last_episode_title_text', 'seasons_array']

filename = str(date) + 'character-details.csv'
directory = '/Users/jessiewillms/Dropbox/shonda-greys-db/shondaland-dead-bodies/csv/character_details/'

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

	# -----------------------------------------------------------------------------
	# Loop over every URL in the URL array
	# -----------------------------------------------------------------------------
	character_type_array = []
	for url in url_array:
		# Only get 
		counter_test = 50
		counter_prod = 170
		
		# if counter >= 60 and counter <= 70:
		if counter < counter_prod:
			print '-----------------------------------------------------------------------------------', url
			
			# -----------------------------------------------------------------------------
			# Open each page and get the contents
			# -----------------------------------------------------------------------------
			url_page = urllib.urlopen(url).read()

			# -----------------------------------------------------------------------------
			check_character_is_greys_character = re.search('<div class="page-header__categories-links">(.+?)<a href="/wiki/Category:Characters" data-tracking="categories-top-0">Characters</a>,(.+?)<a href="/wiki/Category:GA_Characters" data-tracking="categories-top-1">GA Characters</a>(.+?)</div>', url_page, re.S|re.DOTALL)
			
			if check_character_is_greys_character is not None:
				character_name = "" # variable 1
				diagnosis = []
				cause_of_death = []
				treatment = []
				actor = ""
				image = ""
				single_or_multiple_episodes = ""

				appearances = []

				first_episode_title_underscore  = ""
				first_episode_title_text  = ""
				
				last_episode_title_underscore = ""
				last_episode_title_text = ""
				ep_loop = []

				season_episode_code = []
				seasons_array = []

				# -----------------------------------------------------------------------------
				# For each character, get every episode they appeared in 
				# -----------------------------------------------------------------------------
				for every_apt in re.finditer('<table(.+?)>(.+?)</table>', url_page, re.S|re.DOTALL):
					tbls = every_apt.group(2)
					
					for every_tr in re.finditer('<tr valign="top" (.+?)>(.+?)</tr>', tbls, re.S|re.DOTALL):
						every_tr = every_tr.group(2)
						
						for every_td in re.finditer('<td>"<a href="(.+?)" title="(.+?)">(.+?)</a>"(.+?)</td>', every_tr, re.S|re.DOTALL):

							episode_title = every_td.group(3)

							ep_url = 'http://greysanatomy.wikia.com' + every_td.group(1)
							get_ep_page = urllib.urlopen(ep_url).read()

							get_ep_season_nums = re.search('<tr>(.+?)<td class="pi-horizontal-group-item pi-data-value pi-font pi-border-color pi-item-spacing">Season (.+?)</td>(.+?)<td class="pi-horizontal-group-item pi-data-value pi-font pi-border-color pi-item-spacing">Episode (.+?)</td>(.+?)</tr>', get_ep_page, re.S|re.DOTALL)
								
							if get_ep_season_nums.group(0) is not None:
								get_season_number = get_ep_season_nums.group(2)
								get_ep_number = get_ep_season_nums.group(4)

							code_season_number_episode_number = 'S-' + get_season_number + '-EP-' + get_ep_number
							season_episode_code.append(code_season_number_episode_number)
							# print code_season_number_episode_number

				# -----------------------------------------------------------------------------
				# Get the sidebar markup
				# -----------------------------------------------------------------------------
				get_aside = re.search('<aside class="portable-infobox pi-background (.+?) pi-layout-default">(.+?)</aside>', url_page, re.S|re.DOTALL)
				get_character_type = get_aside.group(1)
				get_aside = get_aside.group(0)
				# -----------------------------------------------------------------------------

				# -----------------------------------------------------------------------------
				# Character's photo
				# -----------------------------------------------------------------------------
				get_image_url = re.search('<img src="(.+?)" (.+?) class="pi-image-thumbnail" (.+?)>', get_aside, re.S|re.DOTALL)
				if get_image_url is not None:
					image = get_image_url.group(1)

				# -----------------------------------------------------------------------------
				# Character's name
				# -----------------------------------------------------------------------------
				get_title_of_page = re.search('<h1 class="page-header__title">(.+?)</h1>', url_page, re.S|re.DOTALL)
				character_name = get_title_of_page.group(1)
				# -----------------------------------------------------------------------------
				
				# -----------------------------------------------------------------------------
				# Get the type of character - a doctor (attending, resident, intern), a dog, a skeleton
				# -----------------------------------------------------------------------------
				character_type = get_character_type.split('pi-theme-')[1]
				if character_type not in character_type_array:
					if character_type == 'internresident':
						character_type = "intern resident"
					
					character_type_array.append(character_type)
				# -----------------------------------------------------------------------------

				# -----------------------------------------------------------------------------
				# Episode title for first episode
				# -----------------------------------------------------------------------------
				get_appearances_box = re.search('<section class="pi-item pi-group pi-border-color"><h2 class="pi-item pi-header pi-secondary-font pi-item-spacing pi-secondary-background">Appearances</h2>(.+?)</section>', get_aside, re.S|re.DOTALL)
				if get_appearances_box is not None:
					
					get_appearances_content = re.finditer('<div class="pi-item pi-data pi-item-spacing pi-border-color">(.+?)<h3 class="pi-data-label pi-secondary-font">(.+?)</h3>(.+?)<div class="pi-data-value pi-font">(.+?)</div>(.+?)</div>', get_appearances_box.group(1), re.S|re.DOTALL)

					for single in get_appearances_content:

						# -----------------------------------------------------------------------------
						# Is it the only character appearance or first of a multi-episode arc
						title_sdf = single.group(2)
						content_sdf = single.group(4)

						if title_sdf == "Portrayed by":
							
							if '<a href=' not in content_sdf:
								actor = content_sdf
							else:
								get_actor_name = re.search('<a href="/wiki/(.+?)" title="(.+?)">(.+?)</a>', content_sdf, re.S|re.DOTALL)
								actor = get_actor_name.group(3)
						else:
							actor = "No actor listed."
						
						# ---------------------------------------------------------------------------------------------------------------------------------------------
						# Only appearance 
						# ---------------------------------------------------------------------------------------------------------------------------------------------
						if title_sdf == "Only":
							only_appearence_in_pp = re.search('<b><a href="/wiki/Private_Practice" title="Private Practice">PP</a>:</b> <a href="/wiki/(.+?)" title="(.+?)">(.+?)</a>', content_sdf, re.S|re.DOTALL)
							
							if only_appearence_in_pp is not None:
								pass
							else:
								# If the only text does not contain a reference to Private Practice

								single_or_multiple_episodes = "single"
									
								get_h3_title_text = re.search('<a href="/wiki/(.+?)" title="(.+?)">(.+?)</a>', content_sdf, re.S|re.DOTALL)
								
								first_episode_title_underscore = get_h3_title_text.group(1)
								first_episode_title_text = get_h3_title_text.group(2)

								last_episode_title_underscore = get_h3_title_text.group(1)
								last_episode_title_text = get_h3_title_text.group(2)

								ep_url = 'http://greysanatomy.wikia.com/' + first_episode_title_underscore

								get_ep_page = urllib.urlopen(ep_url).read()

								get_ep_season_nums = re.search('<tr>(.+?)<td class="pi-horizontal-group-item pi-data-value pi-font pi-border-color pi-item-spacing">Season (.+?)</td>(.+?)<td class="pi-horizontal-group-item pi-data-value pi-font pi-border-color pi-item-spacing">Episode (.+?)</td>(.+?)</tr>', get_ep_page, re.S|re.DOTALL)
									
								if get_ep_season_nums.group(0) is not None:
									get_season_number = get_ep_season_nums.group(2)
									get_ep_number = get_ep_season_nums.group(4)

								code_season_number_episode_number = 'S-' + get_season_number + '-EP-' + get_ep_number
								season_episode_code.append(code_season_number_episode_number)
								
								ep_loop = [first_episode_title_underscore, last_episode_title_underscore]
						
						# ---------------------------------------------------------------------------------------------------------------------------------------------
						# First section - "First" h3 tag found
						# ---------------------------------------------------------------------------------------------------------------------------------------------
						if title_sdf == "First":
							
							# ---------------------------------------------------------------------------------------------------------------------------------------------
							# It's PP -- skip it
							# ---------------------------------------------------------------------------------------------------------------------------------------------
							first_appearence_in_pp = re.search('<li><b><a href="/wiki/Private_Practice" title="Private Practice">PP</a>:</b> <a href="/wiki/(.+?)" title="(.+?)">(.+?)</a></li>', content_sdf, re.S|re.DOTALL)
							if first_appearence_in_pp is not None:
								pass
							
							# ---------------------------------------------------------------------------------------------------------------------------------------------
							# It's GA
							# ---------------------------------------------------------------------------------------------------------------------------------------------
							first_appearence_in_ga = re.search('<b><a href="/wiki/Grey%27s_Anatomy" title="Grey\'s Anatomy">GA</a>:</b>', content_sdf, re.S|re.DOTALL)
							if first_appearence_in_ga is not None:
								single_or_multiple_episodes = "multiple"
								
								if first_appearence_in_ga is not None:
									fist_ep_ga = re.search('<b><a href="/wiki/(.+?)" title="(.+?)">GA</a>:</b>(.+?)<a href="/wiki/(.+?)" title="(.+?)">(.+?)</a>', content_sdf, re.S|re.DOTALL)
									
									first_episode_title_underscore = fist_ep_ga.group(4)
									first_episode_title_text = fist_ep_ga.group(5)

									ep_loop.append(first_episode_title_underscore)


									ep_url = 'http://greysanatomy.wikia.com/' + first_episode_title_underscore
									get_ep_page = urllib.urlopen(ep_url).read()
									get_ep_season_nums = re.search('<tr>(.+?)<td class="pi-horizontal-group-item pi-data-value pi-font pi-border-color pi-item-spacing">Season (.+?)</td>(.+?)<td class="pi-horizontal-group-item pi-data-value pi-font pi-border-color pi-item-spacing">Episode (.+?)</td>(.+?)</tr>', get_ep_page, re.S|re.DOTALL)
										
									if get_ep_season_nums.group(0) is not None:
										get_season_number = get_ep_season_nums.group(2)
										get_ep_number = get_ep_season_nums.group(4)

									code_season_number_episode_number = 'S-' + get_season_number + '-EP-' + get_ep_number
									season_episode_code.append(code_season_number_episode_number)



							else:
								get_h3_title_text = re.search('<a href="/wiki/(.+?)" title="(.+?)">(.+?)</a>', content_sdf, re.S|re.DOTALL)
								if get_h3_title_text is not None:
									first_episode_title_underscore = get_h3_title_text.group(1)
									first_episode_title_text = get_h3_title_text.group(2)
									ep_loop.append(first_episode_title_underscore)
						# ---------------------------------------------------------------------------------------------------------------------------------------------
						# Last
						# ---------------------------------------------------------------------------------------------------------------------------------------------
						if title_sdf == "Last":
							
							last_appearence_in_pp = re.search('<li><b><a href="/wiki/Private_Practice" title="Private Practice">PP</a>:</b> <a href="/wiki/(.+?)" title="(.+?)">(.+?)</a></li>', content_sdf, re.S|re.DOTALL)

							if last_appearence_in_pp is not None:
								pass

							last_appearence_in_ga = re.search('<b><a href="/wiki/Grey%27s_Anatomy" title="Grey\'s Anatomy">GA</a>:</b>', content_sdf, re.S|re.DOTALL)

							if last_appearence_in_ga is not None:
								single_or_multiple_episodes = "multiple"
								
								last_ep = re.search('<b><a href="/wiki/(.+?)" title="(.+?)">GA</a>:</b>(.+?)<a href="/wiki/(.+?)" title="(.+?)">(.+?)</a>', content_sdf, re.S|re.DOTALL)
								
								last_episode_title_underscore = last_ep.group(4)
								last_episode_title_text = last_ep.group(5)
								ep_loop.append(last_episode_title_underscore)

								ep_url = 'http://greysanatomy.wikia.com/' + last_episode_title_underscore
								get_ep_page = urllib.urlopen(ep_url).read()
								
								get_ep_season_nums = re.search('<tr>(.+?)<td class="pi-horizontal-group-item pi-data-value pi-font pi-border-color pi-item-spacing">Season (.+?)</td>(.+?)<td class="pi-horizontal-group-item pi-data-value pi-font pi-border-color pi-item-spacing">Episode (.+?)</td>(.+?)</tr>', get_ep_page, re.S|re.DOTALL)
										
								if get_ep_season_nums.group(0) is not None:
									get_season_number = get_ep_season_nums.group(2)
									get_ep_number = get_ep_season_nums.group(4)

								code_season_number_episode_number = 'S-' + get_season_number + '-EP-' + get_ep_number
								season_episode_code.append(code_season_number_episode_number)

							else:
								single_or_multiple_episodes = "multiple"
								get_h3_title_text = re.search('<a href="/wiki/(.+?)" title="(.+?)">(.+?)</a>', content_sdf, re.S|re.DOTALL)

								last_episode_title_underscore = get_h3_title_text.group(1)
								last_episode_title_text = get_h3_title_text.group(2)

								# print 'first episode title underscore', last_episode_title_underscore
								ep_loop.append(last_episode_title_underscore)


								ep_url = 'http://greysanatomy.wikia.com/' + last_episode_title_underscore
								get_ep_page = urllib.urlopen(ep_url).read()
								get_ep_season_nums = re.search('<tr>(.+?)<td class="pi-horizontal-group-item pi-data-value pi-font pi-border-color pi-item-spacing">Season (.+?)</td>(.+?)<td class="pi-horizontal-group-item pi-data-value pi-font pi-border-color pi-item-spacing">Episode (.+?)</td>(.+?)</tr>', get_ep_page, re.S|re.DOTALL)
										
								if get_ep_season_nums.group(0) is not None:
									get_season_number = get_ep_season_nums.group(2)
									get_ep_number = get_ep_season_nums.group(4)

								code_season_number_episode_number = 'S-' + get_season_number + '-EP-' + get_ep_number
								season_episode_code.append(code_season_number_episode_number)

						# ---------------------------------------------------------------------------------------------------------------------------------------------
						# Seasons
						# ---------------------------------------------------------------------------------------------------------------------------------------------
						if title_sdf == "Seasons":
							seasons_on_pp = re.search('<li><b><a href="/wiki/Private_Practice" title="Private Practice">PP</a>:</b> <a href="/wiki/(.+?)" title="(.+?)">(.+?)</a></li>', content_sdf, re.S|re.DOTALL)
							if seasons_on_pp is not None:
								pass

							# ---------------------------------------------------------------------------------------------------------------------------------------------
							seasons_on_ga = re.search('<b><a href="/wiki/Grey%27s_Anatomy" title="Grey\'s Anatomy">GA</a>:</b>(.+?)', content_sdf, re.S|re.DOTALL)
							if seasons_on_ga is not None:
								
								get_appearances_content = re.finditer('<a href="/wiki/Season_(.+?)" title="Season (.+?)">(.+?)</a>', content_sdf, re.S|re.DOTALL)
								for single_season in get_appearances_content:
									single_season = single_season.group(3)
									if single_season not in seasons_array:
										seasons_array.append(single_season)

						# -----------------------------------------------------------------------------
					
				else: 
					single_or_multiple_episodes = "No information available"
				# -----------------------------------------------------------------------------
				

				# -----------------------------------------------------------------------------
				# Character's diagnosis -- variable 3
				# -----------------------------------------------------------------------------
				get_medical_information = re.search('<section class="pi-item pi-group pi-border-color"><h2 class="pi-item pi-header pi-secondary-font pi-item-spacing pi-secondary-background">Medical Information</h2>(.+?)</section>', get_aside, re.S|re.DOTALL)

				if get_medical_information is not None:
					
					get_treatment = re.search('<div class="pi-item pi-data pi-item-spacing pi-border-color">(.+?)<h3 class="pi-data-label pi-secondary-font">Treatment</h3>(.+?)<div class="pi-data-value pi-font">(.+?)</div>(.+?)</div>', get_medical_information.group(1), re.S|re.DOTALL)
					
					if get_treatment is not None:
						get_treatment = get_treatment.group(3)
						check_single_or_multiple_treatment = re.search('<ul><li>(.+?)</li></ul>', get_treatment, re.S|re.DOTALL)
						
						if check_single_or_multiple_treatment is not None:
							split_treatment_on_list_item = check_single_or_multiple_treatment.group(1).split('</li><li>')
							treatment = split_treatment_on_list_item
						else:
							treatment = [get_treatment]
					else: 
						get_treatment = ["No treatment available."]

					# -----------------------------------------------------------------------------
					# Multiple diagnosis -- 
					get_diagnosis = re.search('<div class="pi-item pi-data pi-item-spacing pi-border-color">(.+?)<h3 class="pi-data-label pi-secondary-font">Diagnosis</h3>(.+?)<div class="pi-data-value pi-font">(.+?)</div>(.+?)</div>', get_medical_information.group(1), re.S|re.DOTALL)
					
					if get_diagnosis is not None:
						# cause_of_death = "Has diagnosis"
						get_diagnosis = get_diagnosis.group(3)
						check_for_single_multiple = re.search('<ul><li>(.+?)</li></ul>', get_diagnosis, re.S|re.DOTALL)
						
						if check_for_single_multiple is not None:
							split_diagnosis_on_list_item = check_for_single_multiple.group(1).split('</li><li>')
							diagnosis = split_diagnosis_on_list_item
						# Single diagnosis --
						else:
							diagnosis = [get_diagnosis]

				# -----------------------------------------------------------------------------
				# Really painful way to ensure every character has content in the cause of death column. 
				# To be edited by hand later.
				# -----------------------------------------------------------------------------
				get_main_content = re.search('<article id="WikiaMainContent" class="WikiaMainContent">(.+?)</article>', url_page, re.S|re.DOTALL)
				get_main_content = get_main_content.group(0)
				for every_h3 in re.finditer('<h3><span class="mw-headline" id="(.+?)">(.+?)</span><span class="editsection">(.+?)</span></h3>', get_main_content, re.S|re.DOTALL):
					
					h3_text = every_h3.group(2)
					h3_id = every_h3.group(1)

					if "Death" in h3_text: 

						get_section_para = re.search('<h3><span class="mw-headline" id="' + h3_id + '">' + every_h3.group(2) + '</span><span class="editsection">(.+?)</span></h3>(.+?)</p>(.+?)</p>', get_main_content, re.S|re.DOTALL)
						cause_of_death = [get_section_para.group(0)]
					# else: 
					# 	cause_of_death = h3_text
						# print 'h3_text', h3_text
					
				# else:
				# 	get_body_content = re.search('<article id="WikiaMainContent" class="WikiaMainContent">(.+?)</article>', url_page, re.S|re.DOTALL)
					
				# 	if get_body_content is not None:
				# 		get_body_content = get_body_content.group(0)
				# 		find_h3_with_death = re.finditer('<h3><span class="mw-headline" id="(.+?)">(.+?)</span>(.+?)</h3>', get_body_content, re.S|re.DOTALL)
				# 		for single_h3 in find_h3_with_death:
				# 			if single_h3 is not None:
				# 				print 'find_h3_with_death', single_h3.group(0)

				# 			<h3><span class="mw-headline" id="(.+?)">(.+?)</span><span class="editsection">(.+?)</h3>

				if len(diagnosis) == 0:
					diagnosis = ["No diagnosis available"]
				
				if len(treatment) == 0:
					treatment = ["No treatment available"]
				# -----------------------------------------------------------------------------

				# -----------------------------------------------------------------------------
				# ***Last step***  Write the rows for each variable
				# -----------------------------------------------------------------------------
				character_data = [counter, character_name, image, character_type, diagnosis, cause_of_death, treatment, actor, single_or_multiple_episodes, season_episode_code, first_episode_title_underscore, first_episode_title_text, last_episode_title_underscore, last_episode_title_text, seasons_array]
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
		if get_character_names.group(1) != 'Lillie_Jordan' and get_character_names.group(1) != 'Bizzy_Forbes' and get_character_names.group(1) != 'Timothy_Robbins' and get_character_names.group(1) != 'Susan_Grant' and get_character_names.group(1) != 'David_Gibbs' and get_character_names.group(1) != 'Frances_Wilder' and get_character_names.group(1) != 'Dell_Parker' and get_character_names.group(1) != 'Anna_Wilder' and get_character_names.group(1) != 'Baby_Shepherd' and get_character_names.group(1) != 'Pete_Wilder':
		# if get_character_names.group(1) != 'Nonesense!!!!!!!':
			
			url = 'http://greysanatomy.wikia.com/wiki/' + get_character_names.group(1)
			url_array.append(url)
			character = get_character_names.group(3)

			CharacterNameAndURL.writerow([character, url])

	scrape_character_pages(url_array)

# URLs to access
base_url = 'http://greysanatomy.wikia.com/wiki/Category:Deceased_Characters'
full_url = base_url

html_page = urllib.urlopen(base_url).read() # .urlopen() takes one value, the URL to open # .read() as a method to read returns
scrape_page(html_page)