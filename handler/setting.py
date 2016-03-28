from base import base_handler

class setting_handler(base_handler):
    @tornado.web.authenticated
    def get(self):
        return self.render('setting.html',
                           page_name='setting')