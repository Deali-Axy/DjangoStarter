from typing import List
from django.apps import AppConfig


class DjangoModel(object):
    def __init__(self, name: str, verbose_name: str, url_name: str, fields: List[str]):
        """

        :param name: 模型名称
        :param verbose_name: 中文名
        :param url_name: 路由名称
        """
        self.name = name
        self.verbose_name = verbose_name
        self.url_name = url_name
        self.fields: List[str] = fields

    def __str__(self):
        return f'<DjangoModel>{self.name}:{self.verbose_name}:{self.url_name}'

    def __repr__(self):
        return self.__str__()


class DjangoApp(object):
    def __init__(
            self, name: str,
            name_camel_case: str,
            verbose_name: str,
            path: str,
            models: List[DjangoModel],
            app_config: AppConfig = None
    ):
        """

        :param name: App名称
        :param name_camel_case: 驼峰风格名称
        :param verbose_name: 中文名
        :param path: 路径
        :param models: App中的模型列表
        :param app_config: AppConfig对象
        """
        self.name = name
        self.name_camel_case = name_camel_case
        self.verbose_name = verbose_name
        self.path = path
        self.models: List[DjangoModel] = models
        self.app_config: AppConfig = app_config

    def __str__(self):
        return f'<DjangoApp>{self.name}:{self.name_camel_case}:{self.verbose_name}:{self.models}'

    def __repr__(self):
        return self.__str__()
