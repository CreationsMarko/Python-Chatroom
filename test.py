from pcr.common.packets import UserInitPacket

uip = UserInitPacket('test', 'foo')

print(uip)

en = uip.encode()

new_uip = UserInitPacket.decode(en)

print(new_uip)