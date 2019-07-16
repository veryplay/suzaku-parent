#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import validators

from suzaku_driver.command.common import Command
import suzaku_driver.utils.executor

logger = logging.getLogger(__name__)

class PingHost(Command):
    """scheduler to agent command"""

    serializable_fields = Command.serializable_fields + ('ip',)

    def __init__(self, ip, **kwargs):
        super(PingHost, self).__init__(**kwargs)

        # ip
        self.ip = ip
        assert hasattr(self, "ip")
        assert self.ip is not None
        assert self.ip is not ""

    def execute_before(self):
        pass

    def execute(self):
        ip = self.ip
        cmd = ["ping", "-c", "3", self.ip]
        suzaku_driver.utils.executor.execute(*cmd)
        logger.info("ping %s successfully", ip)

    def execute_after(self):
        pass
