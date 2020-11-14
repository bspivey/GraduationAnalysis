
// define margin and dimensions for svg
var m = {left: 50, right: 350, top: 20, bottom: 50};
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
var x = d3.scaleLinear().range([0, w])
var y = d3.scaleLinear().range([h, 0])
var color = d3.scaleOrdinal().range(['#e6194b', '#3cb44b', '#ffe119', 
    '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', 
    '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', 
    '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', '#000000'])

// enter code to define tooltip
var tip = d3.tip()
    .attr("class", "d3-tip")
    .html(function(d) { return Object.keys(d)[0] + ' : ' + d[Object.keys(d)[0]] })

d3.dsv(",", "df_grad_rate_pct_county_merge.csv", function (d) {
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
}).then(function (data) {
    // enter code to append the game options to the dropdown
    var s = document.getElementById("year")
    var county = data.filter(x => x.Year==s.value)
    
    var select = document.getElementById("county1")
    for(var i = 0; i < county.length; i++) {
        var game = county[i]['County']
        var el = document.createElement("option")
        el.textContent = game
        el.value = game
        select.appendChild(el)
    }
    var c1 = document.getElementById('county1')
    var select1 = document.getElementById("county2")
    for(var i = 0; i < county.length; i++) {
        var game = county[i]['County']
        var el = document.createElement("option")
        el.textContent = game
        el.value = game
        select1.appendChild(el)
    }
    var c2 = document.getElementById('county2')
    c2.selectedIndex = 1
    
    var s = document.getElementById("year")
	s.addEventListener("change", function() {
        createScatter(data, this.value, c1.value, c2.value)})

    c1.addEventListener("change", function() {
        createScatter(data, s.value, this.value, c2.value)})
    
    c2.addEventListener("change", function() {
        createScatter(data, s.value, c1.value, this.value)})
        
    createScatter(data, 2015, "ALBANY", "ALLEGANY")

})

// create a Scatter Plot
function createScatter(schoolData, selectedYear, xCounty, yCounty){ 
    svg.selectAll(".circle").remove()
    svg.selectAll(".labels").remove()
    
    var keys = ["Year", 'County'];
    var values = [parseInt(selectedYear), xCounty, yCounty];
   
    var data = schoolData.filter(function(e) {
        return keys.every(function(a) {
            return values.includes(e[a])
        })
    })
    var scatterData = Object.keys(data).reduce((object, key) => {
        if (key !== 'County') {
          object[key] = data[key]
        }
        return object
      }, {})

      scatterData = Object.keys(scatterData).reduce((object, key) => {
        if (key !== 'County') {
          object[key] = scatterData[key]
        }
        return object
      }, {})
    // set the domains of X and Y scales based on data
    x.domain([0, 100])

    y.domain([0, 100])

    var k = Object.keys(scatterData[0])
    k.pop()
    k.shift()
    var ses = {}
    for (var i = 0; i < k.length; i++){
        if (isNaN(scatterData[0][k[i]])){
            data[0][k[i]] = 0
        } 
        if (isNaN(scatterData[1][k[i]])){
            data[1][k[i]] = 0
        }
        ses[k[i]] = [scatterData[0][k[i]], scatterData[1][k[i]]]
    }

    color.domain(k)

    var circle = svg.selectAll(".circle-group")
        .data([ses])
        .enter()
        .append("g")

    circle.selectAll(".circle")
        .data(function(d) { return  Object.keys(d).map(function(x) { var obj = {}
            obj[x]=d[x]
            return  obj  })})
        .enter()
        .append("circle")
        .attr("class", "circle")
        .attr("r", 5)
        .attr("cx", function(d) { var k = Object.keys(d)[0]
            if(isNaN(d[k][0])){
                return x(0)
            } else {
                return x(d[k][0])} })
        .attr("cy", function(d) { var k = Object.keys(d)[0]
            if (isNaN(d[k][1])){
                return y(0)
            } else {
                return y(d[k][1])} })
        .attr('fill', function(d) { var k = Object.keys(d)[0]
            return color(k) })
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
    .attr('class', 'labels')             
    .attr("transform", "translate(" + (w/2) + " ," + (h + m.top + 30) + ")")
    .style("text-anchor", "middle")
    .text(xCounty);

    // Add the text label for Y axis
    svg.append("text")
    .attr('class', 'labels')
    .attr("transform", "translate(" + (12 - m.left) + ", " + (h/2) + ") rotate(-90)")
    .style("text-anchor", "middle")
    .text(yCounty);
    
    // Legend
    svg.append("g")
        .attr("class", "legend")
        .attr("transform", "translate(750,-35)");

    var legend = d3.legendColor()
        .scale(color)

    svg.select(".legend")
        .call(legend)
}
