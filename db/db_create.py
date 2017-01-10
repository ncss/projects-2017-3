import sqlite3
with sqlite3.connect('db.db') as conn:
    cur = conn.cursor()
    cur.execute(
    '''
    CREATE TABLE users
    (username TEXT NOT NULL,
    email TEXT NOT NULL,
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    password TEXT NOT NULL,
    datetime TEXT NOT NULL,
    gender TEXT,
    dob TEXT,
    bio TEXT,
    picture TEXT NOT NULL,
    nickname TEXT)
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

        def __init__(self, username, email, password, datetime, gender, dob, bio, picture, nickname):
            self.username = username
            self.email = email
            self.password = password
            self.datetime = datetime
            self.gender = gender
            self.dob = dob
            self.bio = bio
            self.picture = picture
            self.nickname = nickname


        @staticmethod
        def find(username):
            cur = conn.cursor(
            '''
            SELECT *
            FROM users
            WHERE username = ? ''', (username,)
            )
            row = cur.fetchone()

            if row is None:
                raise UsernNotFOund('{} does not exist'.format(username))
            return User(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[0], row[0], row[0], row[0])
