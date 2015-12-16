var List = (function() {
  var initialize = function() {
    $(".item .item-link").on("click", function(e) {
      var $item = $(this).parent();
      e.preventDefault();

      $(".formlist .item.active").removeClass("active");
      $item.addClass("active");
      initializePanel($item);
    });

    // initialize already opened panel
    if ($(".formlist .item.active").length > 0) {
      initializePanel($(".formlist .item.active"));
    }

    $("#id_new_alias_btn").on("click", function(e) {
      $(".empty-form").show().addClass("active");
      initializePanel($(".empty-form"));
      $(".empty-form").on("panel.closed", function(e) {
        $(".empty-form").hide();
      });
    });
  }

  var initializePanel = function($item) {
    initializeCloseButton($item);

    $(".panel-item-delete").on("click", function(e) {
      var answer = window.confirm("Would you really delete this alias?");

      if (answer === false) {
        e.preventDefault();
      }
    });
  }

  var initializeCloseButton = function($item) {
    $item.find("button.close").on("click", function() {
      $item.removeClass("active");
      $item.trigger("panel.closed");
    });
  }

  return {
    init: initialize
  }
})();

jQuery(function($) {
  List.init();
});