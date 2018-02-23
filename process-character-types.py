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
character_types_top_columns = ['title','category','total_deaths']
character_types_filename = 'character-type-analysis.csv'

data_analysis_directory = '/Users/jessiewillms/Dropbox/shonda-greys-db/shondaland-dead-bodies/csv/data_analysis/'
# data_analysis_directory = '/Users/cbcwebdev02/Dropbox/2018/2018-01-04-intro-to-python/csv/data_analysis/'

CharacterTypeAnalysis = csv.writer(file(data_analysis_directory + character_types_filename, 'w'),dialect='excel')
CharacterTypeAnalysis.writerow(character_types_top_columns)

# ------------------------------------------------------------------------------------------------------------------- 
# Get the data + process it
# ------------------------------------------------------------------------------------------------------------------- 
get_data = open('/Users/jessiewillms/Dropbox/shonda-greys-db/shondaland-dead-bodies/csv/character_details/character-details.csv')
reader = csv.reader(get_data)

# 1. Total of the type of patient who dies
patient_type = []

for row in reader:
	# Now, count the types of patients
	if row[5] != "character_type":
		patient_type.append(row[5])

# Use python to count the totals of each patient type
patient_types = Counter(patient_type)
for key, value in patient_types.items():
	# Output to CSV
	CharacterTypeAnalysis.writerow([key.title(), key, value])