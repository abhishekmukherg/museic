function submit_vote(href) {
	$.post(href, {}, function(data) {
		if (data.status == "success") {
			var new_perc = (data.score * 100) / 4;
			$('li.current-rating').attr('style',
						'width: ' + new_perc + '%;')
		}
	}, "json");
	return false;

}
$(document).ready(function() {
    debug = true;

    for (var i = 1; i <= 5; i++) {
    	var star = $('a.star_' + i);
	var href = star.attr('href').replace(/\/[^\/]+/, "/ajax");
	star.attr('onclick', 'submit_vote("' + href + '"); return false');
	star.attr('href', '#');
    }
});
