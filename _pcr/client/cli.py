from ..client import Client


def _input(text):
    result = input(text)
    while not result:
        magic = '\33[1A'+'\33[999D'+'\33[2D'
        print(magic, end='')
        result = input(text)
    return result


class ClientCLI(Client):

    def start(self):
        username = _input("What should we call you? ")
        self.set_username(username)
        print(f"Welcome to the chatroom, {self.username}!", end='\n\n')

        while True:
            message = _input("Message: ")
            magic = '\33[s'+'\33[1A'+'\r'+'\33[2K'
            magic += f"{self.username}: {message}"
            magic += '\33[u'
            print(magic, end="", flush=True)
            self.send_message(message)
    
    def process_message(self, message: str):
        magic = '\33[s'+'\33[A'+'\33[999D'+'\33[S'+'\33[L' + message + '\33[u'
        print(magic, end="", flush=True)
