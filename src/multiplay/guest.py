import sys

from src.multiplay.base_socket import BaseSocket


class Guest(BaseSocket):
    def __init__(self):
        super().__init__()

    def connect(self, ip: str, port: int):
        try:
            self.socket.connect((ip, port))
        except AttributeError:
            print("Connection is not established", file=sys.stderr)
        except TimeoutError:
            print("Connection timed out", file=sys.stderr)
        except InterruptedError:
            print("Connection interrupted", file=sys.stderr)
        else:
            self.connected_ip = ip
            self.conn = self.socket
            self.conn.settimeout(5)
            # print(f"Connected to {self.connected_ip}")
