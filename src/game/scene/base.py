class Scene:
    def __init__(self, name: str):
        self.name = name

    def run(self, *args, **kwargs):
        """
        매 틱마다 호출되는 함수, 이 함수에 씬의 렌더링과 로직을 작성해야 함.
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError
