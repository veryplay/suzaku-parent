#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import validators

import suzaku_driver.engine
import suzaku_driver.errors
from suzaku_driver.serialize import Serializable

logger = logging.getLogger(__name__)

OK = "OK"
ERROR = "ERROR"

COMMAND_SETS = {
    "Heart"                 : "suzaku_driver.command.common.Heart",
    "PingHost"              : "suzaku_driver.command.ping.PingHost",
    "SetPXEBoot"            : "suzaku_driver.command.oob.SetPXEBoot",
    "SetDiskBoot"           : "suzaku_driver.command.oob.SetDiskBoot",
    "PowerOn"               : "suzaku_driver.command.oob.PowerOn",
    "PowerOff"              : "suzaku_driver.command.oob.PowerOff",
    "PowerReset"            : "suzaku_driver.command.oob.PowerReset"
}

class Command(Serializable):

    serializable_fields = ( 'sn', 'action', 'status', 'message')

    def __init__(self, sn, action, 
        engine,
        status = OK, message =None):
        # sn
        self.sn = sn
        assert hasattr(self, "sn") 
        assert self.sn is not None 
        assert self.sn is not ""
        self.serializable_fields

        # action
        self.action = action
        assert hasattr(self, "action") 
        assert self.action is not None 
        assert self.action is not ""
        
        # engine
        self.engine = engine
        assert hasattr(self, "engine")
        assert self.engine is not None
        assert isinstance(self.engine, suzaku_driver.engine.Engine)
        
        # status
        self.status = status
        assert hasattr(self, "status")
        assert self.status is not None 
        assert self.status is not ""
        
        # message
        self.message = message

        # data
        self.data = dict()

    def run(self):
        try:
            try:
                self.execute_before()
                self.execute()
                self.status = OK
                message = "run %s success." % self.__class__.__name__
                self.message = message
                logger.info(message)
            finally:
                self.execute_after()
        except Exception as e:
            self.status = ERROR
            message = "run %s failed : %s" % (
                self.__class__.__name__, str(e))
            logger.info(message, exc_info = 1)
            self.message = "run failed, %s" % str(e)
        self.engine.send_command(self)

    def execute_before(self):
        raise suzaku_driver.errors.CommandExecutionError(
            "%s not impl run_before method" % self.__class__.__name__)

    def execute(self):
        raise suzaku_driver.errors.CommandExecutionError(
            "%s not impl after_run method" % self.__class__.__name__)

    def execute_after(self):
        raise suzaku_driver.errors.CommandExecutionError(
            "%s not impl run_after method" % self.__class__.__name__)

class UnkownCommand(Command):
    """agent to scheduler command"""

    def __init__(self, **kwargs):
        super(UnkownCommand, self).__init__(
            action = self.__class__.__name__, 
            status = ERROR, **kwargs)

class JsonSerializeErrorCommand(Command):
    """agent to scheduler command"""

    def __init__(self, **kwargs):
        super(JsonSerializeErrorCommand, self).__init__(
            action = self.__class__.__name__, 
            status=ERROR, **kwargs)

class SystemErrorCommand(Command):
    """agent to scheduler command"""

    def __init__(self, **kwargs):
        super(SystemErrorCommand, self).__init__(
            action = self.__class__.__name__, 
            status = ERROR, **kwargs)

class Heart(Command):
    """agent to scheduler command"""

    def __init__(self, **kwargs):
        super(Heart, self).__init__(
            action = self.__class__.__name__, **kwargs)
