# coding=utf-8
from base import base_handler
import tornado

class setting_handler(base_handler):
    @tornado.web.authenticated
    def get(self):
        return self.render('setting.html',
                           page_name='setting')