#!/usr/bin/env python
# -*- coding: utf-8 -*-

import errno
import os
import logging
from monotonic import monotonic as now
import six
import subprocess
import time
import suzaku_driver.utils.encode
import suzaku_driver.utils.reflection
from suzaku_driver.errors import ProcessExecutionException, UnknownArgumentException, NoRootPermissionException

logger = logging.getLogger(__name__)

def try_execute(*cmd, **kwargs):
    """The same as execute but returns None on error.

    Executes and logs results from a system command. See docs for
    oslo_concurrency.processutils.execute for usage.

    Instead of raising an exception on failure, this method simply
    returns None in case of failure.

    :param *cmd: positional arguments to pass to processutils.execute()
    :param log_stdout: keyword-only argument: whether to log the output
    :param **kwargs: keyword arguments to pass to processutils.execute()
    :raises: UnknownArgumentException on receiving unknown arguments
    :returns: tuple of (stdout, stderr) or None in some error cases
    """
    try:
        return execute(*cmd, **kwargs)
    except (ProcessExecutionException, OSError) as e:
        logger.debug('Command failed: %s', e)

def execute(*cmd, **kwargs):
    """Helper method to shell out and execute a command through subprocess.

    Allows optional.
    
    :param cmd:             Passed to subprocess.Popen.
    :type cmd:              string

    :param cwd:             Set the current working directory
    :type cwd:              string

    :type std_input:        string or bytes

    :param env_variables:   Environment variables and their values that
                            will be set for the process.
    :type env_variables:    dict

    :param check_exit_code: Single bool, int, or list of allowed exit
                            codes.  Defaults to [0].  Raise
                            :class:`ProcessExecutionException` unless
                            program exits with one of these code.
    :type check_exit_code:  boolean, int, or [int]


    :param delay_on_retry:  True | False. Defaults to True. If set to True,
                            wait a short amount of time before retrying.
    :type delay_on_retry:   boolean

    :param attempts_times:  How many times to retry cmd.
    :type attempts_times:   int

    :param run_as_root:     True | False. Defaults to False. If set to True,
                            the command is prefixed by the command specified
                            in the root_helper kwarg.
    :type run_as_root:      boolean

    :param shell:           whether or not there should be a shell used to
                            execute this command. Defaults to True.
    :type shell:            boolean

    :param binary:          On Python 3, return stdout and stderr as bytes if
                            binary is True, as Unicode otherwise.
    :type binary:           boolean

    :param use_standard_locale: keyword-only argument. True | False.
                            Defaults to True. If set to True,
                            execute command with standard locale
                            added to environment variables.
    :type                   boolean

    :param logger_limit     max stdout to logger
    :type logger_limit      boolean

    :returns:               (status, stdout, stderr) from process execution
    """

    cmd = [str(c) for c in cmd]
    cmd_text = ' '.join(cmd)
    use_standard_locale = kwargs.pop('use_standard_locale', True)
    if use_standard_locale:
        env = kwargs.pop('env_variables', os.environ.copy())
        env['LC_ALL'] = 'C'
        kwargs['env_variables'] = env

    cwd = kwargs.pop('cwd', None)

    std_input = kwargs.pop('std_input', None)
    if std_input is not None:
        std_input = suzaku_driver.utils.encode.to_utf8(std_input)

    env_variables = kwargs.pop('env_variables', None)

    ignore_exit_code = False
    check_exit_code = kwargs.pop('check_exit_code', [0])
    if isinstance(check_exit_code, bool):
        ignore_exit_code = not check_exit_code
        check_exit_code = [0]
    elif isinstance(check_exit_code, int):
        check_exit_code = [check_exit_code]

    delay_on_retry = kwargs.pop('delay_on_retry', True)

    attempts_times = kwargs.pop('attempts_times', 1)

    run_as_root = kwargs.pop('run_as_root', False)
    if run_as_root and hasattr(os, 'geteuid') and os.geteuid() != 0:
        raise NoRootPermissionException(
            cmd = cmd_text,
            description='Command requested root, but did not '
                      'specify a root helper.')

    shell = kwargs.pop('shell', False)

    binary = kwargs.pop('binary', False)

    enable_logger_limit = kwargs.pop('enable_logger_limit', False)
    logger_limit_bytes = kwargs.pop('logger_limit_bytes', 500)

    if kwargs:
        raise UnknownArgumentException('Got unknown keyword args: %r' % kwargs)

    watch = StopWatch()
    temp_attempts_times = attempts_times
    while temp_attempts_times > 0:
        temp_attempts_times -= 1
        watch.restart()

        logger.info("ready to run %s", cmd_text)
        try:
            _PIPE = subprocess.PIPE
            obj = subprocess.Popen(cmd,
                                stdin=_PIPE,
                                stdout=_PIPE,
                                stderr=subprocess.STDOUT,
                                close_fds=True,
                                preexec_fn=None,
                                shell=shell,
                                cwd=cwd,
                                env=env_variables)
            result = obj.communicate(std_input)
            obj.stdin.close()
            exit_code = obj.returncode

            (stdout, _) = result
            if six.PY3:
                stdout = os.fsdecode(stdout)
            if exit_code != 0:
                raise ProcessExecutionException(exit_code = exit_code,
                    stdout = stdout,
                    cmd = cmd_text)
            if enable_logger_limit:
                logger.info("execute `%s` completely, exit code : %d, stdout : \n%s ......", 
                    cmd_text, exit_code, stdout[:logger_limit_bytes])
            else:
                logger.info("execute `%s` completely, exit code : %d, stdout : \n%s", 
                    cmd_text, exit_code, stdout)
            return (stdout, exit_code)
        except (ProcessExecutionException, OSError) as e:
            if isinstance(e, ProcessExecutionException):
                logger.error(
                    "%(desc)r\ncommand: %(cmd)r\nexit code: %(code)r\n' \
                    stdout: %(stdout)r\n" % {
                        "desc": e.description,
                        "cmd": e.cmd,
                        "code": e.exit_code,
                        "stdout": e.stdout
                    })
            else:
                logger.error('Got an OSError, command: %(cmd)r, errno: %(errno)r' % {
                        "cmd": cmd_text,
                        "errno": e.strerror})
            if delay_on_retry and temp_attempts_times > 0:
                attempts_period = 0.5 * 2 ** (attempts_times - temp_attempts_times)
                logger.info("retry to run `%s` after %.2f seconds" % (cmd, attempts_period))
                time.sleep(attempts_period)
                continue
            raise
            
        finally:
            # NOTE(termie): this appears to be necessary to let the subprocess
            #               call clean something up in between calls, without
            #               it two execute calls in a row hangs the second one
            # NOTE(bnemec): termie's comment above is probably specific to the
            #               eventlet subprocess module, but since we still
            #               have to support that we're leaving the sleep.  It
            #               won't hurt anything in the stdlib case anyway.
            time.sleep(0)


class Split(object):
    """A *immutable* stopwatch split.

    See: http://en.wikipedia.org/wiki/Stopwatch for what this is/represents.

    .. versionadded:: 1.4
    """

    __slots__ = ['_elapsed', '_length']

    def __init__(self, elapsed, length):
        self._elapsed = elapsed
        self._length = length

    @property
    def elapsed(self):
        """Duration from stopwatch start."""
        return self._elapsed

    @property
    def length(self):
        """Seconds from last split (or the elapsed time if no prior split)."""
        return self._length

    def __repr__(self):
        r = suzaku_driver.utils.reflection.get_class_name(self, fully_qualified=False)
        r += "(elapsed=%s, length=%s)" % (self._elapsed, self._length)
        return r
    
class StopWatch(object):
    """A simple timer/stopwatch helper class.

    Inspired by: apache-commons-lang java stopwatch.

    Not thread-safe (when a single watch is mutated by multiple threads at
    the same time). Thread-safe when used by a single thread (not shared) or
    when operations are performed in a thread-safe manner on these objects by
    wrapping those operations with locks.

    It will use the `monotonic`_ pypi library to find an appropriate
    monotonically increasing time providing function (which typically varies
    depending on operating system and python version).

    .. _monotonic: https://pypi.org/project/monotonic/

    .. versionadded:: 1.4
    """
    _STARTED = 'STARTED'
    _STOPPED = 'STOPPED'

    def __init__(self, duration=None):
        if duration is not None and duration < 0:
            raise ValueError("Duration must be greater or equal to"
                             " zero and not %s" % duration)
        self._duration = duration
        self._started_at = None
        self._stopped_at = None
        self._state = None
        self._splits = ()

    def start(self):
        """Starts the watch (if not already started).

        NOTE(harlowja): resets any splits previously captured (if any).
        """
        if self._state == self._STARTED:
            return self
        self._started_at = now()
        self._stopped_at = None
        self._state = self._STARTED
        self._splits = ()
        return self

    @property
    def splits(self):
        """Accessor to all/any splits that have been captured."""
        return self._splits

    def split(self):
        """Captures a split/elapsed since start time (and doesn't stop)."""
        if self._state == self._STARTED:
            elapsed = self.elapsed()
            if self._splits:
                length = self._delta_seconds(self._splits[-1].elapsed, elapsed)
            else:
                length = elapsed
            self._splits = self._splits + (Split(elapsed, length),)
            return self._splits[-1]
        else:
            raise RuntimeError("Can not create a split time of a stopwatch"
                               " if it has not been started or if it has been"
                               " stopped")

    def restart(self):
        """Restarts the watch from a started/stopped state."""
        if self._state == self._STARTED:
            self.stop()
        self.start()
        return self

    @staticmethod
    def _delta_seconds(earlier, later):
        # Uses max to avoid the delta/time going backwards (and thus negative).
        return max(0.0, later - earlier)

    def elapsed(self, maximum=None):
        """Returns how many seconds have elapsed."""
        if self._state not in (self._STARTED, self._STOPPED):
            raise RuntimeError("Can not get the elapsed time of a stopwatch"
                               " if it has not been started/stopped")
        if self._state == self._STOPPED:
            elapsed = self._delta_seconds(self._started_at, self._stopped_at)
        else:
            elapsed = self._delta_seconds(self._started_at, now())
        if maximum is not None and elapsed > maximum:
            elapsed = max(0.0, maximum)
        return elapsed

    def __enter__(self):
        """Starts the watch."""
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        """Stops the watch (ignoring errors if stop fails)."""
        try:
            self.stop()
        except RuntimeError:  # nosec: errors are meant to be ignored
            pass

    def leftover(self, return_none=False):
        """Returns how many seconds are left until the watch expires.

        :param return_none: when ``True`` instead of raising a ``RuntimeError``
                            when no duration has been set this call will
                            return ``None`` instead.
        :type return_none: boolean
        """
        if self._state != self._STARTED:
            raise RuntimeError("Can not get the leftover time of a stopwatch"
                               " that has not been started")
        if self._duration is None:
            if not return_none:
                raise RuntimeError("Can not get the leftover time of a watch"
                                   " that has no duration")
            return None
        return max(0.0, self._duration - self.elapsed())

    def expired(self):
        """Returns if the watch has expired (ie, duration provided elapsed)."""
        if self._state not in (self._STARTED, self._STOPPED):
            raise RuntimeError("Can not check if a stopwatch has expired"
                               " if it has not been started/stopped")
        if self._duration is None:
            return False
        return self.elapsed() > self._duration

    def has_started(self):
        """Returns True if the watch is in a started state."""
        return self._state == self._STARTED

    def has_stopped(self):
        """Returns True if the watch is in a stopped state."""
        return self._state == self._STOPPED

    def resume(self):
        """Resumes the watch from a stopped state."""
        if self._state == self._STOPPED:
            self._state = self._STARTED
            return self
        else:
            raise RuntimeError("Can not resume a stopwatch that has not been"
                               " stopped")

    def stop(self):
        """Stops the watch."""
        if self._state == self._STOPPED:
            return self
        if self._state != self._STARTED:
            raise RuntimeError("Can not stop a stopwatch that has not been"
                               " started")
        self._stopped_at = now()
        self._state = self._STOPPED
        return self
