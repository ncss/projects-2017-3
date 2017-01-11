$(document).ready(function(){

  $('.submit').click(function(evt){
      return validateForm();
  });

function isPresent($input) {
  if ($input.val().length < 8) {
    $input.parent().find('.error').text('this field is not long enough')
  }
}

function isValidEmail($input) {
  debugger
  var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
  if (!emailReg.test($input)) {
    $input.parent().find('.error').text('the email address you entered is not a valide email address')
  }
}

function isValidName($input) {
  var nameReg = /^[A-Za-z0-9]+$/;
  if (!nameReg.test($input)) {
    $input.parent().find('.error').text('the name you entered for this field is invalid. Note that usernames and nicknames can only contain letters and numbers.')
  }
}



function validateForm() {

    var $username = $('.username')
    var $nickname = $('.nickname')
    var $password = $('.password')
    var $email = $('.email')

    var validUsername = isPresent($username) && isValidName($username);
    var validNickname = isPresent($nickname) && isValidName($username) ;
    var validPassword = isPresent($password);
    var validEmail = isPresent($email) && isValidEmail$(email);

    if (validUsername && validNickname && validPassword && validEmail) {
      return true;
    }

    else {
      return false;
    }

}
});
