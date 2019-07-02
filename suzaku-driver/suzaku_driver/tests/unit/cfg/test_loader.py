#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase


import suzaku_driver.cfg.loader

class TestLoader(TestCase):

    def test_load_config(self):
        loader = suzaku_driver.cfg.loader.ConfigLoader()
        cfg = loader.load_config()
        self.assertIsNotNone(cfg)
