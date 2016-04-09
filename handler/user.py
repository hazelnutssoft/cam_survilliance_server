from base import base_handler
import tcelery
import tasks
import tornado
from model.user import User
from tornado.options import options

tcelery.setup_nonblocking_producer()

class register_handler(base_handler):
    def get(self):
        return self.render('register.html')
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
            return self.render('/register', user=user)
            #return self.send_error_json(user.errors)
        else:
            self.redirect('/login')



class login_handler(base_handler):
    def get(self):
        self.render('login.html',
                    username_warning='',
                    password_warning='',
                    login_warning='',
                    page_name='login')

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
                tasks.user_login.apply_async(args=[username, password], callback=self.on_login_success)

    def on_login_success(self, resp):
        if resp.result:
            user_id = resp.result
            self.set_secure_cookie('u_u', u'{0}'.format(user_id),domain='.{0}'.format(options.www_domain))
            return_url = self.get_argument('return', '/')
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
        self.clear_cookie('u_u', domain='.{0}'.format(options.www_domain))
        return self.redirect('/')
