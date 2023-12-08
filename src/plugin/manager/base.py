from spaceone.core.manager import BaseManager


class GithubBaseManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)

    @classmethod
    def get_all_managers(cls, options):
        cloud_service_types_option = options.get("cloud_service_types")
        if cloud_service_types_option:
            subclasses = []
            for subclass in cls.__subclasses__():
                if (
                    subclass.__name__.replace("Manager", "")
                    in cloud_service_types_option
                ):
                    subclasses.append(subclass)
            return subclasses

        else:
            return cls.__subclasses__()
