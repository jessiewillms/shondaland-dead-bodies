# import libraries 
import csv
import json

from collections import Counter

################################################################### 
# I split the processing of Grey's data into multiple, smaller
# files specific to each output to avoid confusion.
# TODO: See if you can use partials in Python? Or is this fine?
###################################################################

# ------------------------------------------------------------------------------------------------------------------- 
# Set up for the CSV output - to make the bubble chart of character types
# ------------------------------------------------------------------------------------------------------------------- 
character_types_top_columns = ['season','episode_number','episode_title','season_episode_code','has_death','who_died']
character_types_filename = 'episode-deaths.csv'

data_analysis_directory = '/Users/jessiewillms/Dropbox/shonda-greys-db/shondaland-dead-bodies/csv/data_analysis/'
# data_analysis_directory = '/Users/cbcwebdev02/Dropbox/2018/2018-01-04-intro-to-python/csv/data_analysis/'

CharacterTypeAnalysis = csv.writer(file(data_analysis_directory + character_types_filename, 'w'),dialect='excel')
CharacterTypeAnalysis.writerow(character_types_top_columns)

# ------------------------------------------------------------------------------------------------------------------- 
# Get the data + process it
# ------------------------------------------------------------------------------------------------------------------- 
get_ep_data = open('/Users/jessiewillms/Dropbox/shonda-greys-db/shondaland-dead-bodies/csv/episode_list/episode-list.csv')
reader = csv.reader(get_ep_data)

data = []
count = 0
# Re-write one CSV to another? This is dumb??????
for row in reader:
	if count == 0:
		pass
	else:
		season = row[0]
		episode_number = row[1]
		episode_title = row[2]
		season_episode_code = row[3]
		has_death = ''
		who_died = ''

		# Output to CSV
		CharacterTypeAnalysis.writerow([season,episode_number,episode_title,season_episode_code,has_death,who_died])

	count = count + 1

# ------------------------------------------------------------------------------------------------------------------- 
# Get the details data + process it
# ------------------------------------------------------------------------------------------------------------------- 
get_details_data = open('/Users/jessiewillms/Dropbox/shonda-greys-db/shondaland-dead-bodies/csv/character_details/character-details.csv')
details_reader = csv.reader(get_details_data)

for row in details_reader:
	if row[11] != 'season_episode_code':
		episodes_list = row[11].split()[-1].replace("[", "").replace("'", "").replace("]", "")
		print episodes_list
		CharacterTypeAnalysis.writerow(episodes_list)

