$(document).ready(function(){
/*
  $('.submit').click(function(evt){
    evt.preventDefault();
    validateForm();
  });
*/
function isPresent($input) {
  if ($input == "") {

  }
}

function validateForm() {

    var nameReg = /^[A-Za-z]+$/
    var usernameReg = /^[A-Za-z]+$/
    var nicknameReg = /^[A-Za-z]+$/
    var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;

    var username = $('.username').val();
    var nickname = $('.nickname').val();
    var password = $('.password').val();
    var email = $('.email').val();

    if (username.length < 8 ) {

    }


}
});
