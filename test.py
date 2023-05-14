from pcr.client import Client

class ClientCLI(Client):

    def start(self):
        self.set_username("test_account")
        self.leave()
        exit()

ClientCLI().connect('127.0.0.1', 7077)