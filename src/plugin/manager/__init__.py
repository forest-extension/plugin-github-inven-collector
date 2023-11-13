from spaceone.core.manager import BaseManager
from abc import abstractmethod, ABC, ABCMeta


class GithubBaseManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)

    @classmethod
    def get_managers(cls):
        sub_classes = cls.__subclasses__()
        print(sub_classes)
        return sub_classes
