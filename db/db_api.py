import datetime
#from ..backend.common import *
import sqlite3
with sqlite3.connect('db.db') as conn:
    cur = conn.cursor()
    class CommentNotFoundException(Exception):
        pass

    class UserNotFound(Exception):
        pass

    class PostNotFound(Exception):
        pass

    class User:

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
            #list of questions
            #make date time more meaningful

        #method to ask question


        @staticmethod
        def find(id):
            cur.execute(
            '''
            SELECT *
            FROM users
            WHERE id = ? ''', (id,)
            )
            row = cur.fetchone()

            if row is None:
                return None
            return User(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])

        @staticmethod
        def find_by_username(username):
            cur.execute(
            '''
            SELECT *
            FROM users
            WHERE username = ? ''', (username,)
            )
            row = cur.fetchone()

            if row is None:
                return None
            return User.find(row[0])

        @staticmethod
        def find_multiple():
            cur.execute(
            '''
            SELECT *
            FROM users
            ORDER BY creation_date
                ''')
            all_users = cur.fetchall()
            for row in all_users:
                if row is None:
                    return None
            rows = [User.find(row[0]) for row in all_users]
            return rows

        @staticmethod
        def sign_up(username, password, nickname, email):
            #creation_date = get_current_time()
            creation_date = datetime.now().isoformat()
            cur.execute(
            '''
            INSERT INTO users (username, password, nickname, email, creation_date) VALUES (?, ?, ?, ?, ?)
            ''', (username, password, nickname, email, creation_date)
            )
            id = cur.lastrowid
            conn.commit()
            return User.find(id)

        @staticmethod
        def update(id, password, nickname, email, gender, dob, bio, picture):
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
            return User.find(id)

        @staticmethod
        def delete(username):
            cur.execute('''
            DELETE FROM users WHERE username = ?
            ''' , (username,))
            conn.commit()

        @staticmethod
        def login(username, password):
            cur.execute('''
            SELECT id
            FROM users
            WHERE username = ? AND password = ? ''',
            (username, password))
            row = cur.fetchone()
            user_id = None if row is None else row[0]
            return user_id

        def create_post(self, description, title, date, photo_files):
            return Post.create(self.id, description, title, date, photo_files)

        def all_posts(self):
            return Post.find_all(self.id)

        def find_post(post_id):
            return Post.find(post_id)

        def create_comment(self, Post, text, date, parent_id):
            return Comment.create(self.id, Post.return_id(), text, date, parent_id)

        def edit(self, password, nickname, email, gender, dob, bio, picture):
            return User.update(self.id, password, nickname, email, gender, dob, bio, picture)

    class Post:

        def __str__(self):
            return self.__repr__()

        def __repr__(self):
            return "<Post: ID: {}, title: \'{}\', User ID: {}>".format(self.id, self.title, self.user_id)

        def __init__(self, id, user_id, description, title, date, files):
            self.id = id
            self.user_id = user_id
            self.description = description
            self.title = title
            self.date = date
            self.files = files

        def return_id(self):
            return self.id

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

            cur = conn.execute(
            '''
            SELECT file_name
            FROM photos
            WHERE post_id = ? ''', (id,)
            )
            row2 = cur.fetchall()

            return Post(row1[0], row1[1], row1[2], row1[3], row1[4], row2)

        @staticmethod
        def find_all(user_id = None):
            if not user_id:
                cur = conn.execute(
                '''
                SELECT *
                FROM posts; '''
                )
            else:
                cur = conn.execute(
                '''
                SELECT *
                FROM posts
                WHERE user_id = ? ''', (user_id,)
                )
            row1 = cur.fetchall()

            if not row1:
                return None

            posts = []
            for row in row1:
                id = row[0]
                cur = conn.execute(
                '''
                SELECT file_name
                FROM photos
                WHERE post_id = ? ''', (id,)
                )
                posts.append(Post.find(id))

            return posts

        @staticmethod
        def add_photo(file_name, post_id, date):
            cur = conn.execute(
            '''
            INSERT INTO photos (file_name, post_id, photo_date)
            VALUES (?, ?, ?); ''', (file_name, post_id, date)
            )
            conn.commit()
            return (cur.lastrowid, file_name)

        @staticmethod
        def delete_photo(post_id, file_name):
            cur = conn.execute(
            '''
            DELETE FROM photos
            WHERE post_id = ? AND file_name = ? ''' , (post_id, file_name)
            )
            conn.commit()

        @staticmethod
        def create(user_id, description, title, date, photo_files):
            cur = conn.execute(
            '''
            INSERT INTO posts (user_id, description, title, post_date)
            VALUES (?, ?, ?, ?); ''', (user_id, description, title, date)
            )
            id = cur.lastrowid
            conn.commit()

            for files in photo_files:
                Post.add_photo(files, id, date)
            return Post.find(id)

        @staticmethod
        def delete(id):
            cur = conn.execute(
            '''
            DELETE FROM posts
            WHERE id = ? ''' , (id,)
            )
            conn.commit()

        @staticmethod
        def update(id, user_id, description, title, date, files):
            cur = conn.excecute(
            '''
            UPDATE posts
            SET description = ?,
            title = ?,
            WHERE id = ?
            ''', (description, title, id)
            )
            conn.commit()
            return Post.find(id)

        def all_comments(self):
            return Comment.find_all(self.id)

        def find_comment(comment_id):
            return Comment.find(comment_id)

    class Comment:

        def __init__(self, id, user_id, post_id, text, date, parent_id, score = None, loc_latitude = None, loc_longitude = None):
            self.id = id
            self.user_id = user_id
            self.post_id = post_id
            self.text = text
            self.date = date
            self.parent_id = parent_id
            self.score = score
            self.loc_latitude = loc_latitude
            self.loc_longitude = loc_longitude

        @staticmethod
        def create(user_id, post_id, text, date, parent_id):
            cur = conn.execute(
            '''
            INSERT INTO comments (user_id, post_id, text, date, parent_id)
            VALUES (?, ?, ?, ?, ?); ''', (user_id, post_id, text, date, parent_id))

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
            return Comment(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])

        @staticmethod
        def find_comments_for_post_id(post_id):
            cur = conn.excecute(
            '''
            SELECT *
            FROM comments
            WHERE post_id = ?
            ORDER BY date''', (post_id,)
            )
            rows = [Comment.find(row[0]) for row in cur.fetchall()]
            return rows

        @staticmethod
        def find_comments_for_user(user_id):
            cur = conn.excecute(
            '''
            SELECT *
            FROM comments
            WHERE user_id = ?
            ORDER BY date''', (post_id,)
            )
            rows = [Comment.find(row[0]) for row in cur.fetchall()]
            return rows

        @staticmethod
        def find_children_for_comment(parent_id):
            cur = conn.excecute(
            '''
            SELECT *
            FROM comments
            WHERE parent_id = ?
            ORDER BY date''', (parent_id,))

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
            return find(comment_id)

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
        #multidetails = User.find_multiple()

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
        #kay = User(1, 'kay', '12345abc', 'kyap', 'yapkaymen@gmail.com')
        #kay_post = Post(1, 1, 'description', 'title', 'date', ['files'])
        #kay.create_post(self, 'Hi', 'One', '1/1/2017', 'file') - works
        #print(kay.find_post(1)) - works
        #print(Post.find_all()) - works
        #print(kay.all_posts()) - works
        #print(kay.find_post(5)) - works
        #print(kay.create_comment(kay_post, 'text', 'date', None))
