document.addEventListener('DOMContentLoaded', function () {
  var options = {
    draggable: true,
    edge: 'left'
  }
  var elems = document.querySelectorAll('.sidenav');
  var instances = M.Sidenav.init(elems, options);

  $('.collapsible').collapsible();

  console.log('loaded');



  // GitHub gets

  async function connectProject(repo) {
    let response = await axios.get(`https://api.github.com/repos/kayjitsu/${repo}`);
    console.log(response);
  }

  async function getUser(username) {
    let response = await axios.get(`https://api.github.com/repos/${username}/repos`);
    return response;
  }

  

});