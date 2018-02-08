
let dataHelpers = {}


let makePie = (data, title, val) => {
    let chart = d3.select('#gender-chart'),
        width = +chart.attr('width'), 
        height = +chart.attr('height'), 
        radius = Math.min(width, height) / 2
        g = chart.append("g").attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");
    
    let color = d3.scaleOrdinal(["#bada55", "#da467d"])                

    let pie = d3.pie()
                .sort(null)
                .value((d) => {
                    return d[val]
                })
    let path = d3.arc()
        .outerRadius(radius - 10)
        .innerRadius(0);    
    let label = d3.arc()
        .outerRadius(radius - 40)
        .innerRadius(radius - 40);            

    let arc = g.selectAll(".arc")
            .data(pie(data))
            .enter().append("g")
                .attr("class", "arc")

    arc.append("path")
        .attr("d", path)
        .attr("fill", function(d) {return color(d.data[title]) });            
    
    arc.append("text")
        .attr("transform", function(d) { return "translate(" + label.centroid(d) + ")"; })
        .attr("dy", "0.35em")
        .text(function(d) { return d.data[title]; });
    
}

makeLineGraph = (data) => {
    // set the dimensions and margins of the graph
    var margin = {top: 20, right: 20, bottom: 100, left: 100},
        width = 960 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;

    // parse the date / time
    var parseTime = d3.timeParse("%d-%b-%y");

    // set the ranges
    var x = d3.scaleLinear().range([0, width]);
    var y = d3.scaleLinear().range([height, 0]);

    // define the line
    var valueline = d3.line()
        .x(function(d) { return x(d.season); })
        .y(function(d) { return y(d.season_death_total); });

    // append the svg obgect to the body of the page
    // appends a 'group' element to 'svg'
    // moves the 'group' element to the top left margin
    var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");


    x.domain(d3.extent(data, function(d) { return d.season; }));  
    y.domain([0, d3.max(data, function(d) { return d.season_death_total; })]);    
    svg.append("path")
      .data([data])
      .attr("class", "line")
      .attr("d", valueline);

    // Add the X Axis
    svg.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));
    // text label for the x axis
    svg.append("text")             
        .attr("transform",
            "translate(" + (width/2) + " ," + 
                            (height + margin.top + 20) + ")")
        .style("text-anchor", "middle")
        .text("Season");  

    // Add the Y Axis
    svg.append("g")
      .call(d3.axisLeft(y));
    // text label for the y axis
    svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 30 - margin.left)
        .attr("x",0 - (height / 2))
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .text("Number of deaths");   


   

}



let numbersByGender = (data) => {
    let gender = {
        male: 0, 
        female: 0
    }
    let gender_obj = []
    data.forEach((el, i) => {
        if(el.character_gender == 'male' || el.character_gender == 'female'){
            gender[el.character_gender] = gender[el.character_gender] + 1
        }
    })
   for(item in gender){
       obj = {
           gender_name: item, 
           gender_count: gender[item]
       }
       gender_obj.push(obj)
   }
    return gender_obj
}


dataHelpers.getDeathSeasons = (data) => {
    let seasons = data.map((el, i) => {
        if(el.season_episode_code){
            return dataHelpers.getDeathSeason(el.season_episode_code)
        }else {
            return 'no_season'
        }
    })
    return seasons
}

dataHelpers.getDeathSeason = (item) => {
    if(item) {
        let death_season = item.split('S-')[1]
        death_season ? death_season = death_season.split('-')[0] : death_season = 'no_season'
        return death_season
    }
}
 


let deathsBySeason = (data) => {
    let totals_by_season = {}
    let deaths_by_season_formatted = []
   
    let seasons = dataHelpers.getDeathSeasons(data)
    console.log(seasons)
    seasons.forEach((el, i) => {
        totals_by_season[el] ? totals_by_season[el] = totals_by_season[el] + 1 : totals_by_season[el] = 1
    })
    for(season in totals_by_season) {
        obj = {
            season: season, 
            season_death_total: totals_by_season[season]
        }
        season !=  "no_season" ? deaths_by_season_formatted.push(obj) : null
    }
    return deaths_by_season_formatted
}


let deathsByCharacterStatus = (data) => {
    let data_arr = [
        {
            character_status: 'major', 
            death_total: 0
        }, 
        {
            character_status: 'minor', 
            death_total: 0
        }
    ]

    data.forEach((el, i) => {
        if(el.character_major_or_minor === 'major') {
            data_arr[0].death_total += 1
        }else if(el.character_major_or_minor === 'minor') {
            data_arr[1].death_total += 1 
        }else {
            return
        }
    })
    return data_arr
}

let deathsByCharacterStatusBySeason = (data) => {
    // get unique list of seasons
    let seasons = Array.from(new Set(dataHelpers.getDeathSeasons(data)));
    let death_by_season_and_status = []
    seasons.forEach((season, i) => {
        let data_obj = {
            season: season, 
            death_count_minor: 0,
            death_count_major: 0
        }
        data.forEach((obj, i) => {
            if (dataHelpers.getDeathSeason(obj.season_episode_code) == season) {
                if(obj.character_major_or_minor === 'major'){
                    data_obj.death_count_major +=1
                }else if(obj.character_major_or_minor === 'minor'){
                    data_obj.death_count_minor += 1
                }else {
                    return
                }
            }
        })
        death_by_season_and_status.push(data_obj)
    })
    return death_by_season_and_status
}




d3.csv("../csv/character_details/character-details.csv", (data) => {
    // console.log(data)
    console.log(deathsByCharacterStatus(data))
    console.log(deathsBySeason(data))
    console.log(deathsByCharacterStatusBySeason(data))
    // makeLineGraph(deathsBySeason(data))
    // let gender_obj = numbersByGender(data)
    // makePie(gender_obj, 'gender_name', 'gender_count')
})




$(() => {
    // console.log('doc ready')
})