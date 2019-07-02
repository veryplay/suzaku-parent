#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import importlib
import os
import Queue
from Queue import Empty
import signal
import sys
import tempfile
from threading import Timer
from threading import Condition
import time
import thread
import threading

import suzaku_driver.command.common
import suzaku_driver.errors
import suzaku_driver.lifecycle
import suzaku_driver.rabbitmq

from suzaku_driver.exception import ProcessExecutionException

logger = logging.getLogger(__name__)

class Engine(suzaku_driver.lifecycle.LifeCycle):

    DEFAULT_HEART_PERIOD = 30

    def __init__(self, config):
        super(Engine, self).__init__()
        self.config = config
        heart_period = config["heart"]["period"]
        if heart_period and str(heart_period).isdigit():
            self.heart_period = int(heart_period)
        else:
            logger.error("heart_period is not int type, use default %d", \
                self.DEFAULT_HEART_PERIOD)
            self.heart_period = self.DEFAULT_HEART_PERIOD
        logger.info("use heart period : %d", heart_period)

        self.serial_number = config["mq"]["receive_routing_key"]
        self.subscribe_queue = Queue.Queue()
        self.publish_queue = Queue.Queue()
        self.encoder = suzaku_driver.serialize.DefaultJsonEncoder()
        self.decoder = suzaku_driver.serialize.DefaultJsonDecoder()

        self.heart_thread_singal = threading.Event()
        self.command_process_thread_singal = threading.Event()
        
    def do_start(self):
        self._bind_signal()

        # rabbitmq
        self.rabbitmq = suzaku_driver.rabbitmq.Broker(self.config, self.subscribe_queue, 
            self.publish_queue, self.serial_number)
        self.rabbitmq.start()

        # command thread
        self.command_process_thread = threading.Thread(group = None, 
            target = self.command_process_thread_run, 
            name = "CommandProcessThread")
        self.command_process_thread.start()

        # heart thread
        self.heart_thread = threading.Thread(group = None, 
            target = self.heart_thread_run,
            name = "HeartThread")
        self.heart_thread.start()


    def do_stop(self):
        self._unbind_signal()

        # heart thread
        self.heart_thread_singal.set()
        if (hasattr(self, "heart_thread")
            and self.heart_thread 
            and self.heart_thread.isAlive()):
            self.heart_thread.join(1)
            if self.heart_thread.isAlive():
                logger.warn("%s stop timeout.", self.heart_thread.getName())
            logger.info("%s stoped.", self.heart_thread.getName())
        
        # command process thread
        self.command_process_thread_singal.set()
        if (hasattr(self, "command_process_thread") 
            and self.command_process_thread 
            and self.command_process_thread.isAlive()):
            self.command_process_thread.join(1)
            if self.command_process_thread.isAlive():
                logger.warn("%s stop timeout.", self.command_process_thread.getName())
            logger.info("%s stoped.", self.command_process_thread.getName())
        
        if self.rabbitmq:
            self.rabbitmq.stop()

    def _bind_signal(self):
        # bind signal
        self.hold_sigint = signal.signal(signal.SIGINT, self._handler_signal)
        self.hold_sigterm = signal.signal(signal.SIGTERM, self._handler_signal)
    
    def _unbind_signal(self):
        # unbind signal
        signal.signal(signal.SIGINT, self.hold_sigint)
        signal.signal(signal.SIGTERM, self.hold_sigterm)

    def _handler_signal(self, signum, frame):
        logger.info("receive a kill signal %s=%s.", signum, frame)
        self.stop()

    def get_subscribe_queue(self):
        return self.subscribe_queue
    
    def get_publish_queue(self):
        return self.publish_queue

    def send_command(self, cmd):
        self.publish_queue.put(self.encoder.encode(cmd))

    def heart_thread_run(self):
        while not self.should_stop():
            try:
                heart = suzaku_driver.command.common.Heart(sn = self.serial_number, 
                    engine  = self)
                self.publish_queue.put(self.encoder.encode(heart))
                logger.info("trigger a heart period %d.", self.heart_period)
                self.heart_thread_singal.wait(self.heart_period)
            except Exception:
                logger.error("generate heart command failed, ignore it. retry after %d seconds", 
                    self.heart_period, exc_info = 1)
        logger.info("%s stoped.", threading.current_thread().getName())
    
    def command_process_thread_run(self):
        while not self.should_stop():
            try:
                message = self.subscribe_queue.get(timeout = 0.2)
                if not message:
                    logger.warn("get a None messagpublish_queuee from subscribe_queue : %s", message)
                    continue
                directive = self.decoder.decode(message)
                if type(directive) is dict and directive.has_key("action"):
                    action = directive.get("action")
                    if suzaku_driver.command.common.COMMAND_SETS.has_key(action):
                        directive_clazz_string = suzaku_driver.command.common.COMMAND_SETS.get(action)
                        clazz_data = directive_clazz_string.split('.')
                        module_path = '.'.join(clazz_data[:-1])
                        clazz_name = clazz_data[-1]
                        module = importlib.import_module(module_path)
                        directive_clazz = getattr(module, clazz_name)
                        directive_object = directive_clazz(engine = self, **directive)
                        directive_object.run()
                        continue
                logger.error("unknow command action : %s", message)
                cmd = suzaku_driver.command.common.UnkownCommand(sn = self.serial_number, 
                    engine = self, message = message)
                self.publish_queue.put(self.encoder.encode(cmd))
            except ValueError as e:
                message = ("%s : %s") % (message, str(e))
                cmd = suzaku_driver.command.common.JsonSerializeErrorCommand(
                    sn = self.serial_number, engine = self, message = message)
                self.publish_queue.put(self.encoder.encode(cmd))
                logger.error("decode directive failed, ignore it. %s", 
                    message,  exc_info = 1)
                continue
            except Empty:
                continue
            except Exception as e:
                message = ("%s : %s") % (message, str(e))
                cmd = suzaku_driver.command.common.SystemErrorCommand(
                    sn = self.serial_number, engine = self, message = message)
                self.publish_queue.put(self.encoder.encode(cmd))
                logger.error("process message failed : %s", 
                    message, exc_info = 1)
                continue
        logger.info("%s stoped.", threading.current_thread().getName())