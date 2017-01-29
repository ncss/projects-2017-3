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

});
