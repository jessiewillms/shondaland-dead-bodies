# import libraries 
import time # wait commands (space out)
import re # regular expressions (text parser)
import csv
import json

# ------------------------------------------------------------------------------------------------------------------- 
# Set up for the CSV output
# ------------------------------------------------------------------------------------------------------------------- 
top_columns = ['female', 'male', 'female_major', 'male_major', 'female_minor', 'male_minor']
filename = 'data-analysis.csv'

directory = '/Users/jessiewillms/Dropbox/shonda-greys-db/shondaland-dead-bodies/csv/data_analysis/'
# directory = '/Users/cbcwebdev02/Dropbox/2018/2018-01-04-intro-to-python/csv/data_analysis/'

DataAnalysis = csv.writer(file(directory + filename, 'w'),dialect='excel')
DataAnalysis.writerow(top_columns)

# ------------------------------------------------------------------------------------------------------------------- 
# Get the data + process it
# CBC computer: get_data = open('/Users/cbcwebdev02/Dropbox/2018/2018-01-04-intro-to-python/project/csv/character_details/character-details.csv')
# ------------------------------------------------------------------------------------------------------------------- 
get_data = open('/Users/jessiewillms/Dropbox/shonda-greys-db/shondaland-dead-bodies/csv/character_details/character-details.csv')
reader = csv.reader(get_data)


analysis_json = '/Users/jessiewillms/Dropbox/shonda-greys-db/shondaland-dead-bodies/json/data_analysis/gender-totals.json'
episode_json = '/Users/jessiewillms/Dropbox/shonda-greys-db/shondaland-dead-bodies/json/data_analysis/episode-chart.json'

# -------------------------------------------------------------------------------------------------
# EPISODE COUNTS 
# -------------------------------------------------------------------------------------------------
# episode_breakdown = []

# count = 0
# for row in reader:
# 	# Get episode breakdown
# 	if count < 10:
# 		if row[11] is not None:
# 			code = row[11]
# 			episode_breakdown.append({'ep_season_code': code})
# 		count = count + 1

# with open(episode_json, 'w') as outfile:
# 	json.dump(episode_breakdown, outfile)



# ------------------------------------------------------------------------------------------------------------------- 
# GENDER COUNTS -----------------------------------------------------------------------------------------
# 
# 1. Gender breakdown of deaths
# 2. Gender breakdown of *major* deaths vs. gender breakdown of *minor* deaths
# 3. Gender deaths by season
# 
# ------------------------------------------------------------------------------------------------------------------- 
gender_breakdown = []

# 1. Gender breakdown of deaths
female = 0
male = 0
unknown = 0 # one of these "dead characters" is a skelton

# 2. Gender breakdown of *major* deaths vs. gender breakdown of *minor* deaths
female_major = 0
male_major = 0
unknown_major = 0

female_minor = 0
male_minor = 0
unknown_minor = 0

makeJSONObj = {}
for row in reader:
	
	print '-------------------------------------'
	# print row
	# print name, 'is a', major_minor, 'character.'
	# print '-------------------------------------'

	# Get gender breakdown
	name = row[1]

	gender = row[2]
	# print gender
	major_minor = row[3]
 
	if gender == "female":
		female += 1
		
		# 2. Gender breakdown + major/minor breakdown
		if major_minor == "major":
			female_major += 1
		else:
			female_minor += 1

	elif gender == "male":
		male = male + 2

		# 2. Gender breakdown + major/minor breakdown
		if major_minor == "major":
			male_major += 1
		else:
			male_minor += 1

	else:
		unknown = unknown + 1


# Print gender totals 
# print 'female', female_major
# print 'male', male_major

DataAnalysis.writerow([female, male, female_major, male_major, female_minor, male_minor])
# DataAnalysis.writerow([female, male, unknown])



gender_totals_json = {'female': female, 'male': male, 'female_major': female_major, 'male_major': male_major,'female_minor': female_minor, 'male_minor': male_minor}
gender_breakdown.append(gender_totals_json)


with open(analysis_json, 'w') as outfile:
	json.dump(gender_totals_json, outfile)
