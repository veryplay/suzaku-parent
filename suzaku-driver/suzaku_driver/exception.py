#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)


class InvalidArgumentException(Exception):

    def __init__(self, message=None):
        super(InvalidArgumentException, self).__init__(message)

class UnknownArgumentException(Exception):

    def __init__(self, message=None):
        super(UnknownArgumentException, self).__init__(message)

class UnsupportDeviceException(Exception):

    def __init__(self, message=None):
        super(UnsupportDeviceException, self).__init__(message)

class IncompatibleHardwareMethodError(Exception):
    """Error raised when HardwareManager method incompatible with hardware."""

    message = 'HardwareManager method is not compatible with hardware'

    def __init__(self, message=None):
        super(IncompatibleHardwareMethodError, self).__init__(message)

class ProcessExecutionException(Exception):

    def __init__(self, stdout=None, exit_code=None, cmd=None,
                 description=None):
        super(ProcessExecutionException, self).__init__(
            stdout, exit_code, cmd, description)
        self.stdout = stdout
        self.exit_code = exit_code
        self.cmd = cmd
        self.description = description

    def __str__(self):
        description = self.description
        if description is None:
            description = "Unexpected error while running command."

        exit_code = self.exit_code
        if exit_code is None:
            exit_code = '-'

        message = ('%(description)s\n'
                    'Command: %(cmd)s\n'
                    'Exit code: %(exit_code)s\n'
                    'Stdout: %(stdout)r') % {'description': description,
                                             'cmd': self.cmd,
                                             'exit_code': exit_code,
                                             'stdout': self.stdout}
        return message

class NoRootPermissionException(ProcessExecutionException):
    def __init__(self, **kwargs):
        super(NoRootPermissionException, self).__init__(**kwargs)

class SuzakuException(Exception):
    """Base Suzaku Exception

    To correctly use this class, inherit from it and define
    a 'message' property. That message will get printf'd
    with the keyword arguments provided to the constructor.

    """
    message = "An unknown exception occurred."

    def __init__(self, message=None):
        if message is None:
            message = self.message
        super(SuzakuException, self).__init__(message)