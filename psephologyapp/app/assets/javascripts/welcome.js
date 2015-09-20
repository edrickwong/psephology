$( document ).ready(function() {
    new Chartist.Line('.ct-chart', {
	  labels: gon.dates,
	  series: [
	    gon.cpcSentiment,
	    gon.lpcSentiment,
	    gon.ndpSentiment,
	  ]
	}, {
	  fullWidth: true,
	  chartPadding: {
	    right: 60
	  }
	});
});