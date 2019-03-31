
$(document).on('click', '.trigger', function (event) {
    event.preventDefault();
    var target = $(this.hash);
    console.log(target);
    target.iziModal('open');
});

$(document).ready(function() {
	$(".modal").iziModal({width:700});

	$('a[href*="#"]')
	  .not('[href="#"]')
	  .not('[href="#0"]')
	  .click(function(event) {
	    if (this.classList.contains('trigger')){
	      var target = $(this.hash);
	      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
	      if (target.length) {
	        event.preventDefault();
	        target.iziModal('open');
	      }
	    }
	  });
});