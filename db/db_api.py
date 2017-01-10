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

        def __init__(self, id, username, password,  nickname, email, gender = None, dob = None, bio = None, picture = None, datetime = None):
            self.id = id
            self.username = username
            self.password = password
            self.nickname = nickname
            self.email = email
            self.gender = gender
            self.dob = dob
            self.bio = bio
            self.picture = picture
            self.datetime = datetime

        @staticmethod
        def find(username):
            cur.execute(
            '''
            SELECT *
            FROM users
            WHERE username = ? ''', (username,)
            )
            row = cur.fetchone()

            if row is None:
                raise UserNotFound('{} does not exist'.format(username))
            return User(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])

        @staticmethod
        def find_multiple():
            cur.execute(
            '''
            SELECT *
            FROM users
            ORDER BY datetime
                ''')
            all_users = cur.fetchall()
            for row in all_users:
                if row is None:
                    raise UserNotFound('{} does not exist'.format(username))
            return all_users

        @staticmethod
        def sign_up(username, password, nickname, email, datetime):
            cur.execute(
            '''
            INSERT INTO users (username, password, nickname, email, datetime) VALUES (?, ?, ?, ?, ?)
            ''', (username, password, nickname, email, datetime)
            )
            id = cur.lastrowid
            conn.commit()
            return User(id, username, password, nickname, email, datetime)

        @staticmethod
        def update(username, password, nickname, email, gender, dob, bio, picture):
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
            WHERE username = ?
            ''', (password, nickname, email, gender, dob, bio, picture, username)
            )
            conn.commit()
            return User(username, password, nickname, email, gender, dob, bio, picture)

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
            user_id = False if row is None else True
            return user_id

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
                raise PostNotFound('{} does not correspond to a post that exists.'.format(id))

            cur = conn.execute(
            '''
            SELECT file_name
            FROM photos
            WHERE post_id = ? ''', (id,)
            )
            row2 = cur.fetchall()

            return Post(row1[0], row1[1], row1[2], row1[3], row1[4], row2)

        @staticmethod
        def add_photo(file_name, user_id, post_id, date):
            cur = conn.execute(
            '''
            INSERT INTO photos (file_name, user_id, post_id, photo_date)
            VALUES (?, ?, ?, ?); ''', (file_name, user_id, post_id, date)
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
                Post.add_photo(files, user_id, id, date)
            return Post (id, user_id, description, title, date, photo_files)

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
            return Post(id, user_id, description, title, date, files)

    class Comment:

        def __init__(self, id, user_id, post_id, text, date, parent_id, score):
            self.id = id
            self.user_id = user_id
            self.post_id = post_id
            self.text = text
            self.date = date
            self.parent_id = parent_id
            self.score = score

        @staticmethod
        def create(user_id, post_id, text, date, parent_id):
            cur = conn.cursor(
            '''
            INSERT INTO comments (user_id, post_id, text, date, parent_id)
            VALUES (?, ?, ?, ?, ?); ''', (user_id, post_id, text, date, parent_id))

            return Comment(cur.lastrowid, user_id, post_id, text, date, parent_id, 0)

        @staticmethod
        def find(id):
            cur = conn.excecute(
            '''
            SELECT *
            FROM comments
            WHERE id = ? ''', (id,)
            )
            row = cur.fetchone()

            if row is None:
                raise CommentNotFoundException('{} does not exist'.format(id))
            return Comment(row[0], row[1], row[2], row[3], row[4], row[5], row[6])

        @staticmethod
        def find_comments_for_post_id(post_id):
            cur = conn.excecute(
            '''
            SELECT *
            FROM comments
            WHERE post_id = ?
            ORDER BY date''', (post_id,)
            )
            rows = [Comment(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in cur.fetchall()]
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
            rows = [Comment(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in cur.fetchall()]
            return rows

        @staticmethod
        def find_children_for_comment(parent_id):
            cur = conn.excecute(
            '''
            SELECT *
            FROM comments
            WHERE parent_id = ?
            ORDER BY date''', (parent_id,))

            rows = [Comment(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in cur.fetchall()]
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
        #sign_up(username, password, nickname, email, datetime)
        User.sign_up('kay', '12345abc', 'kyap', 'yapkaymen@gmail.com', '1/10/2017')
        User.sign_up('abc', 'ghsdak', 'paks', 'team@gmail.com', '1/10/2017')
        details = User.find('kay')
        assert details.username == 'kay'
        try:
            details1 = User.find('abc')

        except UserNotFound:
            pass
        multidetails = User.find_multiple()
#Georges
        my_user = User.sign_up('amazing-user', 'secure-password', '¯\_(ツ)_/¯', 'some@email.com', '1/10/2017')

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
