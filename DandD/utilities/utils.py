import hashlib


def make_response(message, code, url=None):
    return {'message': message, 'code': code, 'url': url}


def calculate_md5(filename):
    return hashlib.md5(filename).hexdigest()
