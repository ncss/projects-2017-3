function writeError($input, text){
    $input.parent().find(".error").text(text)
}
function clearError($input){
    $input.parent().find(".error").text('')
}


$(document).ready(function(){

  var $form = $('form.sign-in');
  var $login_button = $('.login_button');
  $login_button.attr('disabled', true);
  var isUsernameEmpty = true;
  var isPasswordEmpty = true;

  $('#username').on("change keyup blur", function(evt){

    var $username = $('#username');

    if ($username.val() == ''){
      writeError($username, 'This field is required.');
      isUsernameEmpty = true;
    } else {
      clearError($username);
      isUsernameEmpty = false;
    }
    return isUsernameEmpty;
  });

  $('#password').on("change keyup blur", function(evt){

    var $password = $('#password');

    if ($password.val() == ''){
      writeError($password, 'This field is required.');
      isPasswordEmpty = true;
    } else {
      clearError($password);
      isPasswordEmpty = false;
    }
    return isPasswordEmpty;
  });

  $('#username').on("change keyup blur", function(evt){
    var fieldsAreFilled = !isUsernameEmpty && !isPasswordEmpty;
    if (fieldsAreFilled){
      $login_button.attr('disabled', false);
    } else {
      $login_button.attr('disabled', true);
    }
    return fieldsAreFilled;
  });

  $('#password').on("change keyup blur", function(evt){
    var fieldsAreFilled = !isUsernameEmpty && !isPasswordEmpty;
    if (fieldsAreFilled){
      $login_button.attr('disabled', false);
    } else {
      $login_button.attr('disabled', true);
    }
    return fieldsAreFilled;
  });

  $('.login_button').click(function(evt){

    var $username = $('#username');
    var $password = $('#password');

    // Check if username in db
    $.ajax("/ajax/signin_username", {
      async:false,
      datatype: "json",
      type: "post",
      data: {username: $username.val()
      }, success: function(data){
          if (data.username_exists){
            isValidUsername = true;
            clearError($username)
          } else {
            isValidUsername = false;
            writeError($username, "Username cannot be found in database.");
          }
      }, failure: function(){
        alert("Failed to ajax. Check your internet connection.")
      }
    });

    //TODO: Check if the password corresponds to hashed password in db
    // Refer to sign in post handler

    return;
  });

});
