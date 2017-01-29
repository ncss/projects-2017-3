function writeError($input, text, do_write){
  $input.parent().find(".error").text(text);
}

function clearError($input){
  var $form = $('form.sign-in');
  $input.parent().find(".error").text('');
}

function isUndefined(input){
  return typeof input === 'undefined';
}

function setStateLoginButton(isUsernameEmpty, isPasswordEmpty){

  var $form = $('form.sign-in');
  var $login_button = $('.login_button');

  var $username = $('#username');
  var isUsernameEmpty = !checkIfPresent($username);

  var $password = $('#password');
  var isPasswordEmpty = !checkIfPresent($password);

  var fieldsAreFilled = !isUsernameEmpty && !isPasswordEmpty;
  if (fieldsAreFilled){
    $login_button.attr('disabled', false);
  } else {
    $login_button.attr('disabled', true);
  }
  return fieldsAreFilled;
}

function checkIfPresent($input) {

  if ($input.val().length < 1) {
    return false;
  } else {
    clearError($input)
    return true;
  }
}

function setErrorMessageIfEmpty($input) {
  if (checkIfPresent($input)){
    clearError($input)
  } else {
    writeError($input, 'This field is required.')
  }
  return;
}

$(document).ready(function(){

  var $form = $('form.sign-in');
  var $login_button = $('.login_button');
  $login_button.attr('disabled', true);
  var isUsernameEmpty = true;
  var isPasswordEmpty = true;

  $('#username').on("change keyup blur", function(evt){
    var $username = $('#username');
    setErrorMessageIfEmpty($username);
    return setStateLoginButton();
  });

  $('#password').on("change keyup blur", function(evt){
    var $password = $('#password');
    setErrorMessageIfEmpty($password);
    return setStateLoginButton();
  });

});
