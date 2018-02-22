
# import libraries 
import time # wait commands (space out)
import re # regular expressions (text parser)
import urllib # Internet connection (socket connections, https)
import csv
import json

date = time.time()

# -------------------------------------------------------------------------------------------------------------------
# Make the headers for each column
# -------------------------------------------------------------------------------------------------------------------
top_columns_character_details =  ['season', 'episode_number', 'episode_title', 'season_episode_code']


# filename = str(date) + 'episode-list.csv'
filename = 'episode-list.csv'
directory = '/Users/jessiewillms/Dropbox/shonda-greys-db/shondaland-dead-bodies/csv/episode_list/'

episode_json = '/Users/jessiewillms/Dropbox/shonda-greys-db/shondaland-dead-bodies/json/episode_list/episode-list.json'

episode_deatils = csv.writer(file(directory + filename, 'a'),dialect='excel')
episode_deatils.writerow(top_columns_character_details)

# -------------------------------------------------------------------------------------------------------------------
# Get list of every episode + make code 
# ------------------------------------------------------------------------------------------------------------------- 
def scrape_page():
	episodes = []

	# URLs to access
	base_url = 'http://greysanatomy.wikia.com/wiki/Grey%27s_Anatomy_Episodes'

	html_page = urllib.urlopen(base_url).read()

	for every_table in re.finditer('<h3><span class="mw-headline" id="(.+?)"><b>Season (.+?)</b>(.+?)</span>(.+?)</h3>(.+?)<table class="wikitable plainrowheaders" (.+?)>(.+?)</table>', html_page, re.S|re.DOTALL):
		season = every_table.group(2)

		for every_tr in re.finditer('<tr class="vevent" style="(.+?)">(.+?)</tr>', every_table.group(7), re.S|re.DOTALL):
			every_tr = every_tr.group(2)

			for row in re.finditer('<th id="(.+?)" scope="row">(.+?)</th><td>(.+?)</td><td class="summary" style="text-align:left;">(.+?)</td><td>(.+?)</td><td>(.+?)</td>', every_tr, re.S|re.DOTALL):
				
				gets_title = re.search('<a href="/wiki/(.+?)" title="(.+?)">(.+?)</a>', row.group(4), re.S|re.DOTALL)
				if gets_title is not None:
					ep_title = gets_title.group(2)
				else:
					ep_title = "Not available."

				ep_num = row.group(3)
				air_date = row.group(5)
				overall_number = row.group(2)

				season_episode_code = 'S-' + season + '-EP-' + ep_num

				data =  [season, ep_num, ep_title, season_episode_code]
				episode_deatils.writerow(data)

				episodes.append({'season': season, 'ep_num': ep_num, 'ep_title': ep_title, 'season_episode_code': season_episode_code})


	with open(episode_json, 'w') as outfile:
		json.dump(episodes, outfile)

scrape_page()










