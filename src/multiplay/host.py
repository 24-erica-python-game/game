from src.baseclass.socket import SocketMeta


class Host(SocketMeta):
    def __init__(self, port: int):
        super().__init__()
        self.socket.bind(('localhost', port))

    def accept(self):
        self.socket.listen()
        self.conn, connection_info = self.socket.accept()
        self.connected_ip = connection_info[0]

        # if connected;
        self.conn.settimeout(5)
