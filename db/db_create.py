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
                raise UsernNotFOund('{} does not exist'.format(username))
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
            #if row is None:
                #raise UsernNotFOund('{} does not exist'.format(username))
            return all_users

        @staticmethod
        def sign_up(username, password, nickname, email):
            cur.execute(
            '''
            INSERT INTO users (username, password, nickname, email) VALUES (?, ?, ?, ?)
            ''', (username, password, nickname, email)
            )
            id = cur.lastrowid
            conn.commit()
            return User(id, username, password, nickname, email)


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

    User.sign_up('ske', 'h3FR9R', 'steph', 'fdghasbka')
    User.sign_up('hi', 'hfks', 'shdkd', 'jskfs')
    User.login('ske', 'h3FR9R')
    User.find_multiple()
    conn.commit()
