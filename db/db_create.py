import sqlite3
with sqlite3.connect('db.db') as conn:
    cur = conn.cursor()
    cur.execute(
    '''
    CREATE TABLE users
    (username TEXT NOT NULL,
    email TEXT NOT NULL,
    UNIQUE INTEGER PRIMARY KEY(id),
    password TEXT NOT NULL,
    creation_date TEXT NOT NULL,
    gender TEXT,
    dob TEXT,
    bio TEXT,
    picture TEXT NOT NULL,
    nickname TEXT)
    '''
    )

    cur.execute(
    '''
    CREATE TABLE photos
    (UNIQUE INTEGER PRIMARY KEY(id),
    file_name TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(post_id) REFERENCES posts(id), photo_date NOT NULL)

    '''
    )

    cur.execute(
    '''
    CREATE TABLE posts
    (UNIQUE PRIMARY KEY(id), FOREIGN KEY(user_id) REFERENCES users(id),
     description, title NOT NULL, post_date NOT NULL)

    '''
    )

    cur.execute(
    '''
    CREATE TABLE comments
    (UNIQUE PRIMARY KEY(id), FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(post_id) REFERENCES posts(id),
    text NOT NULL, date NOT NULL, parent_id, score NOT NULL)

    '''
    )
