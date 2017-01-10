# Frontend Todos

## Committing notes
- Do NOT commit until you've shown your work to someone else
- Take turns to commit after each part:
  + Sync before committing
  + check your work (show it to someone!)
  + Commit
  + Sync after committing
  + Tell the next person it's their turn to commit

## Part one

- **Courtney** Look for this line in templates/signup.html:
  ```
  <form action="/signup" method="post" enctype = "multipart/form-data">
  ```
  add a similar line to templates/signin.html to POST the data to the backend
- **Rachel** Follow instructions in templates/_shared_head.html
- **Sarah (Courtney join when finished)** Follow instructions in static/css/base.css
- **Jack** Follow instructions in static/js/site.js

## Part two

- **Jack** Continue with static/js/site.js
- **Sarah & Rachel** Include template/_nav_bar.html on every page
- **Courtney** Add Sarah's logo to the nav bar
  * image should go in static/images
  * HTML for image should go in templates/_nav_bar.html
  * look in templates/index.html for example of an <img/> element

## Part three

This is the least important, if anyone gives you work during the day it's probably more important. Skip this as needed!

- Check styling of the nav bar on every page, make adjustments to static/css/_nav_bar.css as needed
- add more styling to base.css
  * do links look good?
    - You can remove the underline with this styling: http://stackoverflow.com/a/10853894/863846
    - You can make them a different color with { color: red; }
    - You can change the color (or any style) when the user hovers with http://www.w3schools.com/cssref/sel_hover.asp
  * Is there enough spacing around the words?
    - Try adding margin and/or padding
  * Do any elements need a border or more space around them?