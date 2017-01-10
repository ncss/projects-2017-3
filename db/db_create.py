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
    picture TEXT NOT NULL,
    datetime TEXT NOT NULL)
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
    class User:

        def __init__(self, id, username, password,  nickname, email, gender, dob, bio, picture, datetime):
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
        def sign_up(username, password, nickname, email, datetime):
            cur = conn.excecute(
            '''
            INSERT INTO users VALUES (?, ?, ?, ?, ?)
            ''', (username, password, nickname, email, datetime)
            )
            return User(username, password, nickname, email)


        @staticmethod
        def update(username, password, nickname, email, gender, dob, bio, picture):
            cur = conn.excecute(
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
            return User(username, password, nickname, email, gender, dob, bio, picture)


        @staticmethod
        def delete_user(username):
            cur = conn.excecute('''
            DELETE FROM users WHERE username = ?
            ''' , (username,))

        @staticmethod
        def find(username):
            cur = conn.excecute(
            '''
            SELECT *
            FROM users
            WHERE username = ? ''', (username,)
            )
            row = cur.fetchone()

            if row is None:
                raise UsernNotFOund('{} does not exist'.format(username))
            return User(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])

    class Post:

        def __init__(self, id, user_id, description, title, date, files):
            self.id = id
            self.user_id = user_id
            self.description = description
            self.title = title
            self.date = date
            self.files = files

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

        def add_photo(file_name, user_id, post_id, date):
            cur = conn.execute(
            '''
            INSERT INTO photos (file_name, user_id, post_id, photo_date)
            VALUES (?, ?, ?, ?); ''', (file_name, user_id, post_id, date)
            )
            conn.commit()
            return (cur.lastrowid, file_name)

        def delete_photo(post_id, file_name):
            cur = conn.execute(
            '''
            DELETE FROM photos
            WHERE post_id = ? AND file_name = ? ''' , (post_id, file_name)
            )
            conn.commit()

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

        def delete(id):
            cur = conn.excecute(
            '''
            DELETE FROM posts
            WHERE id = ? ''' , (id,)
            )
            conn.commit()

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

    Post.create(1, 'some text', 'some title', 'probally a string', ['file1', 'file2', 'file3'])
    Post.find(1)
    Post.delete_photo(1, 'file1')
