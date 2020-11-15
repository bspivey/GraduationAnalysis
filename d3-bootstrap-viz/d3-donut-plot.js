export function Donut(county){
    var radius = 150

    var color = d3.scaleOrdinal().range(d3.schemeDark2)

    // enter code to define tooltip
    var tip = d3.tip()
        .attr("class", "d3-tip")
        .html(function(d) { return d.data.key + ' : ' + d.value })

    d3.dsv(",", "df_grad_rate_pct_county_merge.csv", function (d) {
        return {
            'County': d.COUNTY_NAME,
            'Indian': +d['AMERICAN INDIAN OR ALASKA NATIVE'],
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
            'Graduation' : +d['PCT_GRAD'],
            'Year' : +d['YEAR']   
        }
    }).then(function (data) {

        var s = document.getElementById("year")
	    s.addEventListener("change", function() {
            createDonut(data, this.value, county.properties.NAME.toUpperCase())})
    
        createDonut(data, 2015, county.properties.NAME.toUpperCase())
    })
    function createDonut(schoolData, selectedYear, selectedCounty) {
        d3.select('#subchart').remove()
        d3.select('#choropleth').append('div').attr('id', 'subchart')
        
        // define margin and dimensions for svg
        var m = {left: 50, right: 50, top: 20, bottom: 0};
        var w = 1200 - m.left - m.right;
        var h = 300 - m.top - m.bottom;

        // create svg
        var svg = d3.select("#subchart")
        .append("svg")
        .attr("width", w + m.left + m.right)
        .attr("height", h + m.top + m.bottom)
        .append("g")

        var data2 = schoolData.filter(x => x.Year==selectedYear)
        data2 = data2.filter(y => y.County==selectedCounty)
        var countyData = (({ Male, Female }) => ({ Male, Female}))(data2[0])
        
        var raceData = (({ Indian, Asian, Black, White, Hispanic, Multiracial }) => ({ Indian, Asian, Black, White, Hispanic, Multiracial }))(data2[0])
        
        var gradData = (({ Graduation }) => ({ Graduation }))(data2[0])

        color.domain(Object.keys(countyData))

        var pie = d3.pie()
            .value(function(d) { return d.value })
            
        var pieData = pie(d3.entries(countyData))

        var arc = d3.arc()
            .innerRadius(radius * 0.5)
            .outerRadius(radius * 0.8)

        svg.selectAll('.allSlices')
            .data(pieData)
            .enter()
            .append('path')
            .attr('class', 'allSlices')
            .attr('d', arc)
            .attr('fill', function(d){ return color(d.data.key) })
            .attr("stroke", "white")
            .style("stroke-width", "1px")
            .style("opacity", 0.7)
            .attr("transform", "translate(150, 150)")
            .on('mouseover', tip.show)
            .on('mouseout', tip.hide)

        svg.append('svg:foreignObject')
            .attr('height', '80px')
            .attr('width', '70px')
            .attr("transform", "translate(120, 110)")
            .attr("color", "#3895D3")
            .attr('font-size', function (d) { return '60px' })
            .html('<i class="fa fa-venus-mars"></i>'); 

        svg.call(tip)

        svg.append("line")
            .attr("x1", 350)
            .attr("y1", 20)
            .attr("x2", 350)
            .attr("y2", 280)
            .style("stroke-width", 1)
            .style("stroke", "#3895D3")
            .style("opacity", 0.2)
            .style("fill", "none");

        svg.append('svg:foreignObject')
            .attr('height', '80px')
            .attr('width', '80px')
            .attr("transform", "translate(515, 30)")
            .attr("color", "#3895D3")
            .attr('font-size', function (d) { return '60px' })
            .html('<i class="fa fa-graduation-cap"></i>');

        svg.append("text")
            .attr("transform", "translate(" + (w/2) + " , 165)")
            .style("text-anchor", "middle")
            .attr('font-size', '36px')
            .text(gradData['Graduation'] + ' %');

        svg.append("text")
            .attr("transform", "translate(" + (w/2) + " , 190)")
            .style("text-anchor", "middle")
            .text('Graduation Percentage in ' + county.properties.NAME + ' County.');

        var pie2 = d3.pie()
            .value(function(d) { return d.value })
            var pie2Data = pie(d3.entries(raceData))

        svg.selectAll('.allSlices2')
            .data(pie2Data)
            .enter()
            .append('path')
            .attr('class', 'allSlices2')
            .attr('d', arc)
            .attr('fill', function(d){ return color(d.data.key) })
            .attr("stroke", "white")
            .style("stroke-width", "1px")
            .style("opacity", 0.7)
            .attr("transform", "translate(950, 150)")
            .on('mouseover', tip.show)
            .on('mouseout', tip.hide)

        svg.append('svg:foreignObject')
            .attr('height', '80px')
            .attr('width', '80px')
            .attr("transform", "translate(915, 100)")
            .attr("color", "#3895D3")
            .attr('font-size', function (d) { return '60px' })
            .html('<i class="fa fa-users"></i>');

        svg.append("line")
            .attr("x1", 750)
            .attr("y1", 20)
            .attr("x2", 750)
            .attr("y2", 280)
            .style("stroke-width", 1)
            .style("stroke", "#3895D3")
            .style("opacity", 0.2)
            .style("fill", "none");

        svg.append('svg:foreignObject')
            .attr('height', '20px')
            .attr('width', '20px')
            .attr("transform", "translate(1080, 20)")
            .attr("color", "#3895D3")
            .attr('font-size', function (d) { return '12px' })
            .html('<i class="fa fa-times-circle"></i>')
            .on('click', removeChart)

        function removeChart(){
            d3.select('#subchart').remove()
        }
    }
}