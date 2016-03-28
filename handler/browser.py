from base import base_handler

class browser_handler(base_handler):
    @tornado.web.authenticated
    def get(self):
        return self.render('browser.html',
                           page_name='browser')