from ..common.chatsocket import ChatSocket
from socket import SOL_SOCKET, SO_REUSEADDR
from threading import Thread

from typing import Dict


def _rb(data: bytes):
    return data.decode('utf-8')

def _sb(data: str):
    return data.encode('utf-8')

class Server:

    sock: ChatSocket

    users = {}

    def __init__(self):
        self.sock = ChatSocket()
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    def start(self, host, port):
        self.sock.bind((host, port))
        self.sock.listen(5)

        while True:
            connection, address = self.sock.accept()

            process = Thread(
                target=self.await_messages, args=(connection, address))
            process.daemon = True
            process.start()


    def await_messages(self, connection, address):

        username = _rb(connection.recv(16))
        print(f"User '{username}' connected from IP {address}")

        self.users[connection] = username

        self.process_messages(connection)
    
    def process_messages(self, user):

        while True:
            message = _rb(user.recv(1024))
            if not message:
                del self.users[user]
                break
            print(f"User '{self.users[user]}' sent a message")

            receivers = [i for i in self.users.keys() if i != user]
            for receiver in receivers:
                receiver.send(_sb(f'{self.users[user]}: {message}'))
