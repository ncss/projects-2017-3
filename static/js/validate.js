$(document).ready(function(){

  $(".username").blur(function(){
    alert("Username field has lost focus"); // this doesn't get triggered
    //return validateUsername();
  });

  $('.submit').click(function(evt){
     return validateSignupForm();
  });

       return validateForm();
  $('.post_submit').click(function(evt){
    return validatePost();
  });



  function isPresent($input) {
    if ($input.val().length < 4) {
      $input.parent()
        .find('.error')
        .text('At least four characters are required in this field.')
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
        .text('This is not a valid email address.')
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

  function validateUsername() {

    var $form = $('form.sign-in');
    $('.error').html("");

    var $username = $form.find('.username');
    var validUsername = isPresent($username) && isValidName($username);
    return validUsername

  }

  function validateSignupForm() {
    var $form = $('form.sign-in');
    $('.error').html("");

    var $username = $form.find('.username');
    var $nickname = $form.find('.nickname');
    var $password = $form.find('.password');
    var $email = $form.find('.email');

    var validUsername = isPresent($username) && isValidName($username);
    //var validUsername = validateUsername()
    var validNickname = isPresent($nickname) && isValidName($nickname);
    var validPassword = isPresent($password);
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
    } else {
      return false;
    }
  }
});
