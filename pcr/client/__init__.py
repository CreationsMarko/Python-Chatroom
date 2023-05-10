from socket import socket
import multiprocessing

from cryptography.fernet import Fernet

from ..common.user import User
from ..common.user.userlist import UserList
from ..common.packets import Packet, UserJoinPacket, UserMessagePacket, UserInitPacket

class MessageTooLongError(Exception):
    pass

class Client:

    server: socket
    users: UserList

    user: User

    username: str
    public_key: str
    private_key: str

    def __init__(self):
        self.server = socket()
        self.public_key = Fernet.generate_key()
        self.private_key = Fernet.generate_key()

        self.users = UserList()

    def connect(self,
        host: str, port: int
    ):
        self.server.connect((host, port))

        process = multiprocessing.Process(
            target=self.packet_handler, args=(self.server,))
        process.daemon = True
        process.start()

        self.start()
    


    def packet_handler(self, connection):

        while True:
            raw_packet = connection.recv(1024)
            packet = Packet.guess_packet(raw_packet)

            if packet.type == 'user_init':
                self._initialize_self(packet)
            if packet.type == 'user_join':
                self._initialize_user(packet)
            if packet.type == 'user_message':
                self._process_message(packet)
            if packet.type == 'user_leave':
                self._remove_user(packet)


    def _initialize_self(self, data: UserInitPacket):

        for raw_user in data.users:
            user = User(**raw_user)
            self.users.add(user)

    def _initialize_user(self, data: UserJoinPacket):

        user = User(**data.user)

        self.users.add(user)

    def _process_message(self, data: UserMessagePacket):

        user = self.users.from_username(data.username)
        message = data.message.encode()
        decoded_message = Fernet(user.public_key.encode()).decrypt(message)

        self.process_message(user.name, decoded_message.decode())

    def await_messages(self):
        while True:
            message = self.server.recv(1024).decode('utf-8')
            self.process_message(message)


    def set_username(self, username):
        if len(username) > 16:
            raise MessageTooLongError("Username must be at most 16 characters long.")
        self.username = username

        user = User(self.username, self.private_key.decode(), self.public_key.decode())

        join_packet = UserJoinPacket(user.raw())
        self.server.send(join_packet.encode())


    def start(self):
        pass

    def send_message(self, message: str):
        """
        Sends a message to the chatroom.

        Args:
            message (str)
        """
        if len(message) > 1024:
            raise MessageTooLongError("Message must contain at most 1000 characters.")
        encoded_message = Fernet(self.public_key).encrypt(message.encode())

        message_packet = UserMessagePacket(self.username, encoded_message.decode(), self.private_key.decode())
        self.server.send(message_packet.encode())
        self.process_message(self.username, message)

    def process_message(self, username: str, message: str):
        """
        This method gets called whenever a message is received from another user in the chatroom.

        Args:
            message (str)
        """

    def join_message(self, username: str):
        """
        This method gets called whenever a user joins the chatroom.

        Args:
            message (str)
        """

    def leave_message(self, username: str):
        """
        This method gets called whenever a user leaves the chatroom.

        Args:
            message (str)
        """
