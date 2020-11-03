// define margin and dimensions for svg
var m = {left: 50, right: 200, top: 20, bottom: 50};
var w = 1080 - m.left - m.right;
var h = 400 - m.top - m.bottom;

// create svg
var svg = d3.select("#scatter")
.append("svg")
.attr("width", w + m.left + m.right)
.attr("height", h + m.top + m.bottom)
.append("g")
.attr("transform", "translate(" + m.left + "," + m.top + ")");

// x, y, and color scale
var x = d3.scalePoint().range([0, w])
var y = d3.scaleLinear().range([h, 0])

var color = d3.scaleOrdinal().range(["#525c72", "#21ce03", "#fe3302", 
    "#fa46ff", "#876d0d", "#a24568", "#159bfc", "#14926d", "#9149f8", 
    "#fd5a93", "#85706a", "#ad4d1e", "#4a8b00", "#a96bb1", "#04859b", 
    "#4d6643", "#e2770f", "#4567c6", "#d517a9", "#76527b", "#c310f3", 
    "#d5324b", "#7c78a9", "#657b79", "#7d80fd", "#949401", "#b46965", 
    "#017065", "#6f864d", "#805432", "#12ad4b", "#b86dfd", "#b0743b", 
    "#c66495", "#eb6555", "#5c5c59", "#0e7b3a"])

// enter code to define tooltip
var tip = d3.tip()
    .attr("class", "d3-tip")
    .html(function(d) { return Object.keys(d)[0] + ' : ' + d[Object.keys(d)[0]] })

d3.dsv(",", "df_grad_rate_pct_county.csv", function (d) {
    return {
        'COUNTY_NAME': d.COUNTY_NAME,
        'INDIAN': +d['AMERICAN INDIAN OR ALASKA NATIVE'],
        'ASIAN': +d['ASIAN OR PACIFIC ISLANDER'],
        'BLACK': +d['BLACK'],
        'HISPANIC' : +d['HISPANIC'],
        'WHITE' : +d['WHITE'],
        'MULTIRACIAL' : +d['MULTIRACIAL'],
        'FEMALE' : +d['FEMALE'],
        'MALE' : +d['MALE'],
        'FLEP' : +d['FORMERLY LIMITED ENGLISH PROFICIENT'],
        'LEP' : +d['LIMITED ENGLISH PROFICIENT'],
        'GENERAL ED' : +d['GENERAL EDUCATION STUDENTS'],
        'ECO DA' : +d['ECONOMICALLY DISADVANTAGED'],
        'DISABILITY' : +d['STUDENTS WITH DISABILITIES'],
        'MIGRANT' : +d['MIGRANT'],
        'TOTAL GRAD' : +d['PCT_GRAD'],
        'YEAR' : +d['YEAR']     
    }
}).then(function (data) {

    var s = document.getElementById("year")
	    s.addEventListener("change", function() {
            createScatter(data, this.value)})
    
    createScatter(data, 2015)

})

// create a Scatter Plot
function createScatter(schoolData, selectedYear){ 
    svg.selectAll(".circle").remove()

    var data = schoolData.filter(x => x.YEAR==selectedYear)

    var k = Object.keys(data[0])
    k.shift()
    k.pop()
    // set the domains of X and Y scales based on data
    x.domain(k)

    y.domain([0, d3.max(data, function(d){return d['TOTAL GRAD']})])

    color.domain([data.map(x => x['COUNTY_NAME'])])

    var circle = svg.selectAll(".circle-group")
        .data(data)
        .enter()
        .append("g")
        .style("fill", function(d) { return color(d['COUNTY_NAME']) })

    circle.selectAll(".circle")
        .data(function(d) {  return  Object.keys(d).map(function(x) { var obj = {}
            obj[x]=d[x] 
            return  obj  })})
        .enter()
        .append("circle")
        .attr("class", "circle")
        .attr("r", 5)
        .attr("cx", function(d) { var k = Object.keys(d)[0]
            return x(k)  })
        .attr("cy", function(d) { var k = Object.keys(d)[0]
            if (isNaN(d[k])) {
                return y(0)
            } else {
                return y(d[k])
            }
        })
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide)
    
    svg.call(tip)
    
    // Add the X Axis
    svg.append("g")
        .attr("class", "circle")
        .attr("transform", "translate(0," + h + ")")
        .call(d3.axisBottom()
        .scale(x));

    // Add the Y Axis
    svg.append("g")
    .attr("class", "circle")
        .call(d3.axisLeft(y));
    
    // Add the text label for X Axis
    svg.append("text")             
    .attr("transform", "translate(" + (w/2) + " ," + (h + m.top + 30) + ")")
    .style("text-anchor", "middle")
    .text("SES");

    // Add the text label for Y axis
    svg.append("text")
    .attr("transform", "translate(" + (12 - m.left) + ", " + (h/2) + ") rotate(-90)")
    .style("text-anchor", "middle")
    .text("Graduation Rate");
    
    // Legend
    svg.append("g")
        .attr("class", "legend")
        .attr("transform", "translate(880,-35)");

    var legend = d3.legendColor()
        .scale(color)

    svg.select(".legend")
        .call(legend)
}
