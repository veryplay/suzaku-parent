#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import yaml
import logging
import argparse


logger = logging.getLogger(__name__)


class ConfigLoader:

    def __init__(self):
        parser = argparse.ArgumentParser("options")
        parser.add_argument("-e", "--env",
            help="env variable",
            choices=[ "dev" ],
            default="dev")
        args, _ = parser.parse_known_args()
        self.env = args.env

    def load_config(self):
        here = os.path.abspath(os.path.dirname(__file__))
        # load config_$env.yml
        config_path = os.path.join(here, "config-%s.yml" % self.env)
        with open(config_path, 'r') as config_file:
            cfg = yaml.load(config_file)
            cfg["env"] = self.env
        logger.info("load config from %s", config_path)
        return cfg
