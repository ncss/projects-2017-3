/*

HINT
add this file to _shared_head so it automatically gets included on every page

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

*/