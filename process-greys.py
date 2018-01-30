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
get_data = open('/Users/cbcwebdev02/Dropbox/2018/2018-01-04-intro-to-python/csv/character_details/1517269996.48character-details.csv')
reader = csv.reader(get_data)

# Gender counters
female = 0
male = 0
unknown = 0

for row in reader:
	# Get gender breakdown
	gender = row[2]
	# print gender
	
	if gender == "female" or gender == "mostly_female":
		female = female + 1
	elif gender == "male" or gender == "mostly_male":
		male = male + 2
	else:
		unknown = unknown + 1


# Print gender totals 
print 'female', female
print 'male', male
print 'unknown', unknown

DataAnalysis.writerow([female, male, unknown])


