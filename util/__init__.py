__auther__= "guo xiao"

from marcos import *
from hashlib import sha1

def hash_password(password):
    return sha1('{password}{salt}'.format(
        password = sha1(password).hexdigest(),
        salt = PASSWORD_SALT)).hexdigest()

def check_user_exists(func):
    import model
    def wrapper(self, user_id):
        u= model.user.User().find_first("id = ?",user_id)
        if not u:
            self.redirect("/login")
        self.user = u
        return func(self, user_id)
