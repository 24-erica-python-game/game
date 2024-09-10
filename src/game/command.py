from src.multiplay.message.cmd_token import Number, String


commands = dict()


class register:
    """
    명령을 등록하는 데코레이터
    """
    def __init__(self, func):
        commands.update({func.__name__: func})
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


@register
def _call_test_without_args():
    print("_call_test_no_args called;")


@register
def _call_test_with_args(*args):
    print(f"_call_test_with_args called;\nargs: {args}")
