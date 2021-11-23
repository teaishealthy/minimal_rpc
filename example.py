from minimal_rpc import block, handshake, send, windows_connect
from minimal_rpc.rpc import receive


f = windows_connect()

handshake(f, "CLIENT_ID")

send.rp(f, {"state": "Hello World"})

print(receive.auto(f))

block()
