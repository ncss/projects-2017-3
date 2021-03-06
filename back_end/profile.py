from template_engine.parser import render
from back_end.common import *
from auth import authenticate_cookie, requires_login, require_specific_user, authenticate_correct_username

def get_picture(userObj):
    return userObj.picture if userObj.picture is not None and userObj.picture != "" else "nouser.png"


def view_handler_post(request, username):
    ...

def view_handler(request, username):
    user = db.User.find_by_username(username)
    if user is None:
        request.write("username is not in db")
    else:
        request.write(render('profile.html', {'user':user, 'picture': get_picture(user)
                                        , 'signed_in':authenticate_cookie(request), 'same_user':authenticate_correct_username(request, user.username),
                                              'username': user.username
        })) # username required for pages that do not build a user object

@requires_login
@require_specific_user
def edit_handler_post(request, username):
    usr = db.User.find_by_username(username)
    nickname = request.get_field('nickname', default=usr.nickname)
    #TODO check front end for confirmation password req old pass
    pwd = request.get_field('password')
    if pwd:
        # the pwd was changed
        pwd = hash_string(pwd)
    else:
        pwd = usr.password
    email = request.get_field('email', default=usr.email)
    gender = request.get_field('gender', default=usr.gender)
    dob = request.get_field('dob', default=usr.dob)
    bio = request.get_field('bio', default=usr.bio)
    pic = usr.picture

    db.User.update(usr.id, pwd, nickname, email, gender, dob, bio, pic)
    request.redirect('/profile/'+username)


@requires_login
@require_specific_user
def edit_handler(request, username):
    ...