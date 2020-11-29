import socket
import time


class ClientError(Exception):
    pass


class Client():
    """
    The Client class in which the connection is encapsulated
    with the server, a client socket is created and methods
    for receiving (get) and sending (put)
    metrics to the server.  Sending and receiving data in get and put methods
    implemented in accordance with the text protocol.
    The host and port address pair is passed to the constructor
    of the Client class, and an optional timeout argument.
    The connection to the server is established
    when an instance of the Client class is created
    and does not break between requests
    """
    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.data = {}
        self.sock = socket.create_connection((self.host, self.port))
        self.sock.settimeout(self.timeout)

    def put(self, metric_name, metric_value, timestamp=None):
        """
        Send metric to server used dedicated text API
        (command, metric name, metric value)
        Example:
        put eardrum.cpu 2.0 115086428
        """
        self.metric_name = metric_name
        self.metric_value = metric_value

        if not timestamp:
            self.timestamp = int(time.time())
        else:
            self.timestamp = timestamp
        self.req = f"put {self.metric_name} {self.metric_value} {self.timestamp}\n"

        try:
            sock.sendall(self.req.encode("utf-8"))
        except (socket.error, socket.timeout):
            raise ClientError

    def get(self, metric_name):
        """
        Get metrics from the server used dedicated text API
        (command, metric name).
        Use '*' for get all metrics from server
        Example:
        get eardrum.cpu
        get *
        """
        self.metric_name = metric_name
        request = f"get {self.metric_name}\n"

        try:
            self.sock.sendall(request.encode("utf-8"))
            self.responce = self.sock.recv(1024).decode("utf-8")
            if self.responce[0:1] != 'ok':
                raise ClientError
            elif self.responce == "ok\n\n":
                return {}
        except (socket.error, socket.timeout):
            raise ClientError

        try:
            self.metrics_array = [a.split(" ") for a in self.responce[3:-4].split("\n")]
            for metric in self.metrics_array:
                """
                Create dictionary where keys are metrics names
                and values (timestamp and value of metric) stores in list of tuples.
                Values are sorted by timestamp.
                """
                try:
                    if self.data[metric[0]]:
                            self.data[metric[0]].append(
                                (int(metric[2]), float(metric[1])))

                            self.data[metric[0]].sort(key=lambda x: (x[0], x[1]))
                except KeyError:
                    self.data[metric[0]] = [(int(metric[2]), float(metric[1]))]

        except (IndexError, ValueError):
            raise ClientError

        return self.data

try:
    responce = [a.split(" ") for a in resp2[3:-4].split("\n")]
    for metric in responce:
        try:
            if data[metric[0]]:
                data[metric[0]].append((int(metric[2]), float(metric[1])))
                data[metric[0]].sort(key=lambda x: (x[0], x[1]))
        except KeyError:
            data[metric[0]] = [(int(metric[2]), float(metric[1]))]
except (IndexError, ValueError):
    raise ClientError
