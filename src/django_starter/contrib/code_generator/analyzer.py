import inspect
import logging
from typing import List

from django.apps import apps
from jinja2 import Environment, PackageLoader
from django_starter.contrib.code_generator.utils import camel_to_snake, snake_to_camel
from django_starter.contrib.code_generator.entities import DjangoModel, DjangoApp

logger = logging.getLogger('common')


def get_super_class(cls: type) -> type:
    super_classes = inspect.getmro(cls)
    if len(super_classes) >= 2:
        return super_classes[1]
    else:
        return type(None)


def get_class(cls: type) -> type:
    return inspect.getmro(cls)[0]


def get_models(app_label: str) -> List[DjangoModel]:
    django_model_list: List[DjangoModel] = []
    app_obj = apps.get_app_config(app_label)
    for model in app_obj.get_models():
        unsupported_field_types: List[str] = ['ManyToManyField']
        field_names: List[str] = ['pk']
        for field in model._meta.fields:
            if type(field).__name__ not in unsupported_field_types:
                field_names.append(field.name)
        d_model = DjangoModel(
            name=model.__name__,
            verbose_name=model._meta.verbose_name,
            url_name=camel_to_snake(model.__name__),
            fields=field_names
        )
        logger.debug(f'Found django model: {d_model}')
        django_model_list.append(d_model)
    return django_model_list


def get_app(app_label: str, verbose_name: str) -> DjangoApp:
    app_config = apps.get_app_config(app_label)

    django_app = DjangoApp(
        name=app_label,
        name_camel_case=snake_to_camel(app_label),
        verbose_name=verbose_name,
        path=app_config.path,
        models=get_models(app_label),
        app_config=app_config
    )
    return django_app
