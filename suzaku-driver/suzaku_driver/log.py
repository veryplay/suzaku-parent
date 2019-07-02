#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import yaml
import logging.config

def configure_logging():
    here = os.path.abspath(os.path.dirname(__file__))
    log_config_file = os.path.join(here, "logging.yml")

    with open(log_config_file, 'rt') as f:
        log_config = yaml.load(f.read())
    log_config['handlers']['info_file_handler']['filename'] = __get_logs_filename()
    logging.config.dictConfig(log_config)
    return log_config


def __get_logs_filename():
    home = os.path.expanduser('~')
    logs_dir = os.path.join(home, "logs")
    if not os.path.exists(logs_dir):
        os.mkdir(logs_dir)
    logs_path = os.path.join(logs_dir, 'suzaku-driver.log')
    return logs_path