#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import suzaku_driver.utils.executor

logger = logging.getLogger(__name__)

EXECUTABLE_FILE = "/usr/bin/ipmitool"

def set_boot_device(ip, username, password, boot_device):
    cmd = (EXECUTABLE_FILE, 
        "-I", "lanplus", 
        "-H", ip, 
        "-U", username, 
        "-P", password, 
        "chassis", "bootdev", boot_device)
    stdout, exit_code = suzaku_driver.utils.executor.execute(*cmd)
    logger.info("set boot device : %s : %d", stdout, exit_code)

def power_on(ip, username, password):
    cmd = (EXECUTABLE_FILE, 
        "-I", "lanplus", 
        "-H", ip, 
        "-U", username, 
        "-P", password, 
        "chassis", "power", "on")
    stdout, exit_code = suzaku_driver.utils.executor.execute(*cmd)
    logger.info("power on : %s : %d", stdout, exit_code)

def power_off(ip, username, password):
    cmd = (EXECUTABLE_FILE, 
        "-I", "lanplus", 
        "-H", ip, 
        "-U", username, 
        "-P", password, 
        "chassis", "power", "off")
    stdout, exit_code = suzaku_driver.utils.executor.execute(*cmd)
    logger.info("power off : %s : %d", stdout, exit_code)

def power_reset(ip, username, password):
    cmd = (EXECUTABLE_FILE, 
        "-I", "lanplus", 
        "-H", ip, 
        "-U", username, 
        "-P", password, 
        "chassis", "power", "reset")
    stdout, exit_code = suzaku_driver.utils.executor.execute(*cmd)
    logger.info("power reset : %s : %d", stdout, exit_code)