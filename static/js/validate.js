function writeError($input, text){
    $input.parent().find(".error").text(text)
}
function clearError($input){
    $input.parent().find(".error").text('')
}

function validateEmail($input) {
    var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
    if (!emailReg.test($input.val())) {
      writeError($input, 'This is not a valid email address format')
      return false;
    } else {
      clearError($input)
      return true;
    }
  }

function checkIfPresent($input) {
  if ($input.val().length < 4) {
    writeError($input, 'At least four characters are required in this field')
    return false;
  } else {
    clearError($input)
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

    return Boolean(validUsername && validNickname && validPassword && validEmail);
}

function validateName($input) {
  var nameReg = /^[A-Za-z0-9]+$/;
  if (!nameReg.test($input.val())) {
      writeError($input, 'Usernames and nicknames can only contain letters and numbers.')
      return false;
  } else {
      clearError($input)
    return true;
  }
}

function validatePassword($input){
  if ($input.val().length < 8) {
      writeError($input, 'At least eight characters are required in this field.')
      return false;
    } else {
      clearError($input)
      return true;
  }
}

function validatePost(){
    var $question = $('.ask_question')

    var validQuestion = checkIfPresent($question);
    return Boolean(validQuestion);
}



$(document).ready(function(){
  // The blur event is for when a selector has lost focus
  $("#username").on("change paste keyup", function(){
    var $form = $('form.sign-in');

    var $username = $form.find('#username');
    var isValidUsername = checkIfPresent($username) && validateName($username);

    $.ajax("/ajax/user_validate", {datatype: "json", type: "post", data: {username: $username.val()},
        success: function(data){
          if(!data.user_valid){
            writeError($username, "This username is already taken!");
            isValidUsername = false;
          }
        },
        failure: function(){
          alert("failed to ajax");
        }
    });
    return Boolean(isValidUsername);
    // Boolean converts a value into true or false.
  });


  $("#nickname").on("change paste keyup", function(){
    var $form = $('form.sign-in');
    var $nickname = $form.find('#nickname');
    var isValidNickname =  checkIfPresent($nickname) && validateName($nickname);
    return Boolean(isValidNickname);
  });


  $("#password").on("change paste keyup", function(){
    var $form = $('form.sign-in');

    var $password = $form.find('#password');
    var isValidPassword = validatePassword($password);

    return Boolean(isValidPassword);
  });


  $('#email').on("change paste keyup", function(){
    var $form = $('form.sign-in');

    var $email = $form.find('#email');
    var isValidEmail = checkIfPresent($email) && validateEmail($email);

    return Boolean(isValidEmail);
  });

  $('.sign_up_submit').click(function(evt){
    return validateSignupForm();
  });

  $('.post_submit').click(function(evt){
    return validatePost();
  });
});
