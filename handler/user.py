# coding=utf-8
from base import base_handler
#import tcelery
import task
import tornado
from model.user import User
from tornado.options import options
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#tcelery.setup_nonblocking_producer()

class register_handler(base_handler):
    def get(self):
        user = User()
        user.email = ""
        user.password = ""
        user.name=""
        user.password_confirm = ""
        return self.render('register.html', user_name="", user=user, errors={})
    def post(self):
        email = self.get_argument('email','')
        user_name = self.get_argument('user_name','')
        password = self.get_argument('password','')
        password_confirm = self.get_argument('password_confirm','')

        user = User()
        user.email = email
        user.name = user_name
        user.password = password
        user.password_confirm = password_confirm
        user_id = user.create()
        if not user_id:
            return self.render('register.html', user_name="", user=user, errors=user.errors)
            #return self.send_error_json(user.errors)
        else:
            self.redirect('/login')



class login_handler(base_handler):
    def get(self):
        self.render('login.html',
                    username_warning='',
                    password_warning='',
                    login_warning='',
                    page_name='login',
                    user_name="")

    @tornado.web.asynchronous
    def post(self):
        username = self.get_argument('username')
        if username == '':
            self.render('login.html',
                    username_warning = '用户名不能为空',
                    password_warning = '',
                    login_warning = '',
                    page_name = 'login')
        else:
            password = self.get_argument('password')
            if password == '':
                self.render('login.html',
                        username_warning = '',
                        password_warning = '密码不能为空',
                        login_warning = '',
                        page_name = 'login')
            else:
                res = task.user_login(username, password)
                self.on_login_success(res)

    def on_login_success(self, resp):
        if resp:
            user_id = resp
            print 'id',user_id
            self.set_secure_cookie('u_u', str(user_id))
            return_url = self.get_argument('return', '/')
            print "url",return_url
            self.redirect(return_url)
        else:
            self.render('login.html',
                    username_warning = '',
                    password_warning = '',
                    login_warning = '用户名或密码错误',
                    page_name = 'login')


class logout_handler(base_handler):
    @tornado.web.authenticated
    def get(self):
        self.clear_cookie('u_u')
        return self.redirect('/')
