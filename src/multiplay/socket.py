import socket
import struct
import sys
from typing import Optional


class BaseSocket:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn: Optional[socket.socket] = None
        self.connected_ip: Optional[str] = None
        self.msg_size = 1024

    def __del__(self):
        if self.conn is not None:
            self.conn.close()

    def pack(self, data: str, encoding: str = "utf-8") -> bytes:
        """
        데이터를 self.msg_size 바이트의 크기를 가지는 바이트열로 변환함. 맨 앞의 2바이트는 데이터의 길이, 그 후로는 데이터, 남은 공간은 널 문자로 채움.
        :param data: 인코딩할 문자열
        :param encoding: 인코딩 형식, 기본값은 UTF-8
        :return: 패딩을 포함한 바이트열을 반환함
        """
        if len(data) > self.msg_size - 2:
            raise ValueError("data is too big")
        padding_size = self.msg_size - len(data) - 2
        return struct.pack(f"!H {len(data)}s {padding_size}x", len(data), bytes(data, encoding))

    def unpack(self, data, encoding: Optional[str] = "utf-8") -> str | bytes:
        """
        인코딩 된 데이터를 다시 디코딩함, 데이터의 크기는 self.msg_size 같아야 함.
        :param data: 디코딩할 데이터, 데이터의 크기는 1024바이트 크기를 가져야 함.
        :param encoding: 인코딩 형식, 기본값은 UTF-8, None 될 수 있음
        :return: 디코딩 된 데이터, 만약 encoding 파라미터가 None 경우 디코딩 되지 않은 바이트열을 반환함.
        """
        # 한글은 첫글자만 반환되며 이모지는 예외를 일으킴; 알파벳 또는 숫자만 사용할 것
        data_size = struct.unpack("!H", data[:2])[0]
        padding_size = self.msg_size - data_size - 2
        data = struct.unpack_from(f"!{data_size}s {padding_size}x", data, offset=2)[0]
        return data.decode(encoding) if encoding else data

    def read(self):
        recv_data = self.conn.recv(self.msg_size)
        decoded = self.unpack(recv_data)
        return decoded

    def write(self, data):
        try:
            self.conn.send(self.pack(data))
        except AttributeError:  # if None;
            print("Connection is not established", file=sys.stderr)


# h = WSHandler()
# d = h._pack('19239')
# print(h._unpack(d, None))
# print(h._unpack(d))
