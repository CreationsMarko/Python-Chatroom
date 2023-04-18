import socket

class ChatSocket(socket.socket):

    def __init__(self, *args, **kwargs):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM, *args, **kwargs)

    def receive(self):
        return super().recv(1024).decode('utf-8')

    def send(self, message: str):
        super().send( bytes(message, 'utf-8') )