from typing import Callable


USER_COOKIE = "current_user"
ALL_USERS = {"jack", "lucas", "matilda", "dilan", 'julia'}

def get_pass_hash(name):
    #TODO USE A SQL DATABASE
    #RETURN TRUE IF NAME IN ALL _USERS NOW
    return


def authenticate_cookie(response):
    """Returns True if cookies can be authenicated"""
    if response.get_secure_cookie("current_user") in ALL_USERS:
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
