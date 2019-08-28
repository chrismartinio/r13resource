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
    });
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



  $('#submit-user').on('submit', async function (e) {
    e.preventDefault();

    let username = $('#git_username').val();
    let response = await axios.post('/submit-user', {
      username
    });
    if (response.data === 480) {
      M.toast({
        html: 'user already exists'
      })
    } else if (response.data === 404) {
      M.toast({
        html: 'user not found'
      });
    } else if (response.data === 200) {
      M.toast({
        html: 'user added successfully'
      });
      setTimeout(function () {
        location.reload();
      }, 1000);
    } else {
      M.toast({
        html: 'unable to process'
      });
    }
    console.log(response);
  });

  $('#submit-resource').on('submit', async function (e) {
    e.preventDefault();

    let title = $('#resource-title').val();
    let url = $('#resource-url').val();
    console.log(title, url);
    let response = await axios.post('/resources', {
      title,
      url
    });

    if (response.data === 200) {
      M.toast({
        html: 'resource added'
      });
      setTimeout(function () {
        location.reload();
      }, 1000);
    } else {
      M.toast({
        html: 'unable to add'
      })
    }
  });
});