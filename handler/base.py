__author__ = 'sonic-server'

# import tornado
import tornado.web

class base_handler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_id =  self.get_secure_cookie('u_u')
        if not user_id:
            return None
        import model
        u = model.user.User().find_first("id = ?", user_id)
        if not u:
            return None
        return u