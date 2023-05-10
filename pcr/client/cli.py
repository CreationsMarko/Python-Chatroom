from ..client import Client


def required_input(text):
    result = input(text)
    while not result:
        magic = '\33[1A'+'\33[999D'+'\33[2D'
        print(magic, end='')
        result = input(text)
    return result


class ClientCLI(Client):

    magic = '\33[s'+'\33[A'+'\33[999D'+'\33[S'+'\33[L'

    def start(self):
        username = required_input("What should we call you? ")
        self.set_username(username)
        print(f"Welcome to the chatroom, {self.username}!", end='\n\n')
        while True:
            self.handle_messages()

    def handle_messages(self):
        message = required_input('\r'+'\33[2K'+"Message: ")
        magic = '\33[1A'+'\33[999D'+'\33[2D'
        print(magic, end='')
        self.send_message(message)

    def process_message(self, username: str, message: str):
        final = self.magic + f"{username}: {message}" + '\33[u'
        print(final, end="", flush=True)

    def join_message(self, username: str):
        final = self.magic + f"{username} has joined the chat" + '\33[u'
        print(final, end="", flush=True)

    def leave_message(self, username: str):
        final = self.magic + f"{username} has left the chat" + '\33[u'
        print(final, end="", flush=True)