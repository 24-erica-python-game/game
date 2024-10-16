from enum import Enum


class Scene:
    subclasses = dict()

    def __init__(self):
        Scene.subclasses.update({self.__name__: self})

    def run(self):
        pass


scenes = Enum("ScenesEnum", Scene.subclasses)
