console.log("scripts.js loaded!");

$(document).ready(function () {

  

  // Accordion Toggle Icon & Header Color Change (Updated for Bootstrap 5)
  $('.accordion').on('hidden.bs.collapse', function () {
    $(this).find('.fa-chevron-up').removeClass('fa-chevron-up').addClass('fa-chevron-down');
  });

  $('.accordion').on('shown.bs.collapse', function () {
    $(this).find('.fa-chevron-down').removeClass('fa-chevron-down').addClass('fa-chevron-up');
  });

  // No changes needed for dropdown toggle initialization (Bootstrap 5 compatible)
  $(".dropdown-toggle").dropdown();

});
