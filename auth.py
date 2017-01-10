from typing import Callable


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
                                                                                                 )



def check_cookie(response):
    #TODO USE A SQL DATABASE

    return False


def authenticate_cookie(response):
    """Returns True if cookies can be authenicated"""
    if check_cookie(response):
        return True
    return False



def requires_login(func: Callable) -> Callable:
    """
    Function decorator for requring login
    """
    def ret(response, *args, **kwargs):
        if authenticate_cookie(response):
            # noinspection PyCallingNonCallable
            return func(response, *args, **kwargs)
        else:
            return False
    return ret



@requires_login
def foo(response, *args, **kwargs):
    print(response)


#x = User('1', 'jack', 'hash', 'jack', 'email', 'm', '241-25', 'joegjlqejfgjawdlfkjd', '2012391934')
#print(x.id)
