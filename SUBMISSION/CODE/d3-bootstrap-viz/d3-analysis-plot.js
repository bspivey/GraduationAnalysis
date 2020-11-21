export function Analysis(county){
    d3.select('.album').attr('style', 'display:block')
    Promise.all([
        // enter code to read files
        d3.dsv(",", "PCA_plus_preds.csv", function(d) {
            return {
                'County': d.county,
                'PCA1': +d.X1,
                'PCA2': +d.X2,
                'y': +d.y,
                'y_pred': +d.y_pred
            }
        }),
        d3.dsv(",", "county_agg_results.csv", function(d) {
            return {
                'County': d.county,
                'R2': +d.R2,
                'X1': +d.M1,
                'X2': +d.M2,
                'y_intercept': +d.C
            }
        })
    ]).then(function (data, error) {
        // enter code to call ready() with required arguments
    
        ready(error, data[0], data[1], county.properties.NAME)
        }
    );

    function ready(error, scatter, analysis, selectedCounty) { 
        d3.select("#analysis").remove()
        
        d3.select('#analysis-container').append('div').attr('id', 'analysis')  
        // define margin and dimensions for svg
        var m = {left: 50, right: 200, top: 50, bottom: 50};
        var w = 1080 - m.left - m.right;
        var h = 400 - m.top - m.bottom;

        // create svg
        var svg = d3.select("#analysis")
        .append("svg")
        .attr("width", w + m.left + m.right)
        .attr("height", h + m.top + m.bottom)
        .append("g")
        .attr("transform", "translate(" + m.left + "," + m.top + ")");

        // x, y, and color scale
        var x1 = d3.scaleLinear().range([0, w])
        var x2 = d3.scaleLinear().range([h, 0])
        var y = d3.scaleLinear().range([h, 0])
        var y_pred = d3.scaleLinear().range([h, 0])
        var color = d3.scaleOrdinal().range(d3.schemeDark2)

        // enter code to define tooltip
        var pca_tip = d3.tip()
            .attr("class", "d3-tip")
            .html(function(d) { return 'County : ' + d.County + '</br></br> PCA1 : ' + d.PCA1 + '</br></br> PCA2 : ' + d.PCA2 })

        var a_tip = d3.tip()
            .attr("class", "d3-tip")
            .html(function(d) { return 'County : ' + d.County + '</br></br> y : ' + d.y  })

        var pre_tip = d3.tip()
            .attr("class", "d3-tip")
            .html(function(d) { return 'County : ' + d.County + '</br></br>Predicted y : ' + d.y_pred + '</br></br>R-Squared : ' + d['R Squared']  })
        
        //filter data by county
        var scatterData = scatter.filter(x => x.County==selectedCounty)
        var predictedData = scatter.filter(x => x.County==selectedCounty)
        predictedData = predictedData.filter( x => x.y_pred!=0 )
        
        //set data domain
        x1.domain([d3.min(scatterData, function(d){return Math.max(d.PCA1)}), d3.max(scatterData, function(d){return Math.max(d.PCA1)})])
        x2.domain([d3.min(scatterData, function(d){return Math.max(d.PCA2)}), d3.max(scatterData, function(d){return Math.max(d.PCA2)})])
        y.domain([0, d3.max(scatterData, function(d){return Math.max(d.y)})])
        y_pred.domain([0, d3.max(scatterData, function(d){return Math.max(d.y_pred)})])
        color.domain(['Principal Components', 'Actual', 'Predicted'])

        //pca scatter plot
        svg.append("g")
            .selectAll("scatter")
            .data(scatterData)
            .enter()
            .append("circle")
            .attr("r", 5)
            .attr("cx", function(d) { d['R Squared'] = analysis[0].R2
                return x1(d.PCA1) })
            .attr("cy", function(d) { return x2(d.PCA2) })
            .style("opacity", 0.5)
            .attr('fill', function(d) { return color('Principal Components') })
            .on('mouseover', pca_tip.show)
            .on('mouseout', pca_tip.hide)
        
        //actual scatter plot
        svg.append("g")
            .selectAll("scatter")
            .data(scatterData)
            .enter()
            .append("circle")
            .attr("r", 5)
            .attr("cx", function(d) { d['R Squared'] = analysis[0].R2
                return x1(d.PCA1) })
            .attr("cy", function(d) { return y(d.y) })
            .style("opacity", 0.5)
            .attr('fill', function(d) { return color('Actual') })
            .on('mouseover', a_tip.show)
            .on('mouseout', a_tip.hide)

        //add regression prediction
        svg.append("g")
            .selectAll("scatter")
            .data(predictedData)
            .enter()
            .append("circle")
            .attr("r", 5)
            .attr("cx", function(d) { d['R Squared'] = analysis[0].R2
                return x1(d.PCA1) })
            .attr("cy", function(d) { return y_pred(d.y_pred) })
            .style("opacity", 0.5)
            .attr('fill', function(d) { return color('Predicted') })
            .on('mouseover', pre_tip.show)
            .on('mouseout', pre_tip.hide)
            
            
        svg.call(pca_tip)
        svg.call(a_tip)
        svg.call(pre_tip)
    
        // Add the X Axis
        svg.append("g")
            .attr("transform", "translate(0," + h + ")")
            .call(d3.axisBottom()
            .scale(x1));

        // Add the Y Axis
        svg.append("g")
            .attr("transform", "translate(" + x1(0) + ",0)")
            .call(d3.axisLeft(y));

        // Add the text label for X Axis
        svg.append("text")
            .attr('class', 'labels')             
            .attr("transform", "translate(" + (w/2) + " ," + (h + 50) + ")")
            .style("text-anchor", "middle")
            .text('PCA1');

        // Add the text label for Y axis
        svg.append("text")
            .attr('class', 'labels')
            .attr("transform", "translate(" + (12 - m.left) + ", " + (h/2) + ") rotate(-90)")
            .style("text-anchor", "middle")
            .text('PCA2');

        // Add the text Title
        svg.append("text")
            .attr("transform", "translate(" + ((w + m.right)/2) + ", -30)")
            .style("text-anchor", "middle")
            .text('Principal Component Regression');

        //add legend
        svg.append("text")
            .attr("x", w + 40)
            .attr("y", 55 )
            .text('Principal Components')
            .style("fill", color('Principal Components'))

        svg.append("text")
            .attr("x", w + 40)
            .attr("y", 75 )
            .text('Actual')
            .style("fill", color('Actual'))
        
        svg.append("text")
            .attr("x", w + 40)
            .attr("y", 95 )
            .text('Predicted')
            .style("fill", color('Predicted'))

    }
}