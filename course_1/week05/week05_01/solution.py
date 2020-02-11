import socket
import time


class ClientError(socket.timeout):

    def __init__(self, error: str):
        self.error = error

    def __str__(self):
        return self.error

    def __repr__(self):
        return self.error


class Client:

    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        if timeout is not None:
            self.socket.settimeout(timeout)

    @staticmethod
    def _check_response_status(response):
        values = response.split('\n')
        if len(values) < 3:
            raise ClientError('Wrong response format!')
        status = values[0]
        if status != 'ok':
            raise ClientError('Status is not "OK"! Server response: {resp}'.format(resp=values[1]))

    def put(self, metric, value, timestamp=None):
        try:
            if timestamp is None:
                timestamp = int(time.time())
            self.socket.sendall(bytes('put {metric} {value} {timestamp}\n'
                                      .format(metric=metric, value=value, timestamp=timestamp),
                                      encoding='utf-8'))
            response = self.socket.recv(1024).decode("utf8")
            self._check_response_status(response)
        except socket.timeout:
            raise ClientError('Timeout excepted!')

    def get(self, metric):

        try:
            self.socket.sendall(bytes('get {metric}\n'.format(metric=metric), encoding='utf-8'))
            data = self.socket.recv(1024).decode("utf8")
            self._check_response_status(data)
        except socket.timeout:
            raise ClientError('Timeout excepted!')

        values = data.split('\n')
        results = dict()
        for v in values[1:-2]:
            splitted = v.split(' ')
            if len(splitted) != 3:
                raise ClientError('Metric must contains exactly 3 fields!')
            metric, value, timestamp = splitted
            metric_results = results.get(metric, [])
            try:
                metric_results.append((int(timestamp), float(value)))
            except ValueError:
                raise ClientError('Couldnt convert metric record to needed types!')
            results[metric] = metric_results

        for k, v in results.items():
            results[k] = sorted(v, key=lambda item: item[0])
        return results
