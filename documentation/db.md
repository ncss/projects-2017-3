# Database!
---
**NOTE:** This is subject to change (most likely will happen, sorry)
## Importing
Importing the render function:
```python
from db.db_api import User, Post, Comment
```
When importing the database module, the database file is automatically opened, so you don't need to worry about that :)

---
## Users

The `User` object manipulates users inside the database, as well as some other things like posts. Instead of using the ```__init__``` method, you will be using the static methods listed below to get a `User` object (most of the time).

### Sign up
To sign up a user, you will need a username, password, nickname, email and creation_time:
```python
User.sign_up('username', 'password', 'nickname', 'email', 'creation_time')
```
A `User` object is returned
### Sign In
To sign in a user:
```python
User.login('username', 'password')
```
This will return the ID of a user if the user exists, otherwise `None` is returned.

### Find a User
There are multiple ways for finding a `User` in the database:
```python
User.find(0) # Find by an ID in the database
User.find_by_username("username")
```
Both return a `User` object if the user exists, otherwise `None`

*The below are instance methods (they require you to have an `User` object to call them)*
### Create a Post on behalf of a User
To create a `Post` on behalf of a `User`:
```python
user.create_post('description', 'title', 'date', ['file1.jpg', 'file2.jpg'])
```
Returns a `Post` object

### List all posts by a User
To get all the posts created by a `User`:
```python
user.all_posts()
```
Returns an array of `Post` objects

### Get a specific post
To get a specific `Post`:
```python
user.find_post(0) # The Post ID
```
Returns a `Post` object

### Create a Comment on behalf of a User
To create a `Comment` on behalf of a `User`:
```python
user.create_comment(post<Post>, 'text', 'date', 0)
# Last parameter is the parent ID of the comment. Specify `None` if comment has no parent
```
Returns a `Post` object

### Edit a User
To edit a `User`s details:
```python
user.edit('password', 'nickname', 'gender', 'dob', 'bio', 'filename.jpg')
```
Returns a `Post` object

---

## Posts

Content inside a pair of `{% if %}` and `{% end if %}` tags is only generated if the python expression inside the `{% if expression %}` clause returns true.

```html
{% if expression %}
<p>code if expresion is true</p>
{% end if %}
```
### Else Clause
Optionally, you are able to add a third tag into the if statement that renders the HTML content inside it if the if expression evaluates to False.

```html
{% if expression %}
  <p>code if expresion is true</p>
{% else %}
  <p>code if expresion is false</p>
{% end if %}
```

Note that `else if` or `elif` statements are not supported.

---
## Include Statements
Include statements allow you to include sections of HTML in several files.

File `header.html`:
```html
<h1>This is a header!</h1>
```

File `login.html`:
```html
{% include header.html %}
<form>
  <input type='text'>
  <input type='submit'>
</form>
```
When rendered, `login.html` will become:
```html
<h1>This is a header!</h1>
<form>
  <input type='text'>
  <input type='submit'>
</form>
```
---
## For Statements
For statements iterate through an iterable expression, passing the content returned from the iterable into an iterator variable. These iterator variables can be referenced locally using normal `{{ x }}` expression syntax.

This HTML:
```html
{% for i in range(5) %}
  <p>Your number is {{ i }}!</p>
{% end for %}
```
Becomes:
```html
<p>Your number is 0!</p>
<p>Your number is 1!</p>
<p>Your number is 2!</p>
<p>Your number is 3!</p>
<p>Your number is 4!</p>
```

You may also pass contextual variables to the for statement:
```python
parser.render('some_template.html', {'array': ['hello', 'world']})
```
```html
{% for i in array %}
  <p>{{ i }}</p>
{% end for %}
```
Becomes:
```html
<p>Hello</p>
<p>World</p>
```
---
## Comment Statements
Content inside a pair of `{% comment %}` and `{% end comment %}` tags is ignored and taken out of the HTML.
```html
<p>
  Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut ipsum nisi, placerat eu felis vitae, consequat elementum justo.
<p>
<p>
   Curabitur tellus felis, varius ac quam non, malesuada volutpat turpis. Nulla auctor porttitor sagittis. Aliquam quis dictum nulla.
</p>
  {% comment %}
    Can someone change this placeholder text?
  {% end comment %}
<p>
  Vivamus a condimentum metus. Vestibulum tempor erat a rhoncus tristique. Integer blandit nisi sit amet felis ultricies, et gravida est elementum. Praesent tincidunt purus semper, lacinia lectus sed, tincidunt nibh.
</p>
<p>
  Nulla facilisi. Nam luctus, lacus a bibendum tincidunt, purus magna malesuada felis, eget condimentum leo diam eu justo.
</p>
```

---
Author: George Dan | [github](https://github.com/ninjaprawn) | [Twitter](https://twitter.com/theninjaprawn)
