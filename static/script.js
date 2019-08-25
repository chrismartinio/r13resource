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
      console.log('click')
      let id = $(this).data('lecture-id');
      let url = $(this).data('lecture-url');
      $('#main').html(`<iframe src='${url}'></iframe>`);
      $(`#${id}`).addClass('active');
    });
  });
  
  $(function () {
    $(".exercise-link").on("click", function (e) {
      e.preventDefault(); 
      console.log('click')
      let id = $(this).data('exercise-id');
      let url = $(this).data('exercise-url');
      $('#main').html(`<iframe src='${url}'></iframe>`);
      $(`#${id}`).addClass('active');
    });
  });

  console.log('loaded');

});

// $(function () {
//   $(".lecture-link").on("click", function (e) {
//     e.preventDefault(); 
//     let id = $(this).data('lecture-id');
//     let url = $(this).data('lecture-url');
//     $('#main').html(`<iframe src='${url}'></iframe>`);
//     $(`#${id}`).addClass('active');
//   });
// });

// $(function () {
//   $(".exercise-link").on("click", function (e) {
//     e.preventDefault(); 
//     let id = $(this).data('exercise-id');
//     let url = $(this).data('exercise-url');
//     $('#main').html(`<iframe src='${url}'></iframe>`);
//     $(`#${id}`).addClass('active');
//   });
// });