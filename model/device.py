#!/usr/bin/env python
# -*- coding: utf-8 -*-
from transwarp.db import next_id
from transwarp.orm import Model, StringField, BooleanField, FloatField, TextField, IntegerField
import time
from util import get_md5

class Device(Model):
    __table__ = 'device'

    id = IntegerField(primary_key=True, default=next_id)
    location = StringField(ddl='varchar(50)')
    mac = StringField(ddl='varchar(50)')
    created_at = FloatField(updatable=False, default=time.time)

    def create(self):
        pass


    def creator(self, device_id):
        return self.find_first('where id = ?', device_id)

    def get_device_by_mac(self, mac):
        mac_wrapped = get_md5(mac)
        device = self.find_first('where mac = ?', mac_wrapped)
        if device:
            return device.id
        return None

