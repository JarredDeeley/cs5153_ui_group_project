var Turbolinks = require("turbolinks");
Turbolinks.start();

$(function() {
  $('button').click(function() {
    var user = $('#txtUsername').val();
    var pass = $('#txtPassword').val();
    $.ajax({
      url: '/signUpUser',
      data: $('form').serialize(),
      type: 'POST',
      success: function(response) {
        console.log(response);
      },
      error: function(error) {
        console.log(error);
      }
    });
  });
});

// $(document).on("turbolinks:load", function() {
//   $.ajaxSetup({
//     beforeSend: function(xhr) {
//       return xhr.setRequestHeader('Accept', 'text/javascript');
//     }
//   });
// });
