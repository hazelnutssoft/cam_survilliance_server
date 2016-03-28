from base import base_handler

class about_handler(base_handler):
    def get(self):
        return self.render('about.html',
                           page_name='about')

class home_handler(base_handler):
    @tornado.web.authenticated
    def get(self):

        return self.render('home.html',
                           page_name='home')