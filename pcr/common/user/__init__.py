from socket import socket
from dataclasses import dataclass

@dataclass
class User:

    name: str
    
    private_key: str = None
    public_key: str = None
    connection: socket = None

    def send(self, packet):
        self.connection.send(packet)


    def raw(self):
        return self.__dict__.copy()
        