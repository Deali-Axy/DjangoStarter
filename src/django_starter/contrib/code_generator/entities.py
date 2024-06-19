from typing import List, Optional, Type
from django.apps import AppConfig
from django.db.models import Field, Model, ImageField, TextField


class ModelField(object):
    def __init__(
            self, name: str, attname: str, field_type: Type[Field],
            primary_key: bool = False,
            is_relation: bool = False,
            python_type: Optional[type] = None,
            verbose_name: str = None,
    ):
        self.name = name
        self.attname = attname
        self.field_type = field_type
        self.primary_key = primary_key
        self.is_relation = is_relation
        self.python_type = python_type
        if verbose_name:
            self.verbose_name = verbose_name
        else:
            self.verbose_name = name

    @property
    def is_djs_reserve(self):
        """是否DjangoStarter保留字段"""
        return self.name in ['is_deleted', 'created_time', 'updated_time']

    @property
    def is_image(self):
        """是否图片字段"""
        return self.field_type == ImageField

    @property
    def is_text(self):
        # return self.field_type.__class__ == TextField
        return self.field_type == TextField


class DjangoModel(object):
    def __init__(self, model: Model, name: str, verbose_name: str, slug: str, fields: List[ModelField]):
        """

        :param model: django.db.models.Model 实例
        :param name: 模型名称
        :param verbose_name: 中文名
        :param slug: URL名称
        """
        self.model = model
        self.name = name
        self.verbose_name = verbose_name
        self.slug = slug
        self.fields: List[ModelField] = fields

    def is_model_ext_instance(self):
        from django_starter.db.models import ModelExt
        return isinstance(self.model, ModelExt)

    def __str__(self):
        return f'<DjangoModel>{self.name}:{self.verbose_name}:{self.slug}'

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
