#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'guoxiao'

from transwarp.db import next_id
from transwarp.orm import Model, StringField, BooleanField, FloatField, TextField, IntegerField
import time

class Device_Observed(Model):
    __table__ = "device_observed"

    id = IntegerField(primary_key=True, default=next_id)
    device_id = IntegerField()
    user_id = IntegerField()

    def observe(self, user_id, device_id):
        observed = self.find_first('where user_id = ? and device_id = ?', user_id, device_id)
        if not observed:
            self.user_id = user_id
            self.device_id = device_id
            self.insert()
            return True
        return True

    def unobserve(self, user_id, device_id):
        observed = self.find_first('where user_id = ? and device_id = ?', user_id, device_id)
        if observed:
            observed.delete()
            return True
        return True


    def observed_devices(self, user_id):
        devices = self.find_by('where user_id = ?', user_id)
        if devices:
            return devices
        return []

    def count_user_devices(self, user_id):
        return self.count_by('where user_id = ?', user_id)