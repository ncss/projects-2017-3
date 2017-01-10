/*
Validate user input

- sign up page
  * check for presence of:
    * username
    * nickname
    * password
    * email
  * check for validation of:
    * password (is it more than 8 characters?)
    * email (does it meet standard email address requirements)
      Validating email addresses is notoriously difficult.
      Read about it here: http://stackoverflow.com/a/1373724/863846
      Implement this (comparatively simple) version: http://stackoverflow.com/a/9204568/863846

- sign in page
  * check for presence of:
    * username
    * password

- ask question page
  * check for presence of:
    * question
    * description
    * file (see http://stackoverflow.com/questions/46219/how-to-determine-if-user-selected-a-file-for-file-upload)

HINT
When _shared_head has been committed and synced do the following:
- Add
    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
  to _shared_head so you automatically get jquery on every page

- add THIS file to _shared_head so it automatically gets included on every page


*/

/*
isPresent Notes
- Read through the sudo code below and then come back to read these notes
- Starting variables with a "$" is convention to signify that it is a jQuery element.
  Something like $('body') might be referenced as $element
- to get an input's value use http://api.jquery.com/val/
- To display an error message you need to add a <span> (or <div> or <p>) below the input.
  (http://api.jquery.com/insertafter/)
- This new element should have class "error".
  (https://api.jquery.com/addclass/)
- You can add any text you want (something like "this field is required")
- Add a tiny bit of styling to make the error text red
- Remove the element
  https://api.jquery.com/remove/
*/
function isPresent($input) {
  // get the input's value
  // if no value is present
    // display an error message below the input
    // return false
  // otherwise
    // remove the error message (it might not be there)
    // return true
}

/*
isLongEnough Notes
- Reference http://stackoverflow.com/questions/2702862/jquery-check-length-of-input-field
*/
function isLongEnough($input) {
  // get the input's value
  // if length of input's value < 8
    // display an error message below the input
    // return false
  // otherwise
    // remove the error message (it might not be there)
    // return true
}

/*
isValidEmail Notes
- Reference http://stackoverflow.com/a/9082446/863846
*/
function isValidEmail($input) {
  // get the input's value
  // if the email does *not* pass the regex test
    // display an error message below the input
    // return false
  // otherwise
    // remove the error message (it might not be there)
    // return true
}

/*
isValidForm Notes
- Since each of the above functions take care of displaying error messages
  we don't need to worry about it here
*/
function isValidForm($form) {
  // assign a variable for each of the form's input elements
  var $username =
  var $nickname =
  var $password =
  var $email =

  var validUsername = isPresent($username);
  var validNickname = isPresent($nickname);
  var validPassword = isPresent($password) && isLongEnough($password);
  var validEmail = isPresent($email) && isValidEmail($email);
  // if validUsername && validNickname && validPassword && validEmail
    // return true
  // otherwise
    // return false
}


/*
Submit handler notes
- Reference http://stackoverflow.com/a/17828644/863846
*/
$('SELECTOR').submit(function(event) {
  return isValidForm($('SELECTOR'))
})







