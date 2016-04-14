__author__ = 'guoxiao'

from base import base_handler
import os

#import tcelery
import task
from model.device import Device
from model.position import Position
from model.device_observed import Device_Observed
from util import get_md5

#tcelery.setup_nonblocking_producer()


class image_handler(base_handler):
    def post(self):

        file_metas=self.request.files['file']
        if len(file_metas) > 0:

            device_mac = self.get_argument('mac', '')
            device_pos = self.get_argument('pos', '')
            meta = file_metas[0]
            res = task.img_upload(device_mac, device_pos, meta)
            self.on_upload_success(res)

    def on_upload_success(self, resp):
        if resp:
            self.write('ok')
        else:
            self.write('fail')

class device_handler(base_handler):
    def post(self):
        device_mac = self.get_argument('mac', '')
        device_location = self.get_argument('location', '')
        dev = Device(mac=get_md5(device_mac), location=device_location)
        device_id = dev.create()
        if not device_id:
            self.write('fail')
            return
        self.write('ok')

class observer_handler(base_handler):
    def post(self):
        device_mac = self.get_argument('mac','')
        dev = Device()
        self.device_id = dev.get_device_by_mac(device_mac)
        self.observed = self.get_argument('observed',False)
        user_name = self.get_argument('user_name','')
        user_password = self.get_argument('user_password','')
        res = task.user_login(user_name, user_password)
        self.on_login_success(res)

    def on_login_success(self, resp):
        if resp:
            dev_observed = Device_Observed()
            if self.observed:
                dev_observed.observe(resp.result, self.device_id)
            else:
                dev_observed.unobserve(resp.result, self.device_id)



class position_handler(base_handler):
    def post(self):
        device_mac = self.get_argument('mac', '')
        dev = Device()
        device_id = dev.get_device_by_mac(device_mac)
        position_infos = self.get_argument('positions', [])
        for pos_info in position_infos:
            position = pos_info['position']
            object_name = pos_info['object_name']
            duration = pos_info['duration']
            pos = Position()
            pos.device_id = device_id
            pos.position = position
            pos.object_name = object_name
            pos.duration = duration
            pos_id = pos.create()
            if not pos_id:
                self.write('fail')
                return
        self.write('ok')


