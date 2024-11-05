prev = False

def once(signal: bool) -> bool:
    """
    ``True`` 값이 연속되어 들어오는 상황에서 처음 입력만 ``True`` 가 될 수 있도록 값을 출력함.

    입력이 ``False`` 가 될 경우 초기화 됨.

    스레드 안전하지 않음.

    >>> for _ in range(5):
    ...   once(True)
    True
    False
    False
    False
    False
    :param signal:
    :return:
    """
    global prev
    if signal:
        if not prev:
            prev = True
            return True
    else:
        prev = False
    return False
