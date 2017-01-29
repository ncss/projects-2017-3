function writeError($input, text){
    $input.parent().find(".error").text(text)
}
function clearError($input){
    $input.parent().find(".error").text('')
}


$(document).ready(function(){

  var $form = $('form.post-comment');
  var $comment_field = $('#addComment');
  var $submit_button = $('.comment_submit')

  var isLoggedIn = false

  $.ajax("/ajax/logged_in_validate", {datatype: "json", type: "post", data: {},
      success: function(data){
        if(!data.is_logged_in){
          $comment_field.attr('disabled', true);
          $comment_field.attr('placeholder', "You will need to sign in or sign up to be able to post your comment.")
          $submit_button.attr('disabled', true);
          isLoggedIn = false;
        } else {
          clearError($comment_field);
          $comment_field.attr('disabled', false);
          $comment_field.attr('placeholder', "Enter your response here.")
          $submit_button.attr('disabled', false);
          isLoggedIn = true;
        }
      },
      failure: function(){
        alert("failed to ajax. This can be caused by network issues.");
      }
  });

  return Boolean(isLoggedIn);

});
