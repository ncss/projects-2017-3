from typing import Callable
from template_engine.parser import render


USER_COOKIE = "current_user"

ALL_USER = {} # username : USER (object)
class User:
    def __init__(self, id, username, pasw, nick, email, gend, dob, bio, date):
        self.id = id
        self.username = username
        self.pasw = pasw
        self.nick = nick
        self.email = email
        self.gend = gend
        self.dob = dob
        self.bio = bio
        self.date = date

    def __str__(self):
        return "id=%s, user=%s, pass=%s, nick=%s, email=%s, gend=%s, dob=%s, bio=%s, date=%s" % (self.id, self.username, self.pasw, self.nick, self.email, self.gend,
                                                                                                 self.dob, self.bio, self.date
                                                                                             self.dob, self.bio, self.date
                                                                                                 )

def add_user(user):
    ALL_USER[user.username] = user

def check_cookie(response):

    user_cookie = response.get_secure_cookie(USER_COOKIE)
    if user_cookie:
        user_cookie = user_cookie.decode("utf-8")
        print(user_cookie)
        user = ALL_USER.get(user_cookie, None) # type: User
        if user is not None:
            print('user_cookie in alluser')
            return True

    return False


def authenticate_cookie(response):
    """Returns True if cookies can be authenicated"""
    if check_cookie(response):
        return True
    return False

def render_no_login(response):
    response.write(render('notsignedin.html',{}))

def requires_login(func: Callable) -> Callable:
    """
    Function decorator for requiring login
    """
    def ret(response, *args, **kwargs):
        if authenticate_cookie(response):
            # noinspection PyCallingNonCallable
            return func(response, *args, **kwargs)
        else:
            return render_no_login(response)
    return ret



@requires_login
def foo(response, *args, **kwargs):
    print(response)


#x = User('1', 'jack', 'hash', 'jack', 'email', 'm', '241-25', 'joegjlqejfgjawdlfkjd', '2012391934')
#print(x.id)
ALL_USER['jack'] = User('1', 'jack', '21i3u41234', 'jackywathy','jackywathy24@gmail.com', 'm', '24029999', 'jack is a person', '24/02/1111')
