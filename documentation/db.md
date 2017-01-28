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
User.sign_up('username', 'password', 'nickname', 'email')
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
User.find(1) # Find by an ID in the database
User.find(username="username") #Use optional username if you have the username instead
```
Both return a `User` object if the user exists, otherwise `None`

*The below are instance methods (they require you to have an `User` object to call them)*
### Create a Post on behalf of a User
To create a `Post` on behalf of a `User`:
```python
user.create_post('user_id', 'description', 'title', 'photo_file')
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
user.find_post(1) # The Post ID
```
Returns a `Post` object

### Create a Comment on behalf of a User
To create a `Comment` on behalf of a `User`:
```python
user.create_comment(post<Post>, 'text', 'date', 1)
# Last parameter is the parent ID of the comment. Specify `None` if comment has no parent
```
Returns a `Post` object

### Edit a User
To edit a `User`'s details:
```python
user.edit('password', 'nickname', 'email', 'gender', 'dob', 'bio', 'filename.jpg')
```
Returns a `User` object

### Properties
The `User` object has some properties:
```python
id, username, password, nickname, email, gender, dob, bio, picture, creation_date
```
`picture` is path of the `User`'s profile pic. Example of what it should have: `os.path.join('static', 'uploads', 'user_image', User.id +'.jpg')`

---

## Posts
The `Post` object manipulates posts inside of the database. Similar to the `User` object in terms of initialisation. Remember creation is done on behalf of the `User`.

### Find a Post
To find a `Post`:
```python
Post.find(1) # The ID of a Post
```
Returns a `Post` object

### Get all Posts
To get all `Post`s, or to get all `Post`s by a user:
```python
Post.find_all() 	# Gets every post out there
Post.find_all(1) 	# Gets every post by a user with an ID
```
Returns an array of `Post` objects


### Delete a Post
To delete a `Post`:
```python
Post.delete(1) # 1st parameter is the post ID
```

*The below are instance methods (they require you to have an `Post` object to call them)*
### Get all the comments on a Post
To get all the comments on a `Post`:
```python
post.all_comments()
```
Returns an array of `Comment` objects

### Find a specific comment
To find a comment on a `Post`:
```python
post.find_comment(1) # 1st parameter is the comment ID
```
Returns a `Comment` object

### Properties
The `Post` object has some properties:
```python
id, user, description, title, date, file
```

---
## Comments
The `Comment` object manipulates comments inside of the database. Similar to the above classes in terms of initialisation. Remember creation is done on behalf of the `User`, using the `Post` object as well. ^\_^

### Creating comments
This allows you to create a new comment object:
```python
Comment.create(user_id, post_id, text, date[, parent_id, loc_latitude, loc_longitude, score])
```
Everything inside the square brackets is optional.

### Finding comments
There are a variety of ways on finding comments. Those ways are expressed in the function name:
```python
Comment.find(1) 					    # 1st parameter is the comment ID
Comment.find_comments_for_post_id(1)	# 1st parameter is the post ID
Comment.find_comments_for_user(1)	   # 1st parameter is the user ID
```
`Post.find` returns a `Comment` object. The others return an array of `Comment` objects.

### Find children
To find children comments on a comment:
```python
Comment.find_children_for_comment(1) # 1st parameter is the comment ID
```
Returns an array of `Comment` objects

### Edit a comment
To edit a comment:
```python
Comment.edit_comment_with_id(1, "new_text") # 1st parameter is the comment ID
```
Returns a `Comment` object

### Properties
The `Comment` object has some properties:
```python
id, user_id, post_id, text, date[, parent_id, loc_latitude, loc_longitude, score]
```

---
Author: George Dan | [github](https://github.com/ninjaprawn) | [Twitter](https://twitter.com/theninjaprawn)
