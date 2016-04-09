#!/usr/bin/env python
# -*- coding: utf-8 -*-
from transwarp.db import next_id
from transwarp.orm import Model, StringField, BooleanField, FloatField, TextField, IntegerField
import time,os

class Image(Model):
    __table__ = 'image'

    id = IntegerField(primary_key=True, default=next_id)
    position_id = IntegerField()
    path = StringField(ddl='varchar(200)')
    created_at = FloatField(updatable=False, default=time.time)

    def validate(self):
        if os.path.exists(self.path):
            return True
        return False

    def create(self):
        self.created_at = time.time()
        if self.validate():
            self.insert()
            return self.id
        else:
            return None

    def count_by_position_id(self, position_id):
        return self.count_by('where position_id = ?', position_id)
