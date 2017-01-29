function writeError($input, text){
    $input.parent().find(".error").text(text)
}
function clearError($input){
    $input.parent().find(".error").text('')
}


$(document).ready(function(){

  var $form = $('form.sign-in');
  var $login_button = $('.login_button');

  $('#username').on("change keyup", function(evt){

    var $username = $('#username');
    var isUsernameEmpty = false

    if ($username.val() == ''){
      writeError($username, 'This field is required.');
      isUsernameEmpty = true;
    } else {
      clearError($username);
      isUsernameEmpty = false;
    }

    return isUsernameEmpty;

  });

  $('#password').on("change keyup", function(evt){

    // Could refactor here and make a function to check if field is empty but yeh this will do for now
    var $password = $('#password');
    var isPasswordEmpty = false

    if ($password.val() == ''){
      writeError($password, 'This field is required.');
      isPasswordEmpty = true;
    } else {
      clearError($password);
      isPasswordEmpty = false;
    }

    return isPasswordEmpty;

  });

  $('#username').blur(function(evt){

    var $username = $('#username');
    var validUsername = false;

    if ($username.val() != ""){
      $.ajax("/ajax/signin_username", {
        async:false,
        datatype: "json",
        type: "post",
        data: {username: $username.val()
        }, success: function(data){
            if (data.username_exists){
              validUsername = true;
              clearError($username)
              $login_button.attr('disabled', false);
            } else {
              validUsername = false;
              writeError($username, "Username cannot be found in database.");
              $login_button.attr('disabled', true);
            }
        }, failure: function(){
          alert("Failed to ajax. Check your internet connection.")
        }
      });
    } else {
      writeError($username, 'This field is required.');
      validUsername = false;
    }

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
