import pymysql
import json
 
hostname = '104.196.57.15'
username = 'canopyapi'
password = 'CBCn3w51nt3r!'
database = 'canopy'


# Empty object to populate 
character_data = {}
character_name_to_get = "Reed Adamson"
character_diagnosis_to_get = "['Gunshot wound']"

# Do the query function 
def get_all_characters( my_connection ):
	
	cursor = my_connection.cursor() # a little cursor that navigates the DB for you

	cursor.execute("SELECT character_name, character_gender, character_major_or_minor, image, character_type, diagnosis, treatment, actor, single_or_multiple_episodes, season_episode_code, first_episode_title_underscore, first_episode_title_text, last_episode_title_underscore, last_episode_title_text, seasons_array FROM character_details")

	results = cursor.fetchall()

	# if single not in character_data:
	for single_row in results:
		# All characters being returns 
		character_data[single_row[0]] = {
			'name':single_row[0],
			'gender':single_row[1],
			'major_minor':single_row[2],
			'image':single_row[3],
			'character_type':single_row[4],
			'diagnosis':single_row[5],
			'treatment':single_row[6],
			'portrayed_by':single_row[7],
			'single_or_multiple_episodes':single_row[8],
			'season_episode_code':single_row[9],
			'first_ep_title_underscore':single_row[10],
			'first_ep_title':single_row[11],
			'last_ep_title_underscore':single_row[12],
			'last_ep_title':single_row[13],
			'seasons':single_row[14]
		}
	# print character_data

# Do single query
def get_single_character( my_connection ):
	
	cursor = my_connection.cursor() # a little cursor that navigates the DB for you

	cursor.execute("SELECT character_name, character_gender, character_major_or_minor, image, character_type, diagnosis, treatment, actor, single_or_multiple_episodes, season_episode_code, first_episode_title_underscore, first_episode_title_text, last_episode_title_underscore, last_episode_title_text, seasons_array FROM character_details WHERE character_name = '" + character_name_to_get + "' ")

	results = cursor.fetchall()

	character_data[results[0]] = {
		'name':results[0][0],
		'gender':results[0][1],
		'major_minor':results[0][2],
		'image':results[0][3],
		'character_type':results[0][4],
		'diagnosis':results[0][5],
		'treatment':results[0][6],
		'portrayed_by':results[0][7],
		'single_or_multiple_episodes':results[0][8],
		'season_episode_code':results[0][9],
		'first_ep_title_underscore':results[0][10],
		'first_ep_title':results[0][11],
		'last_ep_title_underscore':results[0][12],
		'last_ep_title':results[0][13],
		'seasons':results[0][14]
	}
	# print character_data

# Do single query
# def get_diagnosis( my_connection ):
	
# 	cursor = my_connection.cursor() # a little cursor that navigates the DB for you

# 	cursor.execute("SELECT character_name, character_gender, character_major_or_minor, image, character_type, diagnosis, treatment, actor, single_or_multiple_episodes, season_episode_code, first_episode_title_underscore, first_episode_title_text, last_episode_title_underscore, last_episode_title_text, seasons_array FROM character_details WHERE `['Infection']` IN diagnosis ")

# 	results = cursor.fetchall()

# 	character_data[results[0]] = {
# 		'name':results[0][0],
# 		'gender':results[0][1],
# 		'major_minor':results[0][2],
# 		'image':results[0][3],
# 		'character_type':results[0][4],
# 		'diagnosis':results[0][5],
# 		'treatment':results[0][6],
# 		'portrayed_by':results[0][7],
# 		'single_or_multiple_episodes':results[0][8],
# 		'season_episode_code':results[0][9],
# 		'first_ep_title_underscore':results[0][10],
# 		'first_ep_title':results[0][11],
# 		'last_ep_title_underscore':results[0][12],
# 		'last_ep_title':results[0][13],
# 		'seasons':results[0][14]
# 	}
# 	print character_data

my_connection = pymysql.connect( host=hostname, user=username, passwd=password, db=database)

get_all_characters( my_connection ) # call a function -- whatever you want to do with the DB 
get_single_character( my_connection ) # call a function -- whatever you want to do with the DB 
# get_diagnosis( my_connection ) # call a function -- whatever you want to do with the DB 
# get_episodes( my_connection ) # call a function -- whatever you want to do with the DB 
my_connection.close() # close the connection to th DB 



# Python library FLASK for routing 

