// On document load

document.addEventListener('DOMContentLoaded', function () {
  var options = {
    draggable: true,
    edge: 'left'
  }
  var elems = document.querySelectorAll('.sidenav');
  var instances = M.Sidenav.init(elems, options);

  $('.collapsible').collapsible();

  $(function () {
    $(".lecture-link").on("click", function (e) {
      e.preventDefault();
      let id = $(this).data('lecture-id');
      let url = $(this).data('lecture-url');
      $('#main').html(`<iframe src='${url}'></iframe>`);
    });
  });

  $(function () {
    $(".exercise-link").on("click", function (e) {
      e.preventDefault();
      let id = $(this).data('exercise-id');
      let url = $(this).data('exercise-url');
      $('#main').html(`<iframe src='${url}'></iframe>`);
      $(`#${id}`).addClass('active');
    });
  });

  // Sidenav highlights
  $(function () {
    $('.lecture-link').on('click', function (e) {

      // Remove all active nav
      $("li").removeClass('active-li');

      // Highlight active nav
      let $active = e.target.parentNode;
      $($active).addClass('active-li')

      // Check if close nav on mobile
      let nav = $(this).data('li-parent');
      if ($(window).width() < 990) {
        if (nav === 'no') {
          $('.sidenav').sidenav('close');
        }
      }
    })
  });

  // Sidenav sticky highlights for exercises
  $(function () {
    $('.exercise-link').on('click', function (e) {

      // Remove all active nav
      $("li").removeClass('active-li');

      // Highlight active nav
      let $active = e.target.parentNode;
      $($active).addClass('active-li')

      // Check if close nav on mobile
      let nav = $(this).data('li-parent');
      if ($(window).width() < 990) {
        if (nav === 'no') {
          $('.sidenav').sidenav('close');
        }
      }
    })
  });

  console.log('loaded');

});