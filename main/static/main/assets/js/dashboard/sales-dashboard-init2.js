! function (e) {
	"use strict";


	// Float Bar Chat
	var flotChartOption1 = {
		series: {
			shadowSize: 0,
			bars: {
				show: true,
				lineWidth: 0,
				barWidth: .5,
				fill: 1
			}
		},
		grid: {
			aboveData: true,
			color: '#e5e9f2',
			borderWidth: 0,
			labelMargin: 0
		},
		yaxis: {
			show: true,
			min: 0,
			max: 15
		},
		xaxis: {
			show: true
		}
	};

	$.plot('#flotBarRecentOrders', [{
		data: data7,
		color: '#66a4fb'
	}], flotChartOption1);


	$.plot('#flotBarCompleteOrders', [{
		data: data7,
		color: '#e83e8c'
	}], flotChartOption1);

}(jQuery);