function writeError($input, text){
    $input.parent().find(".error").text(text)
}
function clearError($input){
    $input.parent().find(".error").text('')
}

function isUndefined(input){
  return typeof input === 'undefined';
}

// if do_write is not supplied, it will return false, else true
function validateEmail($input, do_write) {
  var do_write = isUndefined(do_write) ? true : do_write
  var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
  if (!emailReg.test($input.val())) {
    if (do_write){
      writeError($input, 'Please enter a valid email address format.');
    }
    return false;
  } else {
    clearError($input);
    return true;
  }
}

function checkIfPresent($input, do_write) {
  var do_write = isUndefined(do_write) ? true : do_write
  if ($input.val().length < 4) {
    if (do_write){
      writeError($input, 'At least four characters are required in this field')
    }
    return false;
  } else {
    clearError($input)
    return true;
  }
}

function validatePasswordRepeat($pass1, $pass2, do_write){
  var do_write = isUndefined(do_write) ? true : do_write
  if ($pass1.val() != $pass2.val()){
    if (do_write){
      writeError($pass1, 'These two passwords do not match!');
      writeError($pass2, 'These two passwords do not match!');
      return false;
    }
  } else {
    clearError($pass1);
    clearError($pass2);
    return true;
  }
}

function validateSignupForm() {
    var $form = $('form.sign-in');

    var $username = $form.find('#username');
    var $nickname = $form.find('#nickname');
    var $password = $form.find('#password');
    var $password_again = $form.find('#password-check')
    var $email = $form.find('#email');

    var validUsername = checkIfPresent($username) && validateName($username);
    var validNickname = checkIfPresent($nickname) && validateName($nickname);
    var validPassword = validatePassword($password) && validatePasswordRepeat($password, $password_again);
    var validEmail = checkIfPresent($email) && validateEmail($email);

    return Boolean(validUsername && validNickname && validPassword && validEmail);
}

function validateName($input) {
  var do_write = isUndefined(do_write) ? true : do_write
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
  $("#username").on("change keyup", function(){
    var $form = $('form.sign-in');

    var $username = $form.find('#username');
    var isValidUsername = checkIfPresent($username) && validateName($username);

    $.ajax("/ajax/user_validate", {datatype: "json", type: "post", data: {username: $username.val()},
        success: function(data){
          if(!data.user_valid){
            writeError($username, "This username is already taken! Click here to <a href=\"/signin\">login</a> or <a>here</a> to reset password (WIP)");
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


  $("#nickname").on("change keyup", function(){
    var $form = $('form.sign-in');
    var $nickname = $form.find('#nickname');
    var isValidNickname =  checkIfPresent($nickname) && validateName($nickname);
    return Boolean(isValidNickname);
  });


  $("#password").on("change keyup", function(){
    var $form = $('form.sign-in');

    var $password = $form.find('#password');
    var $password_repeat = $form.find('#password-check');
    var isValidPassword;
    if($password_repeat.val() != ''){
      isValidPassword = validatePassword($password) && validatePasswordRepeat($password, $password_repeat);
    } else{
      isValidPassword = validatePassword($password);
    }

    return Boolean(isValidPassword);
  });

  $("#password-check").on("change keyup", function(){
    var $form = $('form.sign-in');

    var $password = $form.find('#password');
    var $password_repeat = $form.find('#password-check');
    var isValidPassword;
    if($password_repeat.val() != ''){
      isValidPassword = validatePassword($password) && validatePasswordRepeat($password, $password_repeat);
    } else{
      isValidPassword = validatePassword($password);
    }
    return Boolean(isValidPassword);
  });


  $('#email').on("change keyup", function(){
    var $form = $('form.sign-in');

    var $email = $form.find('#email');
    var isValidEmail = checkIfPresent($email) && validateEmail($email);

     $.ajax("/ajax/email_validate", {datatype: "json", type: "post", data: {email: $email.val()},
       success: function(data){
         if(!data.email_valid){
           $email.parent().find(".error").html("This email is already registered. Click here to <a href=\"/signin\">login</a> or <a>here</a> to reset password (WIP)");
           isValidEmail = false;
         }},
         failure: function(){
           alert("failed to ajax. This can be caused by network issues");
         }
        });
    return Boolean(isValidEmail);
  });

  $('.sign_up_submit').click(function(evt){
    return validateSignupForm();
  });

  $('.post_submit').click(function(evt){
    return validatePost();
  });
});
