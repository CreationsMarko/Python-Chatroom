from ..common.chatsocket import ChatSocket
import multiprocessing


class MessageTooLongError(Exception):
    pass

class Client:

    sock: ChatSocket

    username: str

    def __init__(self):
        self.sock = ChatSocket()

    def connect(self,
        host: str, port: int
    ):
        self.sock.connect((host, port))

        process = multiprocessing.Process(
            target=self.await_messages)
        process.daemon = True
        process.start()

        self.start()
    
    def await_messages(self):
        while True:
            message = self.sock.recv(1024).decode('utf-8')
            self.process_message(message)

    def start(self):
        pass

    def set_username(self, username):
        if len(username) > 16:
            raise MessageTooLongError("Username must be at most 16 characters long.")
        self.username = username
        self.sock.send(username)


    def send_message(self, message: str):
        """
        Sends a message to the chatroom.

        Args:
            message (str)
        """
        if len(message) > 1024:
            raise MessageTooLongError("Message must contain at most 1000 characters.")
        self.sock.send(message)


    def process_message(self, message: str):
        """
        This function gets called whenever a message is received from another user in the chatroom.

        Args:
            message (str)
        """