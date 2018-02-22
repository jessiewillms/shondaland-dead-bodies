/*--------------------------------------------------------------------------------
Create the HTML for the gender charts*/ 
function create_gender_chart(json) {
	
	console.log(`make gender charts`);
	/*----------------------------------------------------------------------------
	Make gender charts (totals)
	----------------------------------------------------------------------------*/ 
	const male_total = json.male;
	const female_total = json.female;

	// console.log({female_total});
	const total = male_total + female_total;

	// console.log(total);
	const make_total_bars = `<div class="wrapper">
		<section class="bar-wrap">
		<div class="female bar" style="width:${female_total / total * 100}%;"><span class="label">${Math.round(female_total / total * 100)}% female</span></div>
		<div class="bar-tick"></div>
		<div class="male bar" style="width:${male_total / total * 100}%;"><span class="label">${Math.round(male_total / total * 100)}% male</span></div>
		</section>
	</div>`

	/*----------------------------------------------------------------------------
	Make gender charts (major characters)
	----------------------------------------------------------------------------*/ 
	const male_major_total = json.male_major;
	const female_major_total = json.female_major;

	const major_total = male_major_total + female_major_total;

	const make_major_bars = `<div class="wrapper">
		<section class="bar-wrap">
		<div class="female bar" style="width:${female_major_total / major_total * 100}%;"><span class="label">${Math.round(female_major_total / major_total * 100)}% female</span></div>
		<div class="bar-tick"></div>
		<div class="male bar" style="width:${male_major_total / major_total * 100}%;"><span class="label">${Math.round(male_major_total / major_total * 100)}% male</span></div>
		</section>
	</div>`

	/*----------------------------------------------------------------------------
	Make gender charts (minor characters)
	----------------------------------------------------------------------------*/ 
	const male_minor_total = json.male_minor;
	const female_minor_total = json.female_minor;

	const minor_total = male_minor_total + female_minor_total;

	const make_minor_bars = `<div class="wrapper">
		<section class="bar-wrap">
		<div class="female bar" style="width:${female_minor_total / minor_total * 100}%;"><span class="label">${Math.round(female_minor_total / minor_total * 100)}% female</span></div>
		<div class="bar-tick"></div>
		<div class="male bar" style="width:${male_minor_total / minor_total * 100}%;"><span class="label">${Math.round(male_minor_total / minor_total * 100)}% male</span></div>
		</section>
	</div>`

	// Call function to append the HTML into the chart div
	append_charts(make_total_bars, make_major_bars, make_minor_bars);
}

/*--------------------------------------------------------------------------------
Append the charts to the DOM*/ 
function append_charts(make_total_bars, make_major_bars, make_minor_bars) {
	// Make all the charts
	const get_all_chart = document.getElementById('js-gender-wrap--all');
	$(get_all_chart).html(make_total_bars);

	const get_major_chart = document.getElementById('js-gender-wrap--major');
	$(get_major_chart).html(make_major_bars);

	const get_minor_chart = document.getElementById('js-gender-wrap--minor');
	$(get_minor_chart).html(make_minor_bars);
}

function create_deaths_by_season_chart(characters) {
	
	const type = characters.map(single => `${single.character_type}`);

    const character_types = type.reduce(function(obj, item) {
      if (!obj[item]) {
        obj[item] = 0;
      }
      obj[item]++;
      return obj;
    }, {});

    const make_type_bars = Object.entries(character_types);
    let all_bars = [];
    make_type_bars.forEach(single => {
    	// console.log(single);
    	var single_bar = `<div class="character_type bar" style="width:${single[1]}%;"><span class="label">${single[0]}: ${single[1] }</span></div>`;
    	all_bars += single_bar;
    });
  
    const make_total_bars = `<div class="wrapper">
		<section class="bar-wrap">${all_bars}</section>
	</div>`;
	$('#js-all-types').append(make_total_bars);
}

/*--------------------------------------------------------------------------------
Get the data */ 
function get_data() {
	console.log('get data called');
	
	// Details CSV
	const character_details = '../json/character_details/character-details.json'
	const gender_details = '../json/data_analysis/gender-totals.json'
	
	// d3.json(gender_details, function(data) {
 //  		console.log(data);
	// });
	d3.queue()
  		.defer(d3.json, gender_details)
		.defer(d3.json, character_details)
		.await(analyze);

	function analyze(error, gender, characters) {
		if(error) { console.log(error); }

	 	create_gender_chart(gender);
	 	create_deaths_by_season_chart(characters);
	}
}

$(document).ready(function() {
	console.log( "ready!" );
	get_data();
});

