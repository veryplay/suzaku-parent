#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
import logging
import pika
import time
import threading
from Queue import Empty

import suzaku_driver.lifecycle
logger = logging.getLogger(__name__)

DEFAULT_PROPERTIES = pika.BasicProperties(delivery_mode=2)

class Broker(suzaku_driver.lifecycle.LifeCycle):

    def __init__(self, config, 
        rx_queue, 
        tx_queue, 
        rx_queue_name):
        super(Broker, self).__init__()
        # host
        host = config["mq"]["host"]
        assert host is not None
        self.host = host

        # port
        port = config["mq"]["port"]
        assert port is not None
        self.port = port

        # username
        username = config["mq"]["username"]
        assert username is not None
        self.username = username

        # password
        password = config["mq"]["password"]
        assert password is not None
        self.password = password
        
        # vhost
        vhost = config["mq"]["vhost"]
        assert vhost is not None
        self.vhost = vhost
        
        # exchange
        exchange = config["mq"]["exchange"]
        assert exchange is not None
        self.exchange = exchange

        # exchange_type
        self.exchange_type = "direct"

        # system_vendor_info
        self.rx_queue_name = rx_queue_name
        # routing_key
        self.rx_routing_key = self.rx_queue_name

        self.rx_queue = rx_queue

        self.tx_queue_name = self.exchange

        self.tx_routing_key = self.exchange

        self.tx_queue = tx_queue
        # credentials
        self.credentials = pika.PlainCredentials(self.username, 
            self.password)
        
        # parameters
        self.parameters = pika.ConnectionParameters(
            host = self.host,
            port = self.port,
            virtual_host = self.vhost,
            credentials = self.credentials,
            connection_attempts = 1,
            retry_delay = 2,
            socket_timeout = 5,
            heartbeat = 20)

        # type: pika.connection.Connection
        self._rx_connection = None

        # type: pika.channel.Channel
        self._rx_channel = None

        self._consumer_tag = None

        # type: pika.connection.Connection
        self._tx_connection = None

        # type: pika.channel.Channel
        self._tx_channel = None

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if exception_type is not None:
            logger.error("%s, %s, %s", exception_type,
                exception_value, traceback)

    def _setup_connection(self, parameters):
        """This method connects to RabbitMQ, returning the connection handle.
        When the connection is established, the on_connection_open method
        will be invoked by pika.

        :rtype: pika.SelectConnection
        """
        logger.info('Connecting to %s', parameters)
        return pika.BlockingConnection(parameters = parameters)

    def _setup_channel(self, connection):
        return connection.channel()

    def setup_exchange(self, channel, exchange_name, exchange_type):
        """Setup the exchange on RabbitMQ by invoking the Exchange.Declare RPC
        command. When it is complete, the on_exchange_declareok method will
        be invoked by pika.

        :param str|unicode exchange_name: The name of the exchange to declare
        """
        logger.info('Declaring exchange : %s', exchange_name)
        # Note: using functools.partial is not required, it is demonstrating
        # how arbitrary data can be passed to the callback when it is called
        channel.exchange_declare(exchange=exchange_name,
            exchange_type=exchange_type,
            durable = True)

    def setup_queue(self, channel, queue_name):
        """Setup the queue on RabbitMQ by invoking the Queue.Declare RPC
        command. When it is complete, the on_queue_declareok method will
        be invoked by pika.

        :param str|unicode queue_name: The name of the queue to declare.
        """
        logger.info('Declaring queue %s', queue_name)
        channel.queue_declare(queue = queue_name, 
            durable = True,
            auto_delete = False)

    def bind_queue_to_exchange(self, channel, exchange, queue_name, routing_key):
        """Method invoked by pika when the Queue.Declare RPC call made in
        setup_queue has completed. In this method we will bind the queue
        and exchange together with the routing key by issuing the Queue.Bind
        RPC command. When this command is complete, the on_bindok method will
        be invoked by pika.

        :param pika.frame.Method method_frame: The Queue.DeclareOk frame
        :param str|unicode queue_name: Extra user data (queue name)
        """
        logger.info('Binding %s to %s with %s',
                    exchange, queue_name, routing_key)
        channel.queue_bind(queue=queue_name,
            exchange=exchange,
            routing_key=routing_key)

    def start_consuming(self, channel, rx_queue_name):
        """This method sets up the consumer by first calling
        add_on_cancel_callback so that the object is notified if RabbitMQ
        cancels the consumer. It then issues the Basic.Consume RPC command
        which returns the consumer tag that is used to uniquely identify the
        consumer with RabbitMQ. We keep the value to use it when we want to
        cancel consuming. The on_message method is passed in as a callback pika
        will invoke when a message is fully received.
        """
        if self.should_stop():
            logger.info("ready to stop, pause to consume")
            return
        logger.info('Issuing consumer related RPC commands')
        self._consumer_tag = channel.basic_consume(
            self.on_message, rx_queue_name, auto_ack = False)
        channel.start_consuming()

    def on_message(self, unused_channel, basic_deliver, properties, body):
        """Invoked by pika when a message is delivered from RabbitMQ. The
        channel is passed for your convenience. The basic_deliver object that
        is passed in carries the exchange, routing key, delivery tag and
        a redelivered flag for the message. The properties passed in is an
        instance of BasicProperties with the message properties and the body
        is the message that was sent.
        
        :param pika.channel.Channel unused_channel: The channel object
        :param pika.Spec.Basic.Deliver: basic_deliver method
        :param pika.Spec.BasicProperties: properties
        :param str|unicode body: The message body
        """
        logger.info('Received message # %s from %s: %s',
                    basic_deliver.delivery_tag, properties.app_id, body)
        self.rx_queue.put(body)
        self.acknowledge_message(unused_channel, basic_deliver.delivery_tag)

    def acknowledge_message(self, channel, delivery_tag):
        """Acknowledge the message delivery from RabbitMQ by sending a
        Basic.Ack RPC method for the delivery tag.
        
        :param int delivery_tag: The delivery tag from the Basic.Deliver frame
        """
        logger.info('Acknowledging message %s', delivery_tag)
        channel.basic_ack(delivery_tag)

    def _stop_consuming(self):
        """Tell RabbitMQ that you would like to stop consuming by sending the
        Basic.Cancel RPC command.
        """
        if self._rx_channel and self._rx_channel.is_open:
            logger.info('Sending a Basic.Cancel RPC command to RabbitMQ')
            self._rx_channel.basic_cancel(consumer_tag=self._consumer_tag)
        logger.info("stop consuming")

    def _close_channel(self, channel):
        """Call to close the channel with RabbitMQ cleanly by issuing the
        Channel.Close RPC command.
        """
        logger.info('Closing the channel')
        if channel and channel.is_open:
            channel.close()

    def _close_connection(self, connection):
        """This method closes the connection to RabbitMQ."""
        logger.info('Closing connection')
        if connection and connection.is_open:
            connection.close()

    def _subscribe_message(self):
        while not self.should_stop():
            try:
                self._rx_connection = self._setup_connection(self.parameters)
                self._rx_channel = self._setup_channel(self._rx_connection)
                self.setup_exchange(self._rx_channel, self.exchange, self.exchange_type)
                self.setup_queue(self._rx_channel, self.rx_queue_name)
                self.bind_queue_to_exchange(self._rx_channel, self.exchange, 
                    self.rx_queue_name, self.rx_routing_key)
                self._rx_channel.basic_qos(prefetch_count=1)

                logger.info('begin to subscribe message')
                self._consumer_tag = self._rx_channel.basic_consume(
                    queue = self.rx_queue_name, consumer_callback = self.on_message)
                self._rx_channel.start_consuming()
            # Do not recover if connection was closed by broker
            # Do not recover on channel errors
            except (KeyboardInterrupt, pika.exceptions.AMQPChannelError):
                break
            # Recover on all other connection errors
            except pika.exceptions.AMQPConnectionError as e:
                logger.error("connection error, try to reconnect after 1 seconds. %s", e, exc_info = 1)
                self._close_channel(self._rx_channel)
                self._rx_channel = None
                self._close_connection(self._rx_connection)
                self._rx_connection = None
                continue
            

    def _publish_message(self):
        while not self.should_stop():
            try:
                if not self._tx_connection:
                    self._tx_connection = self._setup_connection(self.parameters)
                    self._tx_channel = self._setup_channel(self._tx_connection)
                    self.setup_exchange(self._tx_channel, self.exchange, self.exchange_type)
                    self.setup_queue(self._tx_channel, self.tx_queue_name)
                    self.bind_queue_to_exchange(self._tx_channel, self.exchange, 
                        self.tx_queue_name, self.tx_routing_key)
                    self._tx_channel.confirm_delivery()
                    logger.info("initial tx connect completely.")


                message = self.tx_queue.get(timeout = 0.2)
                if not message:
                    logger.warn("get a None message from publish_queue.")
                    continue    
                if not hasattr(self, "_tx_channel") \
                    or not self._tx_channel \
                    or not self._tx_channel.is_open:
                    raise ConnectionNotInitialException("channel not initialed. ready to initiale it.")
                flag = self._tx_channel.basic_publish(exchange = self.exchange,
                        routing_key = self.tx_routing_key,
                        body = message,
                        properties=pika.BasicProperties(
                            content_type='application/json',
                            app_id=self.rx_queue_name,
                            delivery_mode = 2))
                if not flag:
                    logger.warn("message deliver failed, retry to deliver, flag = %s", flag)
                    self.tx_queue.put(message)
                else:
                    logger.info("deliver message to %s %s %s", 
                        self.exchange, self.tx_routing_key, message)
            except Empty:
                logger.debug("publish_queue is empty")
                continue
            # Do not recover if connection was closed by broker
            # Do not recover on channel errors
            except (KeyboardInterrupt, pika.exceptions.AMQPChannelError):
                break
            # Recover on all other connection errors
            except pika.exceptions.AMQPConnectionError as e:
                logger.error("connection error, try to reconnect after 1 seconds. %s", e, exc_info = 1)
                self._close_channel(self._tx_channel)
                self._tx_channel = None
                self._close_connection(self._tx_connection)
                self._tx_connection = None
                continue
            except Exception as e:
                logger.error("connection error, try to reconnect after 1 seconds. %s", e, exc_info = 1)
                self._close_channel(self._tx_channel)
                self._tx_channel = None
                self._close_connection(self._tx_connection)
                self._tx_connection = None
                continue

    def do_start(self):
        """Run the example consumer by connecting to RabbitMQ and then
        starting the IOLoop to block and allow the SelectConnection to operate.
        """
        threading.Thread(group = None, 
            target = self._subscribe_message, name = "RabbitMQSubscribeThread") .start()
        threading.Thread(group = None, 
            target = self._publish_message, name = "RabbitMQPublishThread").start()

    def do_stop(self):
        """Cleanly shutdown the connection to RabbitMQ by stopping the consumer
        with RabbitMQ. When RabbitMQ confirms the cancellation, on_cancelok
        will be invoked by pika, which will then closing the channel and
        connection. The IOLoop is started again because this method is invoked
        when CTRL-C is pressed raising a KeyboardInterrupt exception. This
        exception stops the IOLoop which needs to be running for pika to
        communicate with RabbitMQ. All of the commands issued prior to starting
        the IOLoop will be buffered but not processed.
        """
        logger.info('Stopping')
        self._stop_consuming()
        logger.info('Stopped')

class ConnectionNotInitialException(Exception):
    """Connection Not Initial Exception

    To correctly use this class, inherit from it and define
    a 'message' property. That message will get printf'd
    with the keyword arguments provided to the constructor.

    """
    message = "connection not initial."

    def __init__(self, message=None):
        if message is None:
            message = self.message
        super(ConnectionNotInitialException, self).__init__(message)
