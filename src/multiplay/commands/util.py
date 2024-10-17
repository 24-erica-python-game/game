from src.game.command import register
from typing import ByteString, Optional

@register
def say_message(message: str, to: Optional[int] = None):
    """
    상대방에게 메세지를 전송함
    :param message: 전송할 메세지의 내용
    :param to: 전달할 상대의 순서, None일 경우 모든 상대에게 전송함
    :return:
    """
    print(f"Message: {message}")