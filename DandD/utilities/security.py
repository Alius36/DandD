# coding: utf-8
import bcrypt
from pyramid.security import Allow


def hash_password(pw):
    pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
    return pwhash.decode('utf8')


def check_password(pw, hashed_pw):
    expected_hash = hashed_pw.encode('utf8')
    return bcrypt.checkpw(pw.encode('utf8'), expected_hash)


def role_finder(username, request):
    # return ['player']
    if 'user' in request.session:
        return [request.session['user']['role']]
    return None


class RootFactory:
    def __init__(self, request):
        self.__acl__ = [
            (Allow, "player", "play")
        ]
