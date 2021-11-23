import asyncio
import json
import os
import struct
import uuid


def windows_connect():
    f = None
    for a in range(10):
        try:
            f = open(rf"\\?\pipe\discord-ipc-{a}", "wb+")
            break
        except FileNotFoundError:
            pass
    return f


def handshake(f, client_id):
    send.json(f, {"v": 1, "client_id": client_id}, 0)
    receive.auto(f)


def send(f, data, code_):
    byte_data = data.encode("utf-8")
    h = struct.pack("<II", code_, len(byte_data))
    f.write(h)
    f.write(byte_data)


def _send_rp(f, data):
    d = {
        "cmd": "SET_ACTIVITY",
        "args": {"pid": os.getpid(), "activity": data},
        "nonce": f"{uuid.uuid4()}",
    }
    send.json(f, d, 1)


send.json = lambda f, data, op: send(f, json.dumps(data), op)
send.rp = _send_rp


def receive(f, len_):
    data = f.read(len_)
    return data


receive.header = lambda f: struct.unpack("<II", receive(f, 8))[1]
receive.json = lambda f, l: json.loads(receive(f, l).decode("utf-8"))
receive.auto = lambda f: receive.json(f, receive.header(f))


def block():
    async def _block():
        await asyncio.Future()

    asyncio.run(_block())
