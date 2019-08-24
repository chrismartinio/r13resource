// On document load

document.addEventListener('DOMContentLoaded', function () {
  var options = {
    draggable: true,
    edge: 'left'
  }
  var elems = document.querySelectorAll('.sidenav');
  var instances = M.Sidenav.init(elems, options);

  $('.collapsible').collapsible();

  console.log('loaded');





});

// $(function () {
//   $(".lecture-link").on("click", function (e) {
//     e.preventDefault(); // cancel the link itself
//     let id = $(this).data('lecture-id');
//     $('#main').append(`<iframe src='/lectures/?id=${id}'></iframe>`);
//   });
// });