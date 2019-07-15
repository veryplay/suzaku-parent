#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)

class OutOfBondAdapter(object):

    def __init__(self, engine):
        self.engine = engine

    def set_boot_device(self, ip, username, 
        password, boot_device):
        pass

    def power_on(self, ip, username, password):
        pass

    def power_off(self, ip, username, password):
        pass

    def power_reset(self, ip, username, password):
        pass
    