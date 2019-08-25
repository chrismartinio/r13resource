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

  $('.sidenav li').click(() => {
    $('.sidenav').sidenav('close');
    console.log('close');
  })

  console.log('loaded');

});

