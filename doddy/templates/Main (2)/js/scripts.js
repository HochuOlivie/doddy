$.noConflict();
jQuery(document).ready(function($){
function getScreenHeight() {
    if($(".screen_height").length > 0) {
        topCoord = $("#topCoord").offset().top
        screenHeight = $(window).height() - topCoord - parseInt($(".content").css("padding-bottom")) - parseInt($("section").css("padding-top"));
        $(".screen_height").css({
            "min-height" : "auto"
        });
        $(".screen_height").css({
            "min-height" : screenHeight + "px"
        });
    }
}
function getLineParams() {
    $(".line").css({
        "width" : "auto"
    });
    leftCoord = $(".step_2:eq(0)").offset().left;
    rightCoord = $(".step_2:eq(1)").offset().left;
    lineWidth = rightCoord - leftCoord + 17;
    $(".line").css({
        "width" : lineWidth  + "px"
    });
}
function getRespParams() {
    // if($("#boostCoord").length > 0) {
    //     boostCoord = $("#boostCoord").offset().top + $("#boostCoord").outerHeight(true) + 25;
    //     footerCoord = $(".footer_section").offset().top;
    //     if(boostCoord >= footerCoord) {
    //         $("body").addClass("resp");
    //     }
    // }
    if($(window).height() <= 1450) {
        $("body").addClass("resp");
    } else {
        $("body").removeClass("resp");
    }
    console.log($(window).height());
}
$(window).resize(function() {
    getScreenHeight();
    getLineParams();
    getRespParams();
});
$(document).scroll(function() {
    getScreenHeight();
    getLineParams();
    getRespParams();
});
$(window).on('load', function(){
    getRespParams();
});
$(document).ready(function() {
    getScreenHeight();
    getLineParams();    
    const swiper = new Swiper('.slider', {
        loop: true,
        direction: 'horizontal',
        navigation: {
            nextEl: '.slide_next',
            prevEl: '.slide_prev',
        },
        keyboard: 
        {
            enabled: true,
            onlyInViewport: false,
        }
    });

    // -----------

    $(document).on("click", "[data-popup-link]",  function(e) {
      e.preventDefault();
      popupName = $(this).attr("data-popup-link");
      div = document.createElement('div');
      div.style.overflowY = 'scroll';
      div.style.width = '50px';
      div.style.height = '50px';
      div.style.visibility = 'hidden';
      document.body.appendChild(div);
      scrollWidth = div.offsetWidth - div.clientWidth;
      document.body.removeChild(div);
      topCoord = $(document).scrollTop();
      $("body").addClass("fixed");
      $("body").css({
          "top" :  -1 * topCoord + "px",
          "padding-right" : scrollWidth + "px"
      });
      $(".popup_bg").fadeIn(300);
      $("[data-popup = '"+ popupName +"']").fadeIn(300);
    });
    $(document).on("click", ".close, .popup_bg, .close_2", function(e) {
      e.preventDefault();
      curTop = $("body").css("top");
      curTop = Math.abs(parseInt(curTop, 10));
      $("body").removeClass("fixed");
      if (curTop !== 0) {
          $("html").scrollTop(curTop);
      }
      $("body").attr("style", "");
      $("[data-popup]").fadeOut(300);
      $(".popup_bg").fadeOut(300);
    });
    $(this).keydown(function(eventObject){
      if (eventObject.which == 27 && $("body").hasClass("fixed")) {
        curTop = $("body").css("top");
        curTop = Math.abs(parseInt(curTop, 10));
        $("body").removeClass("fixed");
        if (curTop !== 0) {
            $("html").scrollTop(curTop);
        }
        $("body").attr("style", "");      
        $(".popup_bg").fadeOut(300);
        $("[data-popup]").fadeOut(300);
      }
    });
    $(document).on("mouseup", function(e) {
      if($(".popup").is(":visible")) {
        e.preventDefault();
        hide_element = $(".popup_content");
        if (!hide_element.is(e.target)
            && hide_element.has(e.target).length === 0) {
            curTop = $("body").css("top");
            curTop = Math.abs(parseInt(curTop, 10));
            $("body").removeClass("fixed");
            if (curTop !== 0) {
                $("html").scrollTop(curTop);
            }
            $("body").attr("style", "");    
            $(".popup_bg").fadeOut(300);
            $("[data-popup]").fadeOut(300);
        }
      }
    });

    // ---------
    if($('.marque').length > 0 && $('.marque .js-marquee-wrapper').length == 0) {
        $('.marque').marquee({
            duration: 20000,
            startVisible: true,
            duplicated: true
        });
    }

});

});