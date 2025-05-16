
import socket

class SCUDClient:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    async def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        login_cmd = f"LOGIN 1.8 {self.username} {self.password}\r\n"
        self.sock.send(login_cmd.encode())
        self.sock.recv(1024)

    async def get_aplist(self):
        self.sock.send(b"GETAPLIST\r\n")
        data = self.sock.recv(1024).decode()
        ids = [int(x) for x in data.split()[2:]]
        return ids

    async def get_apinfo(self, door_id):
        self.sock.send(f"GETAPINFO {door_id}\r\n".encode())
        data = self.sock.recv(1024).decode()
        name = data.split('NAME')[1].split('ZONE')[0].strip().strip('"')
        return {"id": door_id, "name": name}

    async def open_door(self, door_id):
        cmd = f"ALLOWPASS {door_id} 5 UNKNOWN\r\n"
        self.sock.send(cmd.encode())
        self.sock.recv(1024)
