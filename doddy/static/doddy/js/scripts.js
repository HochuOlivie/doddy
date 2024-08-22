$.noConflict();
jQuery(document).ready(function($){
function getScreenHeight(scale) {
    if($(".screen_height").length > 0) {
        topCoord = $("#topCoord").offset().top;
        if($(".top_box").length > 0) {
            topBox = $(".top_box").height();
        } else {
            topBox = 0;
        }
        screenHeight = scaleHeight - topBox - parseInt($(".content").css("padding-bottom") ) - parseInt($(".content").css("padding-top") ) - 30 ;
        $(".screen_height").css({
            "min-height" : "auto"
        });
        $(".screen_height").css({
            "min-height" : screenHeight + "px"
        });
    }
}
function getRespParams() {
    if($(window).height() < 1450) {
        $("body").addClass("resp");
    } else {
        $("body").removeClass("resp");
    }
}
function getSizeParams() {
    if($(window).width() < 768) {
        $("body").css({
            "transform" : "scale(none)",
            "left" : "auto",
            "height" : "auto",
            "top" : "auto",
        });
        $(".content").css({
            "height" : "auto",
        });
        maxWidth = 767;
        devWidth = $(window).width();
        devHeight = $(window).height();
        scale = (devWidth*(100/maxWidth))/100;
        scaleHeight = devHeight / scale;
        $("body").css({
            "transform" : "scale("+scale+")",
            "height" : scaleHeight + "px",
        });
        toptOffset = parseInt($("body").offset().top);
        leftOffset = parseInt($("body").offset().left);
        $("body").css({
            "top" : -1 * toptOffset + "px",
            "left" : -1 * leftOffset + "px",
        });
        $(".content").css({
            "height" : scaleHeight + "px"
        });
         if($(".screen_height").length > 0) {
            topCoord = $("#topCoord").offset().top;
            if($(".top_box").length > 0) {
                topBox = $(".top_box").height();
            } else {
                topBox = 0;
            }
            screenHeight = scaleHeight - topBox - parseInt($(".content").css("padding-bottom") ) - parseInt($(".content").css("padding-top") ) - 30 ;
            $(".screen_height").css({
                "min-height" : "auto"
            });
            $(".screen_height").css({
                "min-height" : screenHeight + "px"
            });
        }
    } else {
        $("body").css({
            "transform" : "scale(1)",
            "left" : "auto",
            "height" : "auto",
            "top" : "auto",
        });
        $(".content").css({
            "height" : "100vh"
        });
    }
    // getRespParams();
    // getScreenHeight(scale);
}

$(window).resize(function() {
    // getRespParams();
    getSizeParams();
    // getScreenHeight();
    // getScreenHeight();
});
$(document).scroll(function() {
    // getScreenHeight();
    // getRespParams();
});
$(window).on('load', function(){
    // getRespParams();
});
$(document).ready(function() {
    getSizeParams();  
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
      // div = document.createElement('div');
      // div.style.overflowY = 'scroll';
      // div.style.width = '50px';
      // div.style.height = '50px';
      // div.style.visibility = 'hidden';
      // document.body.appendChild(div);
      // scrollWidth = div.offsetWidth - div.clientWidth;
      // document.body.removeChild(div);
      // topCoord = $(document).scrollTop();
      // $("body").addClass("fixed");
      // $("body").css({
      //     "top" :  -1 * topCoord + "px",
      //     "padding-right" : scrollWidth + "px"
      // });
      $(".popup_bg").fadeIn(300);
      $("[data-popup = '"+ popupName +"']").fadeIn(300);
    });
    $(document).on("click", ".close, .popup_bg, .close_2, .popup_content .blue_pill_ok", function(e) {
      e.preventDefault();
      // curTop = $("body").css("top");
      // curTop = Math.abs(parseInt(curTop, 10));
      // $("body").removeClass("fixed");
      // if (curTop !== 0) {
      //     $("html").scrollTop(curTop);
      // }
      // $("body").attr("style", "");
      $("[data-popup]").fadeOut(300);
      $(".popup_bg").fadeOut(300);
    });
    $(this).keydown(function(eventObject){
      if (eventObject.which == 27 && $("body").hasClass("fixed")) {
        // curTop = $("body").css("top");
        // curTop = Math.abs(parseInt(curTop, 10));
        // $("body").removeClass("fixed");
        // if (curTop !== 0) {
        //     $("html").scrollTop(curTop);
        // }
        // $("body").attr("style", "");      
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
            // curTop = $("body").css("top");
            // curTop = Math.abs(parseInt(curTop, 10));
            // $("body").removeClass("fixed");
            // if (curTop !== 0) {
            //     $("html").scrollTop(curTop);
            // }
            // $("body").attr("style", "");
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