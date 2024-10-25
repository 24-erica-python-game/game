from typing import Optional, Self

from game.scene.base import Scene


class SceneHandler:
    instance: Self

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SceneHandler, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self._scene_stack: list[Scene] = []
        self._top_index: int = -1

    def get_current_scene(self) -> Scene:
        """
        현재 씬을 반환함.
        :return:
        """
        return self._scene_stack[self._top_index]

    def get_scene_from_index(self, index: int) -> Optional[Scene]:
        """
        스택의 위에서부터 ``index`` 번째에 있는 씬을 반환함.

        만약 스택의 크기를 넘어가면 ``None``이 반환됨.
        :param index:
        :return:
        """
        try:
            return self._scene_stack[index]
        except IndexError:
            return None

    def get_scene_from_name(self, name: str) -> Optional[Scene]:
        """
        스택을 위에서부터 ``name`` 이 같은 씬을 찾을때까지 탐색함.

        만약 찾지 못했을 경우 ``None`` 이 반환됨.

        같은 이름의 씬이 여러개일 경우 스택의 맨 위에 있는 씬이 반환됨.
        :param name:
        :return:
        """
        for i in range(self._top_index, 0, -1):
            if self._scene_stack[i].name == name:
                return self._scene_stack[i]
        return None

    def get_index(self, name: str) -> Optional[int]:
        """
        스택의 위에서부터 ``name`` 이 같은 씬이 나올때까지 탐색하고, 그 씬이 있는 인덱스를 반환함.

        만약 발견하지 못할 경우 ``None`` 이 반환됨.
        :param name:
        :return:
        """
        for i in range(self._top_index, 0, -1):
            if self._scene_stack[i].name == name:
                return i
        return None

    def set_scene_from_name(self, name: str, clear_stack: bool = False):
        """
        스택을 위에서부터 ``name`` 이 같은 스택이 나올때까지 탐색해
        그 씬이 나오면 해당 씬이 스택의 맨 위에 오도록 스택을 비움.

        만약 ``clear_stack`` 이 참일 경우 스택은 해당 씬만 남게 됨.

        만약 찾지 못했을 경우 ``KeyError`` 가 발생함.
        :param name:
        :param clear_stack:
        :raises KeyError: 만약 씬을 찾지 못했을 경우
        :return:
        """
        target_index = None
        for i in range(self._top_index, 0, -1):
            if self._scene_stack[i].name == name:
                target_index = i

        if target_index is not None:
            if not clear_stack:
                for i in range(self._top_index, target_index, -1):
                    del self._scene_stack[i]
                    self._top_index -= 1
            else:
                self._scene_stack = [self._scene_stack[target_index]]
                self._top_index = 0
        else:
            raise KeyError

    def set_scene_from_index(self, index: int, clear_stack: bool = False):
        """
        스택의 맨 위에서부터 ``index`` 번째의 씬이 스택의 맨 위에 오도록 스택을 비움.

        만약 ``index`` 가 스택 크기보다 같거나 클 경우 ``IndexError`` 가 발생함.

        만약 ``clear_stack`` 이 참일 경우 스택은 해당 씬만 남게 됨.
        :param index:
        :param clear_stack:
        :raises IndexError: 올바르지 않은 인덱스가 주어질 경우
        :return:
        """
        if index <= self._top_index:
            raise IndexError

        if not clear_stack:
            for i in range(self._top_index, index, -1):
                del self._scene_stack[i]
                self._top_index -= 1
        else:
            self._scene_stack = [self._scene_stack[index]]

    def set_prev_scene(self):
        """
        현재 씬을 스택에서 제거함.

        만약 스택이 비어있으면 아무것도 하지 않음.
        """
        try:
            del self._scene_stack[self._top_index]
            self._top_index -= 1
        except KeyError:
            return

    def add_scene(self, scene: Scene):
        """
        스택에 씬을 추가함.
        :param scene:
        :return:
        """
        self._scene_stack.append(scene)

    def draw_scene(self):
        """
        현재 씬을 렌더링함.

        만약 스택이 비어있으면 아무것도 하지 않음.
        :return:
        """
        scene = self.get_current_scene()
        if scene is not None:
            scene.run()
        else:
            return
