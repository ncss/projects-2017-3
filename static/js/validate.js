$(document).ready(function(){
/*
  $('.submit').click(function(evt){
    validateForm();
  });
*/
function isPresent($input) {
  if ($input.val().length < 8) {
    $input.parent().find('.error').text('your is not long enough')
  }

function isValidEmail($input) {

}


}

function validateForm() {

    var nameReg = /^[A-Za-z]+$/
    var usernameReg = /^[A-Za-z]+$/
    var nicknameReg = /^[A-Za-z]+$/
    var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;

    var $username = $('.username')
    var $nickname = $('.nickname')
    var $password = $('.password')
    var $email = $('.email')

    isPresent($username);




}
});
