__author__ = 'guoxiao'

from base import base_handler
import os

#import tcelery
import task
from model.device import Device
from model.position import Position
from model.device_observed import Device_Observed
from util import get_md5
import json
import time

#tcelery.setup_nonblocking_producer()


class image_handler(base_handler):
    def post(self):

        file_metas=self.request.files['file']
        if len(file_metas) > 0:
            device_mac = self.get_argument('mac', '')
            device_pos = self.get_argument('pos', '')
            created_at = self.get_argument('created_at',time.time())
            print device_mac, device_pos, created_at
            meta = file_metas[0]
            res = task.img_upload(device_mac, device_pos,created_at, meta)
            self.on_upload_success(res)

    def on_upload_success(self, resp):
        if resp:
            self.write('ok')
        else:
            self.write('fail')


class device_handler(base_handler):
    def post(self):
        jdatas = json.loads(self.request.body)
        #device_mac = self.get_argument('mac', '')
        #device_location = self.get_argument('location', '')
        device_mac = jdatas['mac']
        device_location = jdatas['location']
        print device_mac,'location:',device_location
        dev = Device()
        dev.mac=get_md5(device_mac)
        dev.location=device_location
        if None == dev.get_device_by_mac(device_mac):
            device_id = dev.create()
        else:
            device_id = dev.update_info()
        print device_id
        if not device_id:
            self.write('fail')
            return
        self.write('ok')

class observer_handler(base_handler):
    def post(self):
        jdatas = json.loads(self.request.body)
        device_mac = jdatas['mac']
        #device_mac = self.get_argument('mac','')
        dev = Device()
        self.device_id = dev.get_device_by_mac(device_mac)
        if self.device_id == None:
            self.write("fail")
            return

        #self.observed = self.get_argument('observed',False)
        #user_name = self.get_argument('user_name','')
        #user_password = self.get_argument('user_password','')

        self.observed = jdatas['observed']
        print "observed", self.observed
        user_name = jdatas['user_name']
        user_password = jdatas['user_password']

        res = task.user_login(user_name, user_password)
        if self.on_login_success(res):
            self.write("ok")
            return

        self.write('fail')

    def on_login_success(self, resp):
        if resp:
            dev_observed = Device_Observed()
            if self.observed:
                dev_observed.observe(resp, self.device_id)
            else:
                dev_observed.unobserve(resp, self.device_id)
            return True
        return False



class position_handler(base_handler):
    def post(self):
        jdatas = json.loads(self.request.body)
        #device_mac = self.get_argument('mac', '')
        device_mac = jdatas['mac']

        dev = Device()
        device_id = dev.get_device_by_mac(device_mac)
        #position_infos = self.get_argument('positions', [])
        position_infos = jdatas['positions']

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
            print pos_id
            if not pos_id:
                self.write('fail')
                return
        self.write('ok')


