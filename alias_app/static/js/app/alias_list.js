var List = (function() {
  var initialize = function() {
    $(".item a").on('click', function(e) {
      var $item = $(this).parent();
      e.preventDefault();

      $(".formlist .item.active").removeClass("active");
      $item.addClass('active');
      initializePanel($item);
    });

    // initialize already opened panel
    if ($(".formlist .item.active").length > 0) {
      initializePanel($(".formlist .item.active"));
    }
  }

  var initializePanel = function($item) {
    initializeCloseButton($item);

    $("button[name$='-DELETE']").on('click', function(e) {
      var answer = window.confirm("Would you really delete this alias?");

      if (answer === false) {
        e.preventDefault();
      }
    });
  }

  var initializeCloseButton = function($item) {
    $item.find("button.close").on('click', function() {
      $item.removeClass('active');
    });
  }

  return {
    init: initialize
  }
})();

jQuery(function($) {
  List.init();
});