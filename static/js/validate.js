$(document).ready(function(){

  $("#username").blur(function(){

    var $form = $('form.sign-in');
    $('.error').html("");

    var $username = $form.find('.username');
    var isValidUsername = validateName($username);

    if (isValidUsername) {
      return true;
    } else {
      return false;
    }
  });

  $("#nickname").blur(function(){

    var $form = $('form.sign-in');
    $('.error').html("");

    var $nickname = $form.find('.nickname');
    var isValidNickname = validateName($nickname);

    if (isValidNickname) {
      return true;
    } else {
      return false;
    }

  });

  $("#password").blur(function(){

    var $form = $('form.sign-in');
    $('.error').html("");

    var $password = $form.find('.password');
    var validPassword = isValidPassword($password);

    if (validPassword) {
      return true;
    } else {
      return false;
    }

  });

  $('#email').blur(function(){

    var $form = $('form.sign-in');
    $('.error').html("");

    var $email = $form.find('.email');
    var validEmail = isPresent($email) && isValidEmail($email);

    if (validEmail) {
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

  function isPresent($input) {
    if ($input.val().length < 4) {
      $input.parent()
        .find('.error')
        .text('At least four characters are required in this field')
      return false;
    } else {
      return true;
    }
  }

  function isValidEmail($input) {
    var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
    if (!emailReg.test($input.val())) {
      $input.parent()
        .find('.error')
        .text('This is not a valid email address')
      return false;
    } else {
      return true;
    }
  }

  function isValidName($input) {
    var nameReg = /^[A-Za-z0-9]+$/;
    if (!nameReg.test($input.val())) {
      $input.parent()
        .find('.error')
        .text('Usernames and nicknames can only contain letters and numbers.')
      return false;
    } else {
      return true;
    }
  }

  function isValidPassword($input){
  if ($input.val().length < 8) {
      $input.parent()
        .find('.error')
        .text('At least eight characters are required in this field.')
      return false;
    } else {
      return true;
    }
  }



  function validateSignupForm() {
    var $form = $('form.sign-in');
    $('.error').html("");

    var $username = $form.find('.username');
    var $nickname = $form.find('.nickname');
    var $password = $form.find('.password');
    var $email = $form.find('.email');

    var validUsername = isPresent($username) && isValidName($username);
    var validNickname = isPresent($nickname) && isValidName($nickname);
    var validPassword = isValidPassword($password);
    var validEmail = isPresent($email) && isValidEmail($email);

    if (validUsername && validNickname && validPassword && validEmail) {
      return true;
    } else {
      return false;
    }
  }

  function validatePost() {
    $('.error').html("");

    var $question = $('.ask_question')

    var validQuestion = isPresent($question);

    if (validQuestion) {
      return true;
    }else {
      return false;
    }
  }
});
