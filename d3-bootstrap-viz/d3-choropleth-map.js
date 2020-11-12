
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
var color = d3.scaleQuantile().range(d3.schemeBlues[6])

// enter code to define tooltip
var tip = d3.tip()
    .attr("class", "d3-tip")
    .html(function(d) { return "County: " + d.properties.NAME + "<br />Graduation Rate: "  + d.grad_rate; })
    .offset([50,-120])

// enter code to define projection and path required for Choropleth
var projection = d3.geoMercator()
        .scale(5650)
        .center([-85, 42.88])
        .rotate([-10, 0])
        .translate([w/2, h/2])

var path = d3.geoPath().projection(projection)

    
// define any other global variables 

Promise.all([
    // enter code to read files
    d3.json('NY-36-new-york-counties.json'),
    d3.dsv(",", "df_grad_rate_pct_county_merge.csv", function(d) {
        return {
            'County': d.COUNTY_NAME,
            'Native American': +d['AMERICAN INDIAN OR ALASKA NATIVE'],
            'Asian': +d['ASIAN OR PACIFIC ISLANDER'],
            'Black': +d['BLACK'],
            'White' : +d['WHITE'],
            'Hispanic' : +d['HISPANIC'],
            'Multiracial' : +d['MULTIRACIAL'],
            'Economically Disadvantged' : +d['ECONOMICALLY DISADVANTAGED'],
            'Economically Advantged' : +d['NOT ECONOMICALLY DISADVANTAGED'],
            'Female' : +d['FEMALE'],
            'Male' : +d['MALE'],
            'Formerly Limited English Proficent' : +d['FORMERLY LIMITED ENGLISH PROFICIENT'],
            'Limited English Proficent' : +d['LIMITED ENGLISH PROFICIENT'],
            'English Proficent' : +d['NOT LIMITED ENGLISH PROFICIENT'],
            'General Education' : +d['GENERAL EDUCATION STUDENTS'],
            'Student with Disabilities' : +d['STUDENTS WITH DISABILITIES'],
            'Not Migrant' : +d['NOT MIGRANT'],
            'Migrant' : +d['MIGRANT'],
            'Teacher Inexperience' : +d['PER_TEACH_INEXP'],
            'Graduation Rate' : +d['PCT_GRAD'],
            'Year' : +d['YEAR']
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

function ready(error, ny, schoolData) {   
    var k = Object.keys(schoolData[0])
    k.shift()
    k.pop()
    k.sort()
    
    // enter code to append the game options to the dropdown
    var select = document.getElementById("ses")
    for(var i = 0; i < k.length; i++) {
        var game = k[i]
        var el = document.createElement("option")
        el.textContent = game
        el.value = game
        select.appendChild(el)
    }
    
    // event listener for the dropdown. Update choropleth and legend when selection changes. Call createMapAndLegend() with required arguments.
        var s = document.getElementById("ses")
        var y = document.getElementById("year")
		s.addEventListener("change", function() {
            createMapAndLegend(ny, schoolData, this.value, y.value)})

        y.addEventListener("change", function() {
            createMapAndLegend(ny, schoolData, s.value, this.value)})

    // create Choropleth with default option. Call createMapAndLegend() with required arguments. 
    createMapAndLegend(ny, schoolData, 'Graduation Rate', 2015)
}

// this function should create a Choropleth and legend 
function createMapAndLegend(ny, schoolData, selectedSES, selectedYear){ 
    svg.selectAll(".new-york").remove()

    var data = schoolData.filter(x => x.Year==selectedYear)

    //var genderData = (({ MALE, FEMALE }) => ({ MALE, FEMALE }))(data)
    color.domain([d3.min(data, function(d){return d[selectedSES];}), 
        d3.max(data, function(d){return d[selectedSES];})])
    
    svg.append("g")
        .attr("class", "new-york")
        .selectAll("path")
        .data(topojson.feature(ny, ny.objects.cb_2015_new_york_county_20m).features)
        .enter()
        .append("path")
        .attr("d", path)
        .attr("stroke", "white")
        .attr("fill", function(d) {
            var county = (d.properties.NAME).toUpperCase()
            data.forEach(function(e) {
                if (e['County'] == county) {
                    d.grad_rate = e[selectedSES]
                }
            })
            if (d.grad_rate != null) {
                return color(d.grad_rate)
            } else {
                return "gray"
            }
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
