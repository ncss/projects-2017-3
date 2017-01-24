$(document).ready(function(){

  // The blur event is for when a selector has lost focus
  $("#username").blur(function(){
    var $form = $('form.sign-in');
    var $username = $form.find('#username');
    var isValidUsername = checkIfPresent($username) && validateName($username);

    $.ajax("/ajax/user_validate", {datatype: "json", type: "post", data: {username: $username.val()},
        success: function(data){
            alert(data.user_valid)
            if(!data.user_valid){
                 $username.parent()
                    .find('.error')
                    .text('This username is already taken!')
            }
        }
        });
    if (isValidUsername) {
      return true;
    } else {
      return false;
    }
  });

  $("#nickname").blur(function(){

    var $form = $('form.sign-in');

    var $nickname = $form.find('#nickname');
    var isValidNickname =  checkIfPresent($nickname) && validateName($nickname);

    if (isValidNickname) {
      return true;
    } else {
      return false;
    }

  });

  $("#password").blur(function(){

    var $form = $('form.sign-in');

    var $password = $form.find('#password');
    var isValidPassword = validatePassword($password);

    if (isValidPassword) {
      return true;
    } else {
      return false;
    }

  });

  $('#email').blur(function(){

    var $form = $('form.sign-in');

    var $email = $form.find('#email');
    var isValidEmail = checkIfPresent($email) && validateEmail($email);

    if (isValidEmail) {
      return true;
    } else {
      return false;
    }

  });

  $('.sign_up_submit').click(function(evt){
    return validateSignupForm();
  });

  $('.post_submit').click(function(evt){
    return validatePost();
  });

  function checkIfPresent($input) {
    if ($input.val().length < 4) {
      $input.parent()
        .find('.error')
        .text('At least four characters are required in this field')
      return false;
    } else {
      $input.parent()
        .find('.error')
        .text('')
      return true;
    }
  }

  function validateEmail($input) {
    var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
    if (!emailReg.test($input.val())) {
      $input.parent()
        .find('.error')
        .text('This is not a valid email address format')
      return false;
    } else {
      $input.parent()
        .find('.error')
        .text('')
      return true;
    }
  }

  function validateName($input) {
    var nameReg = /^[A-Za-z0-9]+$/;
    if (!nameReg.test($input.val())) {
      $input.parent()
        .find('.error')
        .text('Usernames and nicknames can only contain letters and numbers.')
      return false;
    } else {
      $input.parent()
        .find('.error')
        .text('')
      return true;
    }
  }

  function validatePassword($input){
  if ($input.val().length < 8) {
      $input.parent()
        .find('.error')
        .text('At least eight characters are required in this field.')
      return false;
    } else {
      $input.parent()
        .find('.error')
        .text('')
      return true;
    }
  }



  function validateSignupForm() {
    var $form = $('form.sign-in');
    $('.error').html("");

    var $username = $form.find('#username');
    var $nickname = $form.find('#nickname');
    var $password = $form.find('#password');
    var $email = $form.find('#email');

    var validUsername = checkIfPresent($username) && validateName($username);
    var validNickname = checkIfPresent($nickname) && validateName($nickname);
    var validPassword = validatePassword($password);
    var validEmail = checkIfPresent($email) && validateEmail($email);

    if (validUsername && validNickname && validPassword && validEmail) {
      return true;
    } else {
      return false;
    }
  }

  function validatePost() {
    $('.error').html("");

    var $question = $('.ask_question')

    var validQuestion = checkIfPresent($question);

    if (validQuestion) {
      return true;
    }else {
      return false;
    }
  }
});
