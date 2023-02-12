import pika
import queue
import threading
import os

class AmqpConnectionPool:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, max_connections=20, timeout=60):
        self.host = os.environ.get('MQ_URL') if 'MQ_URL' in os.environ else os.environ.get('CLOUDAMQP_URL')
        self.max_connections = max_connections
        self.connections = queue.Queue(max_connections)
        self.wait_queue = queue.Queue()
        self.lock = threading.Lock()
        self.timeout = timeout

    def get_connection(self):
        with self.lock:
            if self.connections.qsize() < self.max_connections:
                connection = self._create_connection()
                self.connections.put(connection)
                return connection

            # Wait for a connection to be released
            try:
                connection = self.wait_queue.get(timeout=self.timeout)
                self.wait_queue.task_done()

                if not connection.is_open or connection.is_closing:
                    self.remove_connection(connection)
                    return self.get_connection()

                return connection
            except queue.Empty:
                raise Exception("Timeout reached while waiting for a connection to become available")

    def release_connection(self, connection):
        with self.lock:
            self.connections.put(connection)

    def remove_connection(self, connection):
        with self.lock:
            self.connections.queue.remove(connection)

    def _create_connection(self):
        parameters = pika.URLParameters(self.host)
        connection = pika.BlockingConnection(parameters)
        return connection
