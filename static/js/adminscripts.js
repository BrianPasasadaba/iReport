$(document).ready(function () {
  // Hide sub-menus initially
  $(".sub-menu").hide();

  // jQuery for toggle sub menus
  $(".sub-btn").click(function () {
    $(this).find(".sub-menu").slideToggle();
    $(this).find(".fa-chevron-down").toggleClass("fa-chevron-up"); // Toggle chevron-up class
  });

  // jQuery for expand and collapse the sidebar
  $(".menu-btn").click(function () {
    $(".sidebar").addClass("active");
    $(".menu-btn").css("visibility", "hidden");
  });

  // Active cancel button
  $(".close-btn").click(function () {
    $(".sidebar").removeClass("active");
    $(".menu-btn").css("visibility", "visible");
  });

  // Get all links in the sidebar
  var links = document.querySelectorAll(".sidebar a");

  // Get the current page URL
  var currentPage = window.location.href;

  // Loop through each link
  links.forEach(function (link) {
    // Check if the link's href matches the current URL
    if (currentPage.indexOf(link.getAttribute("href")) > -1) {
      // Add the 'active' class to the link
      link.classList.add("active");
      // If it's a dropdown item, add 'active' to its parent too
      if (link.parentNode.classList.contains("sub-menu")) {
        link.parentNode.parentNode.parentNode
          .querySelector(".dropdown-toggle")
          .classList.add("active");
      }
    }
  });
});
