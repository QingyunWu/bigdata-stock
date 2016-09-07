//frontside logic
//run func when page loads
$(function() {

	//smoothie
	var smoothie = new SmoothieChart({
		timestampFormatter:SmoothieChart.timeFormatter
	});

	var line1 = new TimeSeries();
	
	smoothie.streamTo(document.getElementById("StockChart"), 1000);
	smoothie.addTimeSeries(line1, {
		lineWidth: 3
	});
	var socket = io();

	//when server emit 'data', update UI
	socket.on('data', function (data) {
		console.log(data);
		parsed = JSON.parse(data);

		//D3
		line1.append(Math.trunc(parsed['timestamp'] * 1000), parsed['average'])
	});
});