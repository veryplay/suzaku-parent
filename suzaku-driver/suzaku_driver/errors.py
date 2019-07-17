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

class SuzakuException(Exception):
    """Base class for errors generated in ironic-python-client."""
    # NOTE(JoshNang) `message` should not end with a period
    message = 'An error occurred in agent engine'
    details = 'An unexpected error occurred. Please try back later.'
    serializable_fields = ('type', 'message', 'details')

    def __init__(self, details=None, 
        *args, **kwargs):
        super(SteelException, self).__init__(*args, **kwargs)
        self.type = self.__class__.__name__
        if details:
            self.details = details

    def __str__(self):
        return "{}: {}: {}".format(self.type, self.message, self.details)

    def __repr__(self):
        return "{}('{}')".format(self.type, self.__str__())

class ProcessExecutionException(SuzakuException):

    def __init__(self, stdout=None, exit_code=None, cmd=None,
                 description=None):
        if exit_code is None:
            exit_code = '-'
        
        if description is None:
            description = "Unexpected error while running command."
        
        details = ('%(description)s\n'
                    'Command: %(cmd)s\n'
                    'Exit code: %(exit_code)s\n'
                    'Stdout: %(stdout)r') % {
                        'description': description,
                        'cmd': cmd,
                        'exit_code': exit_code,
                        'stdout': stdout}

        super(ProcessExecutionException, self).__init__(details)
        self.stdout = stdout
        self.exit_code = exit_code
        self.cmd = cmd
        self.description = description

class NoRootPermissionException(ProcessExecutionException):
    
    def __init__(self, **kwargs):
        super(NoRootPermissionException, self).__init__(**kwargs)


class CommandExecutionException(SuzakuException):
    """Error raised when a command fails to execute."""

    message = 'Command execution failed'

    def __init__(self, details):
        super(CommandExecutionException, self).__init__(details)

class UnknownArgumentException(SuzakuException):

    message = 'unknow argument'

    def __init__(self, details):
        super(UnknownArgumentException, self).__init__(details)
