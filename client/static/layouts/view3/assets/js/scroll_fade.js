$(document).ready(function() {
	$('div#parallax').scroll(function(){
	    $(".header_text").css("opacity", 1 - $('div#parallax').scrollTop() / 200);
	  });

});