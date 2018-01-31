// Work with the data
const make_gender_charts = function(details_data) {
	console.log(details_data);

	
}

// Work with the data
// const process_details = function(details_data) {
// 	console.log(details_data);
// }

/* ---------------------------------------------------
Work with the data now
--------------------------------------------------- */
const process_episodes = function(episode_data) {
	console.log(episode_data);

	const ep_calendar = [];
	for (var i = 0; i < episode_data.length; i++) {
		
		ep_calendar.push(`<li data-lol="⚰" data-ep-num=${episode_data[i].episode_number} data-code=${episode_data[i].season_episode_code}></li>`)
		
		// if (episode_data[i].episode_number) {
		// }
	}

	$('#js_ep_calendar').html(ep_calendar);
}

// Get the data + process it with PapaParse
const get_data = function(){

	// const episodes_url = '1517179472.31episode-list.csv';
	// Papa.parse(episodes_url, {
	// 	download: true,
	// 	header: true,
	// 	// rest of config ...
		
	// 	// when this is complete, send data to process function
	// 	complete: function(results, file) {
	// 		// console.log("Parsing complete:", results, file);
	// 		episode_data = results.data;
	// 		process_episodes(episode_data);
	// 	}
	// });


	// Details CSV
	const details_url = '/csv/data_analysis/data-analysis.csv'
	console.log(`details_url`, details_url);
	Papa.parse(details_url, {
		download: true,
		header: true,
		skipEmptyLines: true,
		// rest of config ...
		
		// when this is complete, send data to process function
		complete: function(results, file) {
			// console.log("Parsing complete:", results, file);
			details_data = results.data;
			// process_details(details_data);
			make_gender_charts(details_data[0]);
		}
	});
}

$(document).ready(function() {
	get_data();
	// console.log( "ready!" );
});