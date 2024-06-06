import os
import logging
from pathlib import Path
from jinja2 import Environment, PackageLoader, FileSystemLoader

from django_starter.contrib.code_generator.analyzer import get_models, get_app
from django_starter.contrib.code_generator.entities import DjangoApp

logger = logging.getLogger('common')


class Generator(object):
    """代码生成器"""

    def __init__(self, django_app: DjangoApp, template_path: str):
        """
        初始化代码生成器

        :param django_app: DjangoApp对象
        :param template_path: 模板文件路径
        """
        logger.debug(f'Generator init. django_app={django_app}, template_path={template_path}')
        self.django_app = django_app
        self.template_path = template_path
        self.jinja2_env = Environment(loader=FileSystemLoader(template_path))
        self.default_context = {
            'app': self.django_app,
            'models': self.django_app.models
        }

    def _jinja2_to_py(self, template_filename: str, python_filename: str, context: dict = None):
        logger.debug(f'load jinja2 template: {template_filename}')
        template = self.jinja2_env.get_template(template_filename)

        logger.debug(f'write python file: {os.path.join(self.django_app.path, python_filename)}')
        with open(os.path.join(self.django_app.path, python_filename), 'w+', encoding='utf-8') as f:
            f.write(template.render(self.default_context if context is None else context))

    def make_init(self):
        self._jinja2_to_py('__init__.jinja2', '__init__.py')

    def make_admin(self):
        self._jinja2_to_py('admin.jinja2', 'admin.py')

    def make_apps(self):
        self._jinja2_to_py('apps.jinja2', 'apps.py')

    def make_schemas_and_apis(self):
        ctx = {
            'app': self.django_app,
            'models': self.django_app.models,
        }

        for model in self.django_app.models:
            ctx['model'] = model

            model_apis_path = os.path.join(self.django_app.path, 'apis', model.slug)
            logger.debug(f'create model apis path: {model_apis_path}')
            os.makedirs(model_apis_path, exist_ok=True)

            logger.debug(f'generating schemas for {model.name}')
            template = self.jinja2_env.get_template('apis/schemas.jinja2')
            with open(os.path.join(self.django_app.path, 'apis', model.slug, 'schemas.py'), 'w+',
                      encoding='utf-8') as f:
                f.write(template.render(ctx))

            logger.debug(f'generating apis for {model.name}')
            template = self.jinja2_env.get_template('apis/apis.jinja2')
            with open(os.path.join(self.django_app.path, 'apis', model.slug, 'apis.py'), 'w+',
                      encoding='utf-8') as f:
                f.write(template.render(ctx))

            logger.debug(f'touch __init__ for {model.name}')
            Path(os.path.join(self.django_app.path, 'apis', model.slug, '__init__.py')).touch()

            logger.debug(f'generating __init__ for {model.name}')
            template = self.jinja2_env.get_template('apis/__init__.jinja2')
            with open(os.path.join(self.django_app.path, 'apis', '__init__.py'), 'w+',
                      encoding='utf-8') as f:
                f.write(template.render(ctx))

    def make_tests(self):
        ctx = {
            'app': self.django_app,
            'models': self.django_app.models,
        }

        app_tests_path = os.path.join(self.django_app.path, 'tests')
        logger.debug(f'create model apis path: {app_tests_path}')
        os.makedirs(app_tests_path, exist_ok=True)

        logger.debug(f'touch __init__ for tests')
        Path(os.path.join(self.django_app.path, 'tests', '__init__.py')).touch()

        for model in self.django_app.models:
            ctx['model'] = model

            logger.debug(f'generating tests for {model.name}')
            model_test_path = os.path.join(self.django_app.path, 'tests', f'test_{model.slug}.py')
            template = self.jinja2_env.get_template('tests.jinja2')
            with open(model_test_path, 'w+', encoding='utf-8') as f:
                f.write(template.render(ctx))

    def make_all(self):
        self.make_init()
        self.make_admin()
        self.make_apps()
        self.make_schemas_and_apis()
        self.make_tests()
