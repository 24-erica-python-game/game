commands = dict()

class register:
    def __init__(self, func):
        commands.update({func.__name__: func})
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


@register
def _call_test_without_args():
    print("_call_test_no_args called;")


@register
def _call_test_with_args(*args, **kwargs):
    print(f"_call_test_with_args called;\nargs: {args}")

