import sqlite3
with sqlite3.connect('db.db') as conn:
    cur = conn.cursor()
    cur.execute(
    '''
    CREATE TABLE users
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    nickname TEXT,
    email TEXT NOT NULL,
    gender TEXT,
    dob TEXT,
    bio TEXT,
    picture TEXT,
    datetime TEXT)
    '''
    )


    cur.execute(
    '''
    CREATE TABLE posts
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    description TEXT,
    title TEXT NOT NULL,
    post_date TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id))

    '''
    )

    cur.execute(
    '''
    CREATE TABLE photos
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_name TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    post_id INTEGER NOT NULL,
    photo_date TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(post_id) REFERENCES posts(id)
    )

    '''
    )

    cur.execute(
    '''
    CREATE TABLE comments
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    post_id INTEGER NOT NULL,
    parent_id INTEGER NOT NULL,
    text TEXT NOT NULL,
    date TEXT NOT NULL,
    score INTEGER NOT NULL,
    FOREIGN KEY(parent_id) REFERENCES comments(id),
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(post_id) REFERENCES posts(id))

    '''
    )

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

        def __init__(self, id, user_id, description, title, date):
            self.id = id
            self.user_id = user_id
            self.description = description
            self.title = title
            self.date = date

        def find(id):
            cur = conn.cursor(
            '''
            SELECT *
            FROM posts
            WHERE id = ? ''', (id,)
            )
            row = cur.fetchone()

            if row is None:
                raise PostNotFound('{} does not correspond to a post that exists.'.format(id))
            return Post(row[0], row[1], row[2], row[3], row[4])

        def create(user_id, description, title, date):
            cur = conn.cursor(
            '''
            INSERT INTO posts (user_id, description, title, post_date)
            VALUES (?, ?, ?, ?); ''', (user_id, description, title, date))

            return Post (cur.lastrowid, user_id, description, title, date)

        def delete(id, user_id):
            #   to do
            pass



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
            ORDER BY date''', (parent_id,)

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

    User.sign_up('ske', 'h3FR9R', 'steph', 'fdghasbka')
    User.sign_up('hi', 'hfks', 'shdkd', 'jskfs')
    User.login('ske', 'h3FR9R')
    User.find_multiple()
    conn.commit()
