from typing import List


class DjangoModel(object):
    def __init__(self, name: str, verbose_name: str, url_name: str):
        self.name = name
        self.verbose_name = verbose_name
        self.url_name = url_name


class DjangoApp(object):
    def __init__(self, name: str, name_camel_case: str, verbose_name: str, models: List[DjangoModel]):
        self.name = name
        self.name_camel_case = name_camel_case
        self.verbose_name = verbose_name
        self.models: List[DjangoModel] = models
