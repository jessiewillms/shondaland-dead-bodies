# import libraries 
import time # wait commands (space out)
import re # regular expressions (text parser)
import csv

# ------------------------------------------------------------------------------------------------------------------- 
# Set up for the CSV output
# ------------------------------------------------------------------------------------------------------------------- 
top_columns = ['female', 'male', 'unknown']
filename = 'data-analysis.csv'

# directory = '/Users/jessiewillms/Dropbox/shonda-greys-db/shondaland-dead-bodies/csv/data_analysis/'
directory = '/Users/cbcwebdev02/Dropbox/2018/2018-01-04-intro-to-python/csv/data_analysis/'

DataAnalysis = csv.writer(file(directory + filename, 'a'),dialect='excel')
DataAnalysis.writerow(top_columns)

# ------------------------------------------------------------------------------------------------------------------- 
# Get the data + process it
# ------------------------------------------------------------------------------------------------------------------- 
get_data = open('/Users/cbcwebdev02/Dropbox/2018/2018-01-04-intro-to-python/project/csv/character_details/character-details.csv')
reader = csv.reader(get_data)

# Gender counters
female = 0
male = 0
unknown = 0

female_major = 0
male_major = 0
unknown_major = 0

female_minor = 0
male_minor = 0
unknown_minor = 0

for row in reader:
	# Get gender breakdown
	print 'row', row

	gender = row[2]
	# major_minor = row[x]
	print row[9]
	
	if gender == "female":
		female = female + 1

		if major_minor == "major":
			female_major = female_major + 1
		else:
			female_minor = female_minor + 1

	elif gender == "male" or gender == "mostly_male":
		male = male + 2

		# Is it a major or minor male 
		if major_minor == "major":
			male_major = male_major + 1
		else:
			male_minor = male_minor + 1
	
	else:
		unknown = unknown + 1


# Print gender totals 
print 'female', female
print 'male', male
print 'unknown', unknown

DataAnalysis.writerow([female, male, unknown])