import asyncio
import collections


class ClientServerProtocol(asyncio.Protocol):
    STORAGE = collections.OrderedDict()

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, req):
        self.data = req.decode()[:-1]
        self.responce = self.processing_request().encode()
        self.transport.write(self.responce)

    def processing_request(self):
        try:
            self.command = self.data.split(' ')[0]
        except IndexError:
            return 'error\nwrong command\n\n'

        if self.command == 'get':
            return self._get()

        elif self.command == 'put':
            return self._put()

        else:
            return 'error\nwrong command\n\n'

    def _get(self):
        try:
            self.metric_name = self.data.split(' ')[1]
        except (IndexError):
            return 'error\nwrong command\n\n'

        if len(self.data.split(' ')) != 2:
            return 'error\nwrong command\n\n'

        else:
            return self._return_metrics()

    def _put(self):
        try:
            self.metric_name = self.data.split(' ')[1]
            self.metric_value = str(float(self.data.split(' ')[2]))
            self.timestamp = str(int(self.data.split(' ')[3]))
            assert len(self.data.split(' ')) == 4
        except (IndexError, AssertionError, ValueError):
            return 'error\nwrong command\n\n'
        else:
            return self._save_metrics()

    def _return_metrics(self):
        result = 'ok\n'
        if self.metric_name == '*':
            if len(STORAGE) > 0:
                for key in STORAGE:
                    for metric in STORAGE[key]:
                        result += f"{key} {' '.join(metric)}\n"
                return result + '\n'
            else:
                return 'ok\n\n'

        else:
            try:
                STORAGE[self.metric_name]
            except KeyError:
                return 'ok\n\n'
            else:
                for value in STORAGE[self.metric_name]:
                    result += f"{self.metric_name} {' '.join(value)}\n"
                return result + '\n'

    def _save_metrics(self):
        if self.metric_name not in STORAGE:
            STORAGE[self.metric_name] = []
            STORAGE[self.metric_name].append(
                    [self.metric_value, self.timestamp])
            return 'ok\n\n'

        elif [self.metric_value, self.timestamp] in STORAGE[self.metric_name]:
            return 'ok\n\n'

        else:
            for value in STORAGE[self.metric_name]:
                if value[1] == self.timestamp:
                    STORAGE[self.metric_name].remove([value[0], value[1]])
            STORAGE[self.metric_name].append(
                [self.metric_value, self.timestamp])
            return 'ok\n\n'


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(ClientServerProtocol, host, port)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
