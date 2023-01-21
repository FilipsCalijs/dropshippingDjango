
!(function($) {
  "use strict";

  // Set the count down timer
  if ($('.countdown').length) {
    var count = $('.countdown').data('count');
    var template = $('.countdown').html();
    $('.countdown').countdown(count, function(event) {
      $(this).html(event.strftime(template));
    });
  }

  // Back to top button
  $(window).scroll(function() {
    if ($(this).scrollTop() > 100) {
      $('.back-to-top').fadeIn('slow');
    } else {
      $('.back-to-top').fadeOut('slow');
    }
  });

  $('.back-to-top').click(function() {
    $('html, body').animate({
      scrollTop: 0
    }, 1500, 'easeInOutExpo');
    return false;
  });

})(jQuery);

// home slider
$(document).ready(function(){

  $('.site-slider').owlCarousel({
      loop: true,
      auto: true,
      dots: false,
      mouseDrag: true,
      autoplay: true,
      items: 1,
      nav: true,
      navText:["<div class='nav-btn prev-slide'><i class='material-icons'>arrow_backward</i></div>","<div class='nav-btn next-slide'><i class='material-icons'>arrow_forward</i></div>"],
      slideTransition: 'linear',
      autoplayTimeout: 10000,
      autoplaySpeed: 3000,
    onTranslated: function() {
        var $slideHeading = $('.site-slider .owl-item.active .slider-text h3');
        var $slidePara = $('.site-slider .owl-item.active .slider-text p');
        var $slidebtn = $('.site-slider .owl-item.active .slider-text .banner-btns');
  
          $slideHeading.addClass('animate-in-fast').on('animationend', function(){
          $slideHeading.removeClass('animate-in-fast').addClass('opacFull');
        });
  
          $slidePara.addClass('animate-in-slow').on('animationend', function(){
          $slidePara.removeClass('animate-in-slow').addClass('opacFull');
        });
  
          $slidebtn.addClass('animate-in-slow').on('animationend', function(){
          $slidebtn.removeClass('animate-in-slow').addClass('opacFull');
        });
      },
    onChange: function(){
      var $slideHeading = $('.site-slider .owl-item.active .slider-text h3');
      var $slidePara = $('.site-slider .owl-item.active .slider-text p');
      var $slidebtn = $('.site-slider .owl-item.active .slider-text .banner-btns');
  
      $slideHeading.removeClass('opacFull');
      $slidePara.removeClass('opacFull');
      $slidebtn.removeClass('opacFull');
  
    }
      });
  });
  
  $(window).on('load', function(){
  var $slideHeading = $('.site-slider .owl-item.active .slider-text h3');
  var $slidePara = $('.site-slider .owl-item.active .slider-text p');
  var $slidebtn = $('.site-slider .owl-item.active .slider-text .banner-btns');
  
      $slideHeading.addClass('animate-in-fast').on('animationend', function(){
      $slideHeading.removeClass('animate-in-fast').addClass('opacFull');
      $slidebtn.removeClass('animate-in-fast').addClass('opacFull');
  });
  
      $slidePara.addClass('animate-in-slow').on('animationend', function(){
      $slidePara.removeClass('animate-in-slow').addClass('opacFull');
      $slidebtn.removeClass('animate-in-slow').addClass('opacFull');
  });
  });

//project slider
$(document).ready(function(){

  //Slick Carousel Controllers
  $(".latest-project").slick({
  centerMode: true,
  centerPadding: "0px",
  dots: true,
  slidesToShow: 3,
  infinite: true,
  arrows: false,
  lazyLoad: "ondemand",
  responsive: [
      {
      breakpoint: 1024,
      settings: {
          slidesToShow: 2,
          centerMode: false
      }
      },
      {
      breakpoint: 767,
      settings: {
          slidesToShow: 1
      }
      }
  ]
  });
}); 

// page loader
$(window).load(function() {
  $('#loading').hide();
});

// testimonial slider

  $("#testimonial-slider").owlCarousel({
      items:2,
      itemsDesktop:[1000,2],
      itemsDesktopSmall:[979,2],
      itemsTablet:[768,2],
      itemsMobile:[650,1],
      pagination:true,
      navigation:false,
      slideSpeed:1000,
      autoPlay:true
  });

  // brands slider

  $('.brand-carousel').owlCarousel({
    loop:true,
    items:5,
    margin: 10,
    itemsDesktop:[1000,2],
    itemsDesktopSmall:[979,2],
    itemsTablet:[768,2],
    itemsMobile:[650,1],
    pagination:true,
    navigation:false,
    slideSpeed:1000,
    autoPlay:true
  });

  // form validator
  function ValidateEmail(email) {
    // alert(1);
		var expr = /^([\w-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/;
		return expr.test(email);
	};
	// $("#demo").live("click", function () {
	$("#demo").click(function() {
		if(!ValidateEmail($("#txtEmail").val())) {
			$("#error").addClass("error-msg-display");
		} else {
			$("#error").removeClass("error-msg-display");
			// $( "#success" ).addClass("success-msg-display");
			$("#success").addClass("success-msg-display").delay(3000).queue(function() {
				$(this).removeClass("success-msg-display").dequeue();
			});
		}
	});

// function run spinner on the button "run scraping" on the page fill-database.html
function runSpinner() {
    var spinner = document.getElementById("spinner");
    spinner.style.visibility = 'visible'; //'hidden'
};
