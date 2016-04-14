# coding=utf-8
from base import base_handler
from model.device_observed import Device_Observed
import task
import tornado

#tcelery.setup_nonblocking_producer()


class about_handler(base_handler):
    def get(self):
        return self.render('about.html',
                           page_name='about')


class home_handler(base_handler):
    @tornado.web.authenticated
    def get(self):
        user = self.get_current_user()
        print "home page"
        dev_observed = Device_Observed()
        device_counts = dev_observed.count_user_devices(user.id)
        res = task.get_summery_info(user)
        self.on_get_summery_info(res)


    def on_get_summery_info(self, resp):
        user_name = resp['user_name']
        device_counts = resp['device_counts']
        device_info = resp['device_info']

        return self.render('home.html',
                           user_name=user_name,
                           device_counts=device_counts,
                           device_info=device_info,
                           page_name='home')