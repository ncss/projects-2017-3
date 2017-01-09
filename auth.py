from typing import Callable


def authenticate_cookie(response):
    """Returns True if cookies can be authenicated"""
    return True


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