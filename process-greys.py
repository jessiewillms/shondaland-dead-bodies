# import libraries 
import time # wait commands (space out)
import re # regular expressions (text parser)
import csv

# ------------------------------------------------------------------------------------------------------------------- 
# Set up for the CSV output
# ------------------------------------------------------------------------------------------------------------------- 
top_columns = ['female_total', 'male_total', 'unknown', 'female_major_minor', 'male_major_minor']
filename = 'data-analysis.csv'

directory = '/Users/jessiewillms/Dropbox/shonda-greys-db/shondaland-dead-bodies/csv/data_analysis/'
# directory = '/Users/cbcwebdev02/Dropbox/2018/2018-01-04-intro-to-python/csv/data_analysis/'

DataAnalysis = csv.writer(file(directory + filename, 'a'),dialect='excel')
DataAnalysis.writerow(top_columns)

# ------------------------------------------------------------------------------------------------------------------- 
# Get the data + process it
# CBC computer: get_data = open('/Users/cbcwebdev02/Dropbox/2018/2018-01-04-intro-to-python/project/csv/character_details/character-details.csv')
# ------------------------------------------------------------------------------------------------------------------- 
get_data = open('/Users/jessiewillms/Dropbox/shonda-greys-db/shondaland-dead-bodies/project/csv/character_details/character-details.csv')
reader = csv.reader(get_data)

# ------------------------------------------------------------------------------------------------------------------- 
# GENDER COUNTS -----------------------------------------------------------------------------------------
# 
# 1. Gender breakdown of deaths
# 2. Gender breakdown of *major* deaths vs. gender breakdown of *minor* deaths
# 3. Gender deaths by season
# 
# ------------------------------------------------------------------------------------------------------------------- 


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
	# Get gender breakdown
	name = row[1]

	# print 'name', 

	gender = row[2]
	# print gender
	major_minor = row[3]
 
	if gender == "female":
		female += 1

		print '-------------------------------------'
		print row
		print name, 'is a', major_minor, 'character.'
		print '-------------------------------------'
		
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
print 'female', female_major
print 'male', male_major

DataAnalysis.writerow([female, male, unknown])
DataAnalysis.writerow([female, male, unknown])