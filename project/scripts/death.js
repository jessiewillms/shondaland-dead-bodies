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

/*--------------------------------------------------------------------------------
Create a chart with all the types of patients */ 
function create_character_types_chart(characters, characters_csv) {
	
	const type = characters.map(single => `${single.character_type}`);

    const character_types = type.reduce(function(obj, item) {
      if (!obj[item]) {
        obj[item] = 0;
      }
      obj[item]++;
      return obj;
    }, {});

    console.log(character_types);
    console.table(character_types);
    // Old chart
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
Fun bubble chart */ 
function bubbleChart() {
    var width = 960,
        height = 960,
        maxRadius = 6,
        columnForColors = "category",
        columnForRadius = "views";

    function chart(selection) {
        var data = selection.enter().data();
        var div = selection,
            svg = div.selectAll('svg');
        svg.attr('width', width).attr('height', height);

        var tooltip = selection
            .append("div")
            .style("position", "absolute")
            .style("visibility", "hidden")
            .style("color", "white")
            .style("padding", "5px")
            .style("background-color", "#626D71")
            // .style("border-radius", "6px")
            .style("text-align", "left")
            .style("font-family", "sans-serif")
            .style("width", "200px")
            .text("");


        var simulation = d3.forceSimulation(data)
            .force("charge", d3.forceManyBody().strength([-50]))
            .force("x", d3.forceX())
            .force("y", d3.forceY())
            .on("tick", ticked);

        function ticked(e) {
            node.attr("cx", function(d) {
                    return d.x;
                })
                .attr("cy", function(d) {
                    return d.y;
                });
        }

        var colorCircles = d3.scaleOrdinal(d3.schemeCategory10);
        var scaleRadius = d3.scaleLinear().domain([d3.min(data, function(d) {
            return +d[columnForRadius];
        }), d3.max(data, function(d) {
            return +d[columnForRadius];
        })]).range([5, 18])

        var node = svg.selectAll("circle")
            .data(data)
            .enter()
            .append("circle")
            .attr('r', function(d) {
                return scaleRadius(d[columnForRadius])
            })
            .style("fill", function(d) {
                return colorCircles(d[columnForColors])
            })
            .attr('transform', 'translate(' + [width / 2, height / 2] + ')')
            .on("mouseover", function(d) {
                tooltip.html(d.title + "<br>" + d[columnForRadius] + " deaths");
                return tooltip.style("visibility", "visible");
            })
            .on("mousemove", function() {
                return tooltip.style("top", (d3.event.pageY - 10) + "px").style("left", (d3.event.pageX + 10) + "px");
            })
            .on("mouseout", function() {
                return tooltip.style("visibility", "hidden");
            });
    }

    chart.width = function(value) {
        if (!arguments.length) {
            return width;
        }
        width = value;
        return chart;
    };

    chart.height = function(value) {
        if (!arguments.length) {
            return height;
        }
        height = value;
        return chart;
    };


    chart.columnForColors = function(value) {
        if (!arguments.columnForColors) {
            return columnForColors;
        }
        columnForColors = value;
        return chart;
    };

    chart.columnForRadius = function(value) {
        if (!arguments.columnForRadius) {
            return columnForRadius;
        }
        columnForRadius = value;
        return chart;
    };

    return chart;
}




/*--------------------------------------------------------------------------------
Get the data */ 
function get_data() {
	console.log('get data called');
	
	// Details CSV
	const character_details = '../json/character_details/character-details.json'
	const character_details_csv = '../csv/character_details/character-details.csv'

	// /Users/jessiewillms/Dropbox/shonda-greys-db/shondaland-dead-bodies/project/csv/character_details/character-details.csv
	const gender_details = '../json/data_analysis/gender-totals.json'
	
	// d3.json(gender_details, function(data) {
 //  		console.log(data);
	// });
	d3.queue()
  		.defer(d3.json, gender_details)
		.defer(d3.json, character_details)
		// .defer(d3.csv, character_details_csv)
		.await(analyze);

	function analyze(error, gender, characters, characters_csv) {
		if(error) { console.log(error); }

	 	create_gender_chart(gender);
	 	create_character_types_chart(characters, character_details_csv);
	}
}

$(document).ready(function() {
	console.log( "ready!" );
	get_data();
});

