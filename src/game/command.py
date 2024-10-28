commands = dict()


class register:
    """
    명령을 등록하는 데코레이터

    이 데코레이터를 사용해 함수를 선언면 commands 변수에 함수 이름을 키로 가지며 함수를 값으로 가지는 딕셔너리를 추가한다.
    """
    def __init__(self, func):
        commands.update({func.__name__: func})
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


# @register
# def _call_test_without_args():
#     print("_call_test_no_args called;")


# @register
# def _call_test_with_args(*args):
#     print(f"_call_test_with_args called;\nargs: {args}")
