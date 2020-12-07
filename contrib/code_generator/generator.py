import inspect
from typing import List

from django.apps import apps
from jinja2 import Environment, PackageLoader
from contrib.code_generator.utils import camel_to_snake, snake_to_camel
from contrib.code_generator.models import DjangoModel, DjangoApp


def get_models(app_label: str) -> List[DjangoModel]:
    django_model_list: List[DjangoModel] = []
    app_obj = apps.get_app_config(app_label)
    for model in app_obj.get_models():
        d_model = DjangoModel(
            name=model.__name__,
            verbose_name=model._meta.verbose_name,
            url_name=camel_to_snake(model.__name__),
        )
        print(d_model)
        django_model_list.append(d_model)
    return django_model_list


def get_app(app_label: str, verbose_name: str) -> DjangoApp:
    django_app = DjangoApp(
        name=app_label,
        name_camel_case=snake_to_camel(app_label),
        verbose_name=verbose_name,
        models=get_models(app_label)
    )
    return django_app


if __name__ == '__main__':
    import os, django

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()

    get_models('demo')
    _d_app = get_app('demo', '博客')
    print(_d_app)

    env = Environment(loader=PackageLoader('contrib', 'code_generator', 'templates'))
    template = env.get_template('apps.jinja2')
    print(template)
