function writeError($input, text){
    $input.parent().find(".error").text(text)
}
function clearError($input){
    $input.parent().find(".error").text('')
}


$(document).ready(function(){
  // The blur event is for when a selector has lost focus
  $("#addComment").on("change keyup", function(){
    var $form = $('form.post-comment');
    var $comment_field = $('#addComment');
    var $submit_button = $('#comment_submit')

    var isLoggedIn = false

    $.ajax("/ajax/logged_in_validate", {datatype: "json", type: "post", data: {}, // pass in {empty} or pass in cookie? or is that already done in request
        success: function(data){
          if(!data.user_is_logged_in){

            writeError($comment_field, "You will need to log in or sign up to be able to post your comment.");
            // make Submit and textarea disabled
            $comment_field.disabled = true
            

            isLoggedIn = false;
          }
          else {
            clearError($comment_field);
            // enable Submit and textarea
          }
        },
        failure: function(){
          alert("failed to ajax");
        }
    });
    return Boolean(isLoggedIn);
  });
});
