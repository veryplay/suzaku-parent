#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time

from suzaku_driver.command.common import Command
import suzaku_driver.drivers.boot_devices as boot_devices
from suzaku_driver.drivers.oob_adapter_factory import OutOfBondAdapterFactory

logger = logging.getLogger(__name__)

class SetPXEBoot(Command):
    """scheduler to agent command"""

    serializable_fields = Command.serializable_fields + (
        'ilo_ip', 'username', 'password')

    def __init__(self, ilo_ip, username, password, **kwargs):
        super(SetPXEBoot, self).__init__(**kwargs)

        # ilo_ip
        self.ilo_ip = ilo_ip
        assert hasattr(self, "ilo_ip")
        assert self.ilo_ip is not None
        assert self.ilo_ip is not ""

        # username
        self.username = username
        assert hasattr(self, "username")
        assert self.username is not None
        assert self.username is not ""

        # password
        self.password = password
        assert hasattr(self, "password")
        assert self.password is not None
        assert self.password is not ""

        engine = self.engine
        self.oob_adapter_factory = OutOfBondAdapterFactory(engine)

    def execute_before(self):
        pass
    
    def execute(self):
        oob_adapter = self.oob_adapter_factory.get_out_of_bond_adapter()

        ilo_ip = self.ilo_ip
        username = self.username
        password = self.password
        oob_adapter.set_boot_device(ilo_ip, username, 
            password, boot_devices.PXE)
        time.sleep(3)

        oob_adapter.power_on(ilo_ip, username, password)
        time.sleep(3)
        
        oob_adapter.power_reset(ilo_ip, username, password)
        time.sleep(3)
        logger.info("set %s pxe boot completely", ilo_ip)
    
    def execute_after(self):
        pass


class SetDiskBoot(Command):
    """scheduler to agent command"""

    serializable_fields = Command.serializable_fields + (
        'ilo_ip', 'username', 'password')

    def __init__(self, ilo_ip, username, password, **kwargs):
        super(SetDiskBoot, self).__init__(**kwargs)

        # ilo_ip
        self.ilo_ip = ilo_ip
        assert hasattr(self, "ilo_ip")
        assert self.ilo_ip is not None
        assert self.ilo_ip is not ""

        # username
        self.username = username
        assert hasattr(self, "username")
        assert self.username is not None
        assert self.username is not ""

        # password
        self.password = password
        assert hasattr(self, "password")
        assert self.password is not None
        assert self.password is not ""

        engine = self.engine
        self.oob_adapter_factory = OutOfBondAdapterFactory(engine)

    def execute_before(self):
        pass

    def execute(self):
        oob_adapter = self.oob_adapter_factory.get_out_of_bond_adapter()

        ilo_ip = self.ilo_ip
        username = self.username
        password = self.password
        oob_adapter.set_boot_device(ilo_ip, username,
                                 password, boot_devices.DISK)
        time.sleep(3)

        oob_adapter.power_on(ilo_ip, username, password)
        time.sleep(3)
        
        oob_adapter.power_reset(ilo_ip, username, password)
        time.sleep(3)
        logger.info("set %s disk boot completely", ilo_ip)

    def execute_after(self):
        pass

class PowerOff(Command):
    """scheduler to agent command"""

    serializable_fields = Command.serializable_fields + (
        'ilo_ip', 'username', 'password')

    def __init__(self, ilo_ip, username, password, **kwargs):
        super(PowerOff, self).__init__(**kwargs)

        # ilo_ip
        self.ilo_ip = ilo_ip
        assert hasattr(self, "ilo_ip")
        assert self.ilo_ip is not None
        assert self.ilo_ip is not ""

        # username
        self.username = username
        assert hasattr(self, "username")
        assert self.username is not None
        assert self.username is not ""

        # password
        self.password = password
        assert hasattr(self, "password")
        assert self.password is not None
        assert self.password is not ""

        engine = self.engine
        self.oob_adapter_factory = OutOfBondAdapterFactory(engine)

    def execute_before(self):
        pass
    
    def execute(self):
        oob_adapter = self.oob_adapter_factory.get_out_of_bond_adapter()
        
        ilo_ip = self.ilo_ip
        username = self.username
        password = self.password
        oob_adapter.power_off(ilo_ip, username, password)
        time.sleep(3)
        logger.info("set %s power off completely")
    
    def execute_after(self):
        pass

class PowerOn(Command):
    """scheduler to agent command"""

    serializable_fields = Command.serializable_fields + (
        'ilo_ip', 'username', 'password')

    def __init__(self, ilo_ip, username, password, **kwargs):
        super(PowerOn, self).__init__(**kwargs)

        # ilo_ip
        self.ilo_ip = ilo_ip
        assert hasattr(self, "ilo_ip")
        assert self.ilo_ip is not None
        assert self.ilo_ip is not ""

        # username
        self.username = username
        assert hasattr(self, "username")
        assert self.username is not None
        assert self.username is not ""

        # password
        self.password = password
        assert hasattr(self, "password")
        assert self.password is not None
        assert self.password is not ""

        engine = self.engine
        self.oob_adapter_factory = OutOfBondAdapterFactory(engine)

    def execute_before(self):
        pass
    
    def execute(self):
        oob_adapter = self.oob_adapter_factory.get_out_of_bond_adapter()

        ilo_ip = self.ilo_ip
        username = self.username
        password = self.password
        oob_adapter.power_on(ilo_ip, username, password)
        time.sleep(3)
        logger.info("set %s power on completely")
    
    def execute_after(self):
        pass

class PowerReset(Command):
    """scheduler to agent command"""

    serializable_fields = Command.serializable_fields + (
        'ilo_ip', 'username', 'password')

    def __init__(self, ilo_ip, username, password, **kwargs):
        super(PowerReset, self).__init__(**kwargs)

        # ilo_ip
        self.ilo_ip = ilo_ip
        assert hasattr(self, "ilo_ip")
        assert self.ilo_ip is not None
        assert self.ilo_ip is not ""

        # username
        self.username = username
        assert hasattr(self, "username")
        assert self.username is not None
        assert self.username is not ""

        # password
        self.password = password
        assert hasattr(self, "password")
        assert self.password is not None
        assert self.password is not ""

        engine = self.engine
        self.oob_adapter_factory = OutOfBondAdapterFactory(engine)

    def execute_before(self):
        pass
    
    def execute(self):
        oob_adapter = self.oob_adapter_factory.get_out_of_bond_adapter()

        ilo_ip = self.ilo_ip
        username = self.username
        password = self.password
        oob_adapter.power_reset(ilo_ip, username, password)
        time.sleep(3)
        logger.info("set %s power on completely")
    
    def execute_after(self):
        pass
