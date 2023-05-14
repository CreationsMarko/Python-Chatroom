from dataclasses import dataclass
from json import dumps, loads, JSONDecodeError
from typing import List

from .user import User


@dataclass
class Packet:

    def encode(self):
        json = self.__dict__.copy()
        data = dumps(json)
        return data.encode()
    
    @classmethod
    def decode(cls, data):
        json = data.decode()
        data = loads(json)
        return cls(**data)
    
    @classmethod
    def guess_packet(cls, data):
        json = data.decode()
        try:
            data = loads(json)
        except JSONDecodeError:
            return None
        packet_class = packets[data['type']]
        return packet_class(**data)

@dataclass
class UserInitPacket(Packet):

    users: List[User]

    type: str = 'user_init'

@dataclass
class UserJoinPacket(Packet):

    user: User

    type: str = 'user_join'

@dataclass
class UserLeavePacket(Packet):

    username: str
    private_key: str = ''

    type: str = 'user_leave'

@dataclass
class UserMessagePacket(Packet):

    username: str
    message: str
    private_key: str

    type: str = 'user_message'

@dataclass
class UserOnlinePacket(Packet):

    type: str = 'user_online'


packets = {
    'user_init': UserInitPacket,
    'user_join': UserJoinPacket,
    'user_leave': UserLeavePacket,
    'user_message': UserMessagePacket,
    'user_online': UserOnlinePacket,
}
