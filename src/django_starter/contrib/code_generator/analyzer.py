import inspect
import logging
from typing import List

from django.apps import apps
from django_starter.contrib.code_generator.entities import ModelField, DjangoModel, DjangoApp
from django_starter.contrib.code_generator.utils import camel_to_snake, snake_to_camel

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
    unsupported_field_types: List[str] = ['ManyToManyField']

    django_model_list: List[DjangoModel] = []
    app = apps.get_app_config(app_label)
    for model in app.get_models():
        model_name = model.__name__
        verbose_name = model._meta.verbose_name
        url_name = camel_to_snake(model_name)

        fields = [ModelField(field.name, type(field).__name__,
                             primary_key=field.primary_key,
                             verbose_name=field.verbose_name)
                  for field in model._meta.fields if
                  type(field).__name__ not in unsupported_field_types]

        d_model = DjangoModel(
            name=model_name,
            verbose_name=verbose_name,
            slug=url_name,
            fields=fields
        )
        logger.debug(f'Found django model: {d_model}, fields count: {len(fields)}')

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
