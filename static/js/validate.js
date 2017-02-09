ERROR_TIME = 600;
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
    }
    return false;
  } else {
    return true;
  }
}

function validateSignupForm() {
    var $form = $('form.sign-up');

    var $username = $form.find('#username');
    var $nickname = $form.find('#nickname');
    var $password = $form.find('#password');
    var $password_again = $form.find('#password-check')
    var $email = $form.find('#email');

    var validUsername = checkIfPresent($username) && validateName($username);
    var validNickname = checkIfPresent($nickname) && validateName($nickname);
    var validPassword = validatePassword($password) && validatePasswordRepeat($password, $password_again);
    var validEmail = checkIfPresent($email) && validateEmail($email);


    document.getElementById("webcam-input").value = document.querySelector("#webcam-canvas").toDataURL("image/png");
    
    return Boolean(validUsername && validNickname && validPassword && validEmail);
}


function validateName($input, do_write) {
  var do_write = isUndefined(do_write) ? true : do_write;
  var nameReg = /^[A-Za-z0-9]+$/;
  if (!nameReg.test($input.val())) {
    if(do_write){
      writeError($input, 'Usernames and nicknames can only contain letters and numbers.');
    }
    return false;
  } else {
    clearError($input);
    return true;
  }
}

function validatePassword($input, do_write){
  var do_write = isUndefined(do_write) ? true : do_write
  if ($input.val().length < 8) {
    if (do_write){
      writeError($input, 'At least eight characters are required in this field.')
      return false;
    }
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

function showLoading($input){
  // put code here that shows a loading screen
  console.log("hey");
}

function checkEmpty($input){
  return $input.val() !== '';
}



$(document).ready(function(){

  var username_valid;
  var username_timer;
  $("#username").on("input propertychange", function(){
    // check if the username is correct
    var $form = $('form.sign-up');
    var $username = $form.find('#username');
    
    clearError($username);


    if (!isUndefined(username_timer)){
      clearTimeout(username_timer);
    }


    // check if the username is correct
    // clear the stuff
    username_valid = checkEmpty($username, false)

    if (username_valid){
      if(!validateName($username, false)){
        username_timer = setTimeout(function(){validateName($username, true)}, ERROR_TIME);
        username_valid = false;
      }
    }


    if (username_valid){
      if(!checkIfPresent($username, false)){
        username_timer = setTimeout(function(){checkIfPresent($username, true)}, ERROR_TIME);
        username_valid = false;
      }
    }



    if (username_valid){ //only ajax if needed
      username_valid = false; // set it to false until proven true!
      $.ajax("/ajax/user_validate", {
        datatype: "json",
        type: "post",
        data: {username: $username.val()}, 
        success: 
          function(data){
            if(!data.user_valid){
              // set the timer
              username_timer = setTimeout(
                function(){
                  $username.parent().find(".error").html("This username is already taken! Click here to <a href=\"/signin\">login</a> or <a>here</a> to reset password (WIP)"); 
                }, 
                ERROR_TIME);
            }
            else{
              username_valid = true;
            }
          }, 

        failure:
          function(){
            alert("failed to ajax! Check your internet connection");
          }
      }); 
    }
  });
    

  var nickname_valid=false;
  var nickname_timer;
  $("#nickname").on("input propertychange", function(){
    var $form = $('form.sign-up');
    var $nickname = $form.find('#nickname');
    // reset the vars
    clearError($nickname);
    nickname_valid = false;

    function checkNick(do_write)
    {
      return checkIfPresent($nickname, do_write) && validateName($nickname, do_write);
    }

    if (!isUndefined(nickname_timer))
    {
      clearTimeout(nickname_timer);
    }

    if (!checkNick(false) && $nickname.val() !== '')
    {
      nickname_timer = setTimeout(function(){checkNick(true);}, ERROR_TIME);
    }
    else{
      nickname_valid = true;
    }
  });

  var password_valid = false;
  var password_timer;

  $("#password").on("input propertychange", function(){
    var $form = $('form.sign-up');
    var $password = $form.find('#password');
    // reset the vars
    clearError($password);
    password_valid = false;
    // guilty unless proven innocent!!!!

    function checkPass(do_write){
      return validatePassword($password, do_write);
    }

    if (!isUndefined(password_timer))
    {
      clearTimeout(password_timer);
    }

    if (!checkPass(false) && $password.val() !== '')
    {
      password_timer = setTimeout(function(){checkPass(true);}, ERROR_TIME);
    }
    else{
      password_valid = true;
    }

  });

  var password_a_valid = false;
  var passward_a_timer;
  $("#password-check").on("input propertychange", function(){
    var $form = $('form.sign-up');

    var $password = $form.find('#password');
    var $password_repeat = $form.find('#password-check');
    clearError($password_repeat);

    function checkPassA(do_write){
      isValidPass = validatePassword($password, do_write)  && validatePasswordRepeat($password, $password_repeat,do_write);
      // eval all the terms!
      return isValidPass;
    };

    if (!isUndefined(passward_a_timer))
    {
      clearTimeout(passward_a_timer);
    }

    if (!checkPassA(false) && ($password_repeat.val() !== '' ||  $password.val() !== ''))
    {
      passward_a_timer = setTimeout(function(){checkPassA(true);}, ERROR_TIME);
      password_a_valid = false;
    }
    else{
      password_a_valid = true;
    }

  });

  var email_timer;
  var email_valid = false;

  $('#email').on("input propertychange", function(){
    var $form = $('form.sign-up');

    var $email = $form.find('#email');
    var isValidEmail = checkIfPresent($email) && validateEmail($email);
    
    clearError($email);

    if (!isUndefined(email_timer)){
      clearTimeout(email_timer);
    }

    // check if the username is correct
    email_valid = checkEmpty($email, false);

    //var isValidEmail = checkIfPresent($email) && validateEmail($email);

    if (email_valid){
      if(!validateEmail($email, false)){
        email_timer = setTimeout(function(){validateEmail($email, true)}, ERROR_TIME);
        email_valid = false;
      }
    }

    if (email_valid){
      if(!checkIfPresent($email, false)){
        email_timer = setTimeout(function(){checkIfPresent($username, true)}, ERROR_TIME);
        email_valid = false;
      }
    }

    if (email_valid){ //only ajax if needed
      email_valid = false; // set it to false until proven true!
      $.ajax("/ajax/email_validate", {
        datatype: "json",
        type: "post",
        data: {email: $email.val()}, 
        success: 
          function(data){
            if(!data.email_valid){
              // set the timer
              alert(data.email_valid);
              email_timer = setTimeout(
                function(){
                  $email.parent().find(".error").html("This email is already registered. Click here to <a href=\"/signin\">login</a> or <a>here</a> to reset password (WIP)"); 
                }, 
                ERROR_TIME);
            }
            else{
              email_valid = true;
            }
          }, 

        failure:
          function(){
            alert("failed to ajax! Check your internet connection");
            email_valid = false;
          }
      }); 
    }
  }); 

  $('.sign_up_submit').click(function(evt){
    return validateSignupForm();
  });

  $('.post_submit').click(function(evt){
    return validatePost();
  });
});
