import asyncio
import argparse
from copy import deepcopy


class MetricsStorage:
    _instance = None
    storage = dict()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def put(cls, metric, value, timestamp):
        cls.storage[(metric, timestamp)] = value

    @classmethod
    def get(cls, metric_to_recieve):
        if metric_to_recieve == '*':
            return deepcopy(cls.storage)
        else:
            return {(metric, timestamp): value
                    for (metric, timestamp), value in cls.storage.items()
                    if metric == metric_to_recieve}

    @classmethod
    def __str__(cls):
        return cls.storage.__str__()


def process_data(data):
    try:
        command, payload = data.split(' ', 1)
    except ValueError:
        return 'error\nwrong command\n\n'
    payload = payload.strip()
    # print('Command: "{}"'.format(command))
    # print('Payload: "{}"'.format(payload))
    if command == 'put':
        try:
            metric, value, timestamp = payload.split(' ')
            value = float(value)
            timestamp = int(timestamp)
        except ValueError:
            return 'error\nwrong command\n\n'

        MetricsStorage.put(metric, value, timestamp)
        return 'ok\n\n'
    elif command == 'get':
        metrics = MetricsStorage.get(payload)
        if metrics:
            response = ['{} {} {}'.format(metric, value, timestamp)
                        for (metric, timestamp), value in metrics.items()]
            return 'ok\n{metrics}\n\n'.format(metrics='\n'.join(response))
        else:
            return 'ok\n\n'
    else:
        return 'error\nwrong command\n\n'


class ClientServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = process_data(data.decode())
        self.transport.write(resp.encode())


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        protocol_factory=ClientServerProtocol,
        host=host,
        port=port
    )

    server = loop.run_until_complete(coro)

    print('Start to run server!')
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='127.0.0.1')
    parser.add_argument('--port', type=int, default=8888)
    args = parser.parse_args()
    run_server(args.host, args.port)
