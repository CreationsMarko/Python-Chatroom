from typing import List

from ..user import User

Nothing = None


class UserList:

    users: List[User]

    def send(self, data):
        for user in self.users:
            user.send(data)

    def add(self, user):
        self.users.append(user)

    def remove(self, user):
        self.users.remove(user)
    
    def has_user(self, username):
        for user in self.users:
            if username == user.name:
                return True
        return False


    def __init__(self, users: List[User] = None):
        if users is None:
            users = []
        self.users = users

    def from_username(self, username, fallback = Nothing):
        for user in self.users:
            if user.name == username:
                return user
        if fallback != Nothing:
            return fallback
        raise KeyError(f"Could not find a user with the username '{username}'")

    def from_connection(self, connection, fallback):
        for user in self.users:
            if user.connection == connection:
                return user
        if fallback != Nothing:
            return fallback
        raise KeyError(f"Could not find a user with the connection '{connection}'")

    def from_private_key(self, private_key, fallback):
        for user in self.users:
            if user.private_key == private_key:
                return user
        if fallback != Nothing:
            return fallback
        raise KeyError(f"Could not find a user with the key '{private_key}'")