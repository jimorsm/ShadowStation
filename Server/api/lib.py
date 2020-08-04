import json
import socket

from .models import Account


class SSControl:
    def __init__(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.connection.connect(('127.0.0.1', 6000))

    def get_status(self) -> dict:
        msg = 'ping'
        # result = self._send_command(msg)
        result = json.loads(self._send_command(msg).split(' ')[1])
        return result

    def get_ports(self) -> list:
        result = [int(port) for port in self.get_status()]
        return result

    def add(self, port: int, password: str):
        msg = 'add: {}'.format(json.dumps(dict(server_port=port, password=password)))
        self._result_check(self._send_command(msg))

    def remove(self, port: int):
        msg = 'remove: {}'.format(json.dumps(dict(server_port=port)))
        self._result_check(self._send_command(msg))

    def update(self, old_port: int, new_port: int, password: str):
        self.remove(old_port)
        self.add(new_port, password)

    def sync(self):
        for port in self.get_ports():
            self.remove(port)
        for account in Account.objects.all():
            self.add(account.port, account.secret)

    def _send_command(self, msg):
        self.connection.send(bytes(msg, encoding='utf8'))
        self.connection.settimeout(1)
        try:
            r = self.connection.recv(1560).decode()
        except socket.timeout:
            return 'check ss-manager'
        return r

    def _result_check(self, msg):
        if msg != 'ok':
            return 'Wrong!' + msg
        else:
            return 'Succeed!'
