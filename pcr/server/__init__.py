
from socket import socket, SOL_SOCKET, SO_REUSEADDR
from threading import Thread

from ..common.user import User
from ..common.user.userlist import UserList
from ..common.packets import Packet, UserInitPacket, UserJoinPacket, UserMessagePacket, UserLeavePacket

class Server:

    sock: socket
    users: UserList

    def __init__(self):
        self.sock = socket()
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        self.users = UserList()

    def start(self, host, port):
        self.sock.bind((host, port))
        self.sock.listen(8)

        while True:
            connection, _ = self.sock.accept()

            process = Thread(
                target=self.packet_handler, args=(connection,))
            process.daemon = True
            process.start()



    def packet_handler(self, connection):

        while True:
            try:
                raw_packet = connection.recv(1024)
            except ConnectionResetError:
                continue
            if not raw_packet:
                continue

            packet = Packet.guess_packet(raw_packet)
            if not packet:
                continue

            if packet.type == 'user_join':
                self._initialize_user(connection, packet)
            if packet.type == 'user_message':
                self._process_message(packet)
            if packet.type == 'user_leave':
                self._remove_user(packet)
            #if packet.type == 'user_online':
            #    self.process_message(connection, packet)


    def _initialize_user(self, connection, data):

        if self.users.has_user(data.user['name']):
            return

        user = User(**data.user)
        #user.public_key = None
        user.connection = connection

        clean_user = User(**data.user)
        clean_user.private_key = None

        print(f"User '{user.name}' connected")

        self.users.send(UserJoinPacket(clean_user.raw()).encode())

        user_list = []
        for raw_user in self.users.users:
            clean_user = raw_user.raw()
            clean_user['connection'] = None
            clean_user['private_key'] = None
            user_list.append(clean_user)
        connection.send(UserInitPacket(user_list).encode())

        self.users.add(user)

    
    def _process_message(self, data):

        print(f"User '{data.username}' sent a message")

        for user in self.users.users:
            if user.name != data.username:
                user.send(data.encode())

    def _remove_user(self, data):

        user = self.users.from_private_key(data.private_key, None)
        if not user:
            return

        print(f"User '{user.name}' disconnected")

        self.users.remove(user)

        self.users.send(UserLeavePacket(user.name).encode())
