function submit_vote(href) {
	$.post(href, {}, function(data) {}, "json");
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
