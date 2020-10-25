// enter code to define margin and dimensions for svg
var m = {left: 10, right: 10, top: 10, bottom: 10};
var w = 1200 - m.left - m.right;
var h = 600 - m.top - m.bottom;

// enter code to create svg
var svg = d3.select("#choropleth")
.append("svg")
.attr("width", w + m.left + m.right)
.attr("height", h + m.top + m.bottom)
.append("g")
.attr("transform", "translate(" + m.left + "," + m.top + ")");

// enter code to create color scale
var color = d3.scaleQuantile().range(d3.schemeBlues[4])

// enter code to define tooltip
var tip = d3.tip()
    .attr("class", "d3-tip")
    .html(function(d) { return "County: " + d.properties.NAME + "</br>Game: " + d.Game + "</br>Avg Rating: " + d.average_rating + "</br>Number of Users: " + d.number_of_users; })
    .offset([50,0])

// enter code to define projection and path required for Choropleth
var projection = d3.geoMercator()
        .scale(5650)
        .center([-85, 42.85])
        .rotate([-10, 0])
        .translate([w/2, h/2])

var path = d3.geoPath().projection(projection)

    
// define any other global variables 

Promise.all([
    // enter code to read files
    d3.json('NY-36-new-york-counties.json'),
    d3.dsv(",", "ratings-by-country.csv", function(d) {
        return {
            Game: d.Game,
            Country: d.Country,
            number_of_users: +d["Number of Users"],
            average_rating: +d["Average Rating"]
        } 
    })
]).then(function (data, error) {
    // enter code to call ready() with required arguments
    ready(error, data[0], data[1])
    }
);

// this function should be called once the data from files have been read
// world: topojson from world_countries.json
// gameData: data from ratings-by-country.csv

function ready(error, ny, gameData) {


var game = []


    
   
    
    // create Choropleth with default option. Call createMapAndLegend() with required arguments. 
    createMapAndLegend(ny, gameData, game[0])
}

// this function should create a Choropleth and legend 
function createMapAndLegend(ny, gameData, selectedGame){ 
    svg.selectAll(".new-york").remove()
    
    var data =[]
    gameData.forEach(function(d) {
        if (d.Game == selectedGame) {
            data.push(d)
        }
    })

    color.domain([0,100])
    
    svg.append("g")
        .attr("class", "countries")
        .selectAll("path")
        .data(topojson.feature(ny, ny.objects.cb_2015_new_york_county_20m).features)
        .enter()
        .append("path")
        .attr("d", path)
        .attr("fill", function(d) {
            console.log(d.properties.NAME)
            return color(Math.floor(Math.random() * Math.floor(100)))
         })
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide)

    svg.call(tip)

    svg.append("g")
        .attr("class", "legend")
        .attr("transform", "translate(900,20)");

    var legend = d3.legendColor()
        .labelFormat(d3.format(".2f"))
        .scale(color)

    svg.select(".legend")
        .call(legend)
    
}
