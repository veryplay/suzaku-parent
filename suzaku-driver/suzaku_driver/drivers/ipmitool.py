#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import suzaku_driver.utils.executor
from suzaku_driver.drivers.oob_adapter import OutOfBondAdapter


logger = logging.getLogger(__name__)

EXECUTABLE_FILE = "/usr/bin/ipmitool"

class IPMITool(OutOfBondAdapter):

    OUT_OF_BOND_PROTOCOL = "ipmi"

    def set_boot_device(self, ip, username, password, boot_device):
        '''
        set fisrt boot device of bios

        :param boot_device: see suzaku_driver.drivers.boot_deivce
        '''
        cmd = (EXECUTABLE_FILE, 
            "-I", "lanplus", 
            "-H", ip, 
            "-U", username, 
            "-P", password, 
            "chassis", "bootdev", boot_device)
        stdout, exit_code = suzaku_driver.utils.executor.execute(*cmd)
        logger.info("set boot device : %s : %d", stdout, exit_code)

    def power_on(self, ip, username, password):
        cmd = (EXECUTABLE_FILE, 
            "-I", "lanplus", 
            "-H", ip, 
            "-U", username, 
            "-P", password, 
            "chassis", "power", "on")
        stdout, exit_code = suzaku_driver.utils.executor.execute(*cmd)
        logger.info("power on : %s : %d", stdout, exit_code)

    def power_off(self, ip, username, password):
        cmd = (EXECUTABLE_FILE, 
            "-I", "lanplus", 
            "-H", ip, 
            "-U", username, 
            "-P", password, 
            "chassis", "power", "off")
        stdout, exit_code = suzaku_driver.utils.executor.execute(*cmd)
        logger.info("power off : %s : %d", stdout, exit_code)

    def power_reset(self, ip, username, password):
        cmd = (EXECUTABLE_FILE, 
            "-I", "lanplus", 
            "-H", ip, 
            "-U", username, 
            "-P", password, 
            "chassis", "power", "reset")
        stdout, exit_code = suzaku_driver.utils.executor.execute(*cmd)
        logger.info("power reset : %s : %d", stdout, exit_code)