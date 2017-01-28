function writeError($input, text){
    $input.parent().find(".error").text(text)
}
function clearError($input){
    $input.parent().find(".error").text('')
}


$(document).ready(function(){

  var $form = $('form.post-comment');
  var $comment_field = $('#addComment');
  var $submit_button = $('#comment_submit')

  var isLoggedIn = false

  $.ajax("/ajax/logged_in_validate", {datatype: "json", type: "post", data: {}, // pass in {empty} or pass in cookie? or is that already done in request
      success: function(data){
        if(!data.is_logged_in){
          writeError($comment_field, "You will need to <a href=\"/signin\">sign in</a> or <a href=\"/signup\">sign up</a> to be able to post your comment.");
          $comment_field.disabled = true
          $submit_button.disabled = true
          alert('User not logged in')
          isLoggedIn = false;
        } else {
          clearError($comment_field);
          $comment_field.disabled = false
          $submit_button.disabled = false
          isLoggedIn = true;
          alert('User is logged in')
        }
      },
      failure: function(){
        alert("failed to ajax");
      }
  });

  return Boolean(isLoggedIn);

});
