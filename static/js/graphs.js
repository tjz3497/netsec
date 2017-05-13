queue()
    .defer(d3.json, "/data")
    #.defer(d3.json, "static/geojson/us-states.json")
    .await(makeGraphs);

function makeGraphs(error, avgJson, mapJson) {

	average = avgJson;

	//var ndx = crossfilter(average);

	var ipDim = avgJson.dimension(function(d) {
		return d.mag; 
	});

	//var numIps = ipDim.group();

	var barGraph = dc.barChart("#bar-graph");

	barGraph
		.width(600)
		.width(600)
		.height(160)
		.margins({top: 10, right: 50, bottom: 30, left: 50})
		.dimension(ipDim)
		.group(3)
		.transitionDuration(500)
		.x(d3.linear.scale().domain([0, 20000]))	
		.elasticY(true)
		.xAxisLabel("IP")
		.yAxis().ticks(4);

    dc.renderAll();

};