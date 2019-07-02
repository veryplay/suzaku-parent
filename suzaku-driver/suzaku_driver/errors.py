#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2013 Rackspace, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import suzaku_driver.utils.encode


class EngineError(Exception):
    """Base class for errors."""
    # NOTE(JoshNang) `message` should not end with a period
    message = 'An error occurred in agent engine'
    details = 'An unexpected error occurred. Please try back later.'
    code = "EngineError"
    serializable_fields = ('type', 'code', 'message', 'details')

    def __init__(self, details=None, 
        *args, **kwargs):
        super(EngineError, self).__init__(*args, **kwargs)
        self.type = self.__class__.__name__
        if details:
            self.details = details

    def __str__(self):
        return "{}: {}: {}".format(self.code, self.message, self.details)

    def __repr__(self):
        return "{}('{}')".format(self.__class__.__name__, self.__str__())

class NoDHCPException(EngineError):
    """Error which occurs when a user supplies invalid content.

    Either because that content cannot be parsed according to the advertised
    `Content-Type`, or due to a content validation error.
    """
    details = "no dhcp exception, maybe network error."
    message = "no dhcp exception, maybe network error."
    code = "NoDHCPException"

    def __init__(self, details):
        super(NoDHCPException, self).__init__(details)

class InvalidContentError(EngineError):
    """Error which occurs when a user supplies invalid content.

    Either because that content cannot be parsed according to the advertised
    `Content-Type`, or due to a content validation error.
    """
    message = 'Invalid request body'
    details = message
    code = "InvalidContentError"

    def __init__(self, details):
        super(InvalidContentError, self).__init__(details)


class NotFound(EngineError):
    """Error which occurs if a non-existent APEngineErrorI endpoint is called."""
    message = 'Not found'
    code = "NotFound"
    details = 'The requested URL was not found.'

    def __init__(self, details):
        super(NotFound, self).__init__(details)


class CommandExecutionError(EngineError):
    """Error raised when a command fails to execute."""

    message = 'Command execution failed'
    details = message
    code = "CommandExecutionError"

    def __init__(self, details):
        super(CommandExecutionError, self).__init__(details)


class InvalidCommandError(InvalidContentError):
    """Error which is raised when an unknown command is issued."""

    message = 'Invalid command'
    details = message
    code = "InvalidCommandError"

    def __init__(self, details):
        super(InvalidCommandError, self).__init__(details)


class InvalidCommandParamsError(InvalidContentError):
    """Error which is raised when command parameters are invalid."""

    message = 'Invalid command parameters'
    details = message
    code = 'InvalidCommandParamsError'

    def __init__(self, details):
        super(InvalidCommandParamsError, self).__init__(details)