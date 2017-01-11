$(document).ready(function(){

  $('.submit').click(function(evt){
       // return validateForm();
  });

  $('.post_submit').click(function(evt){
      //return validatePost();
  });

function isPresent($input) {
  if ($input.val().length < 4) {
    $input.parent().find('.error').text('this field is not long enough')
    return false;
  }

  else {
    return true;
  }
}

function isValidEmail($input) {
  var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
  if (!emailReg.test($input.val())) {
    $input.parent().find('.error').text('the email address you entered is not a valid email address')
    return false;
  }
  else {
    return true;
  }
}

function isValidName($input) {
  var nameReg = /^[A-Za-z0-9]+$/;
  if (!nameReg.test($input.val())) {
    $input.parent().find('.error').text('the name you have entered for this field is invalid. Note that usernames and nicknames can only contain letters and numbers.')
    return false;
  }
  else {
    return true;
  }
}

function isImagePresent($input) {
  if ($input.error()) {
    $input.parent().find('.error').text('you need to upload an image in order to ask a question')
    return false;
  }
  else {
    return true;
  }
}

function isvalidImage($input) {

}



function validateForm() {

    $('.error').html("");

    var $username = $('.username')
    var $nickname = $('.nickname')
    var $password = $('.password')
    var $email = $('.email')

    var validUsername = isPresent($username) && isValidName($username);
    var validNickname = isPresent($nickname) && isValidName($nickname);
    var validPassword = isPresent($password);
    var validEmail = isPresent($email) && isValidEmail($email);

    if (validUsername && validNickname && validPassword && validEmail) {
      return true;
    }

    else {
      return false;
    }

}

  function validatePost() {

    $('.error').html("");

    var $question = $('.ask_question')
    var $image = $('.img_upload')
    var $description = $('.description')

    var validQuestion = isPresent($question);
    var validImage = isImagePresent($image);  //make sure that image is a compatable file type


  }

});
