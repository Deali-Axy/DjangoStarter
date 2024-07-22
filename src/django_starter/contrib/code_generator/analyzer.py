import inspect
import logging
from typing import List, Type, Optional

from django.apps import apps
from django.db import models
from django_starter.contrib.code_generator.entities import ModelField, DjangoModel, DjangoApp
from django_starter.contrib.code_generator.utils import camel_to_snake, snake_to_camel

logger = logging.getLogger('common')


def get_python_type(field: Type[models.Field]) -> Optional[type]:
    type_mapping = {
        models.CharField: str,
        models.TextField: str,
        models.IntegerField: int,
        models.FloatField: float,
        models.BooleanField: bool,
        models.DateField: str,  # Dates can be handled as strings in the format 'YYYY-MM-DD'
        models.DateTimeField: str,  # DateTimes can be handled as strings in the format 'YYYY-MM-DD HH:MM:SS'
        models.EmailField: str,
        models.URLField: str,
        models.DecimalField: float,  # Decimal can be converted to float for simplicity
        models.SlugField: str,
        models.UUIDField: str,  # UUID can be handled as a string
        models.BinaryField: bytes,
        models.DurationField: str,  # Duration can be handled as strings in the format 'HH:MM:SS'
        models.IPAddressField: str,
        models.GenericIPAddressField: str,
        models.JSONField: dict,  # JSON fields can be represented as dictionaries
        models.PositiveIntegerField: int,
        models.BigIntegerField: int,
        models.PositiveSmallIntegerField: int,
        models.SmallIntegerField: int,
        models.TimeField: str,  # Time can be handled as strings in the format 'HH:MM:SS'
        models.BigAutoField: int,
    }

    field_class = field.__class__

    for model_field, python_type in type_mapping.items():
        if field_class == model_field:
            return python_type

    return None


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

        fields = [ModelField(field.name, field.attname, type(field),
                             primary_key=field.primary_key,
                             is_relation=field.is_relation,
                             python_type=get_python_type(field if not field.is_relation else field.target_field),
                             verbose_name=field.verbose_name)
                  for field in model._meta.fields if
                  type(field).__name__ not in unsupported_field_types]

        m_obj = DjangoModel(
            model=model,
            name=model_name,
            verbose_name=verbose_name,
            slug=url_name,
            fields=fields
        )
        logger.debug(f'Found django model: {m_obj}, fields count: {len(fields)}')

        django_model_list.append(m_obj)

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
