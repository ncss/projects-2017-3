from datetime import datetime
import sqlite3
import os

class MissingDatabaseException(Exception): pass

# Because connecting to a db will create the file if it doesn't exist, we need to throw an error so we can have a db with dummy data
if not os.path.isfile("db.db"):
    raise MissingDatabaseException("You're missing the database file! Run `python db/db_create.py` and then run this again!")

with sqlite3.connect('db.db') as conn:
    cur = conn.cursor()
    class CommentNotFoundException(Exception):
        pass

    class UserNotFound(Exception):
        pass

    class PostNotFound(Exception):
        pass

    class User:
        """
        User Object that represents a User, with attributes
        id, username (unique), hashed(password), nickname, email(unique), gender, dobm, short bio, picture(path), and creation_date
        """
        COLS = 'id', 'username', 'password', 'nickname', 'gender', 'dob', 'picture', 'creation_date'
        # all possible columns
        MUTABLE_COLS = 'password', 'nickname', 'email', 'gender', 'dob', 'picture', 'creation_date'
        # all columns allowed to be changed after acc creation

        def __init__(self, id, username, password,  nickname, email, gender = None, dob = None, bio = None, picture = None, creation_date = None):
            self.id = id
            self.username = username
            self.password = password
            self.nickname = nickname
            self.email = email
            self.gender = gender
            self.dob = dob
            self.bio = bio
            self.picture = picture
            self.creation_date = creation_date

        @staticmethod
        def find(*, id=None, username=None, email=None, all=False):
            no_args = sum(x is not None and x is not False for x in [id, username, email, all])
            if no_args > 1:
                # more than one option supplied!
                raise ValueError('find() requires 1 argument to be set: either \'id\', \'username\', \'email\' or \'all\''
                                 + ', ' + str(no_args) + " given")
            if id is not None:
                cur.execute(
                '''
                SELECT *
                FROM users
                WHERE id = ?
                ''', (id,)
                )
                row = cur.fetchone()

                if row is None:
                    return None
                return User(*row)

            elif username is not None:
                cur.execute(
                '''
                SELECT *
                FROM users
                WHERE username = ?
                ''', (username,)
                )
                row = cur.fetchone()

                if row is None:
                    return None
                return User(*row)

            elif email is not None:
                cur.execute(
                    '''
                    SELECT *
                    FROM users
                    WHERE email = ?
                    ''', (email,)
                )
                row = cur.fetchone()

                if row is None:
                    return None
                return User(*row)

            elif all:
                cur.execute(
                '''
                SELECT *
                FROM users
                ORDER BY id ASC
                ''')
                all_users = cur.fetchall()
                if all_users:
                    rows = [User(*row) for row in all_users]
                    return rows
                else:
                    return None
            else:
                raise TypeError('find() requires 1 argument to be set: either \'id\', \'username\', \'email\' or \'all\'')



        @staticmethod
        def sign_up(username, password, nickname, email):
            """signs up a user, given the bare minimum"""
            creation_date = datetime.now().isoformat()
            cur.execute(
            '''
            INSERT INTO users (username, password, nickname, email, creation_date) VALUES (?, ?, ?, ?, ?)
            ''', (username, password, nickname, email, creation_date)
            )
            id = cur.lastrowid
            conn.commit()
            return User.find(id=id)

        @staticmethod
        def update(id, password, nickname, email, gender, dob, bio, picture):
            """
            Updates the user given all the values required. see update_some to update one/some value. Kinda deprecated
            """
            cur.execute(
            '''
            UPDATE users
            SET password = ?,
            nickname = ?,
            email = ?,
            gender = ?,
            dob = ?,
            bio = ?,
            picture = ?
            WHERE id = ?
            ''', (password, nickname, email, gender, dob, bio, picture, id)
            )
            conn.commit()
            return User.find(id=id)

        @staticmethod
        def update_some(**kwargs):
            """Updates one value. Use update_one(nickname='newnick',...)"""
            if all((i in User.MUTABLE_COLS for i in kwargs.keys())):
                # check if the columns are allowed to be altered
                for key in kwargs:
                    cur.execute(
                        """UPDATE users
                        SET %s = ?""" % key, (kwargs[key],)
                    )
                    # yes i know string formatting is bad with sql. Its a necessary evil :(
                conn.commit()
            else:
                raise ValueError("Some of the keys were invalid!", [x for x in kwargs.keys() if x not in User.MUTABLE_COLS])


        @staticmethod
        def login(username, password):
            """logs the user in given username and password hash. returns User obj with username or none if login failed"""
            cur.execute(
            '''
            SELECT id
            FROM users
            WHERE username = ? AND password = ?
            ''',
            (username, password))
            row = cur.fetchone()
            if row is None:
                return None
            return User(*row)

        def delete(self):
            """Deletes a user from the database"""
            cur.execute(
            '''
            DELETE FROM users WHERE username = ?
            ''' , (self.username,))
            conn.commit()

        def create_post(self, username, description, title, photo_files):
            return Post.create(self, username, description, title, photo_files)

        def all_posts(self):
            return Post.find_all(self)

        def find_post(self, post_id):
            return Post.find(post_id)

        def create_comment(self, post, text, parent, profile_pic=None):
            return Comment.create(self, post, text, datetime.now(), parent=parent, profile_pic=profile_pic)

        def edit(self, password, nickname, email, gender, dob, bio, picture):
            return User.update(self.id, password, nickname, email, gender, dob, bio, picture)

    class Post:

        def __str__(self):
            return self.__repr__()

        def __repr__(self):
            return "<Post: ID: {}, title: \'{}\', User ID: {}>".format(self.id, self.title, self.user.id)

        def __init__(self, id, user, description, title, date, file):
            self.id = id
            self.user = user # type: User
            self.description = description
            self.title = title
            self.date = date
            self.file = file

        @staticmethod
        def find(id):
            cur = conn.execute(
            '''
            SELECT *
            FROM posts
            WHERE id = ? ''', (id,)
            )
            row1 = cur.fetchone()

            if row1 is None:
                return None
            return Post(row1[0], User.find(id=row1[1]), *row1[2:])

        @staticmethod
        def get_next_post_id():
            cur = conn.execute(
            '''
            SELECT id
            FROM posts
            ORDER BY id desc
            '''
            )
            row1 = cur.fetchone()[0] + 1
            return row1

        @staticmethod
        def find_all(user = None):
            if user is None:
                cur = conn.execute(
                '''
                SELECT *
                FROM posts
                ORDER BY post_date DESC; '''
                )
            else:
                cur = conn.execute('''
                SELECT *
                FROM posts
                WHERE user_id = ?
                ORDER BY post_date DESC; ''', (user.id,)
                )
            all_posts = cur.fetchall()
            if all_posts:
                rows = [Post.find(row[0]) for row in all_posts]
                return rows
            else:
                return None

        @staticmethod
        def create(user, description, title, photo_file):
            date = datetime.now().isoformat()
            cur = conn.execute(
            '''
            INSERT INTO posts (user_id, description, title, post_date, file)
            VALUES (?, ?, ?, ?, ?); ''', (user.id, description, title, date, photo_file)
            )
            id = cur.lastrowid
            conn.commit()
            return Post.find(id)

        @staticmethod
        def update(id, description, title):
            cur = conn.execute(
            '''
            UPDATE posts
            SET description = ?,
            title = ?,
            WHERE id = ?
            ''', (description, title, id)
            )
            conn.commit()
            return Post.find(id)

        def delete(self):
            cur = conn.execute(
            '''
            DELETE FROM posts
            WHERE id = ? ''' , (self.id,)
            )
            conn.commit()

        def all_comments(self):
            return Comment.find_comments_for_post(self)

        def find_comment(self, comment_id):
            return Comment.find(comment_id)

    class Comment:
        """
        Comment Object contains attribs:
        id, user, post(id), parent(id) (for multiple/nested comments), text, date(sent), profile_pic (path of user profile avatar), location(latitude), location(longitude), score
        """

        #def __str__(self):
        #    return self.__repr__()

        #def __repr__(self):
        #    return "<Comment: ID: {}, title: \'{}\', User ID: {}>".format(self.id, self.text, self.user.id)

        def __init__(self, id, user, post, parent = None, text = None, date = None, profile_pic = None, loc_latitude = None, loc_longitude = None, score = None):
            self.id = id
            self.user = user
            self.post = post
            self.text = text
            self.date = date
            self.profile_pic = profile_pic
            self.parent = parent
            self.score = score
            self.loc_latitude = loc_latitude
            self.loc_longitude = loc_longitude

        @staticmethod
        def create(user, post, text, date, parent = None, profile_pic = None, loc_latitude = None, loc_longitude = None, score = None):
            cur = conn.execute(
            '''
            INSERT INTO comments (user_id, post_id, parent_id, text, date, profile_pic, loc_latitude, loc_longitude, score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?); ''', (user.id, post.id, parent.id if parent is not None else parent, text, date, profile_pic, loc_latitude, loc_longitude, score))

            conn.commit()
            print('Comment.create')
            print('text', text)
            print('cur.lastrowid', cur.lastrowid)
            comment_ret = Comment.find(cur.lastrowid)
            print('comment_ret.user', comment_ret.user)
            print('comment_ret.text', comment_ret.text)
            return Comment.find(cur.lastrowid)

        @staticmethod
        def find(id):
            cur = conn.execute(
            '''
            SELECT *
            FROM comments
            WHERE id = ? ''', (id,)
            )
            row = cur.fetchone()

            if row is None:
                return None
            # id | (user obj) | post_id, parent_id, text, date, profile_pic, loc_lat, loc_long, score
            return Comment(row[0], User.find(id=row[1]), *row[2:])

        @staticmethod
        def find_comments_for_post(post):
            cur = conn.execute(
            '''
            SELECT *
            FROM comments
            WHERE post_id = ?
            ORDER BY date''', (post.id,)
            )
            rows = [Comment.find(row[0]) for row in cur.fetchall()]
            return rows

        @staticmethod
        def find_comments_for_user(user):
            cur = conn.execute(
            '''
            SELECT *
            FROM comments
            WHERE user_id = ?
            ORDER BY date''', (user.id,)
            )
            rows = [Comment.find(row[0]) for row in cur.fetchall()]
            return rows

        @staticmethod
        def find_children_for_comment(parent):
            cur = conn.execute(
            '''
            SELECT *
            FROM comments
            WHERE parent_id = ?
            ORDER BY date''', (parent.id,))

            rows = [Comment.find(row[0]) for row in cur.fetchall()]
            return rows

        # Extra field to identify that it's edited? (int, represented as * on page | edited_date represented as string ¯\_(ツ)_/¯)
        @staticmethod
        def edit_comment_with_id(comment_id, new_text):
            cur = conn.execute(
            '''
            UPDATE comments
            SET text = ?
            WHERE id = ?''', (new_text, comment_id)
            )
            conn.commit()
            return Comment.find(comment_id)

    def print_p(*args):
        print("\033[92m" + "[+] " + " ".join(args) + '\033[0m')

    def print_w(*args):
        print("\033[93m" + " ".join(args) + '\033[0m')

    if __name__ == "__main__":
        '''
        #sign_up(username, password, nickname, email, datetime)
        #User.sign_up('kay', '12345abc', 'kyap', 'yapkaymen@gmail.com', '1/10/2017')
        #User.sign_up('abc', 'ghsdak', 'paks', 'team@gmail.com', '1/10/2017')
        #details = User.find('kay')
        #assert details.username == 'kay'
        #try:
            #details1 = User.find('abc')
            #User.update('kay', 'abc', 'bear', 'bear@gmail.com', 'M', '30/01/1999', 'Bear is bear', 'picture')
            #details = User.find('kay')
        #except UserNotFound:
            #pass
        #multidetails = User.find_all()

        #my_user = User.sign_up('amazing-user', 'secure-password', '¯\_(ツ)_/¯', 'some@email.com', '1/10/2017')

        # -- Begin Post testing
        print_w("Beginning Post tests")

        my_post = Post.create(my_user.id, "Can y'all help me with finding out where I can get this water bottle from (and what brand it is)?", "What's this water bottle?", "1/10/2017", [])
        # Post finding testing
        assert Post.find(my_post.id).user_id == my_user.id  # Expected result: Pass
        print_p("Existing Post finding test passed!")
        try:
            Post.find(999) # Expected result: Fail
            assert 0
        except PostNotFound:
            print_p("Uncreated Post finding test passed!")
        # Post deleting testing
        Post.delete(my_post.id)
        try:
            Post.find(my_post.id) # Expected result: Pass
            assert 0
        except PostNotFound:
            print_p("Post deleting test passed!")
        print()
        print_p("Post tests passed!")

        # -- End Post testing
        '''
        kay = User(1, 'kay', '12345abc', 'kyap', 'yapkaymen@gmail.com')
        kay_post = Post(2, 1, 'description', 'title', 'date', 'files')
        print(kay_post.get_next_post_id())
        #kay_post.find(2)
        #kay_comment = Comment.create(1, 1, 2, 'text', 'date')
        #kay_comment.edit_comment_with_id(1, 'text1')
        #kay_post.find_comment(1)
        #kay.create_post(self, 'Hi', 'One', '1/1/2017', 'file')
        #print(kay.find_post(1))
        #print(Post.find_all()) - works
        #print(kay.all_posts())
        #print(kay.find_post(5)) - works
        #kay.create_comment(kay_post, 'text', 'date', None)
        #kay.edit('password', 'nickname', 'email', 'gender', 'dob', 'bio', 'picture')
        #edit = kay.find(kay.id)
        #print(edit)
        #kay_post.find_comment(1)
