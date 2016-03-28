from base import base_handler
import tcelery
import tasks
import tornado

tcelery.setup_nonblocking_producer()

class register_handler(base_handler):
    def get(self):
        pass
    def post(self):
        pass

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
