function writeError($input, text){
    $input.parent().find(".error").text(text)
}
function clearError($input){
    $input.parent().find(".error").text('')
}


$(document).ready(function(){

  var $form = $('form.sign-in');
  var $login_button = $('.login_button');

  $('#username').blur(function(evt){

    var $username = $('#username');
    var validUsername = false;

    $.ajax("/ajax/signin_username", {
      async:false,
      datatype: "json",
      type: "post",
      data: {username: $username.val()
      }, success: function(data){
          if (data.username_exists){
            validUsername = true;
            clearError($username)
          } else {
            validUsername = false;
            writeError($username, "Username cannot be found in database.");
          }
      }, failure: function(){
        alert("Failed to ajax. Check your internet connection.")
      }
    });

    return validUsername;

  });

  $('.login_button').click(function(evt){

    var $username = $('#username');
    var $password = $('#password');

    //TODO: Check if the password corresponds to hashed password in db
    // Refer to sign in post handler

    return;
  });

});
