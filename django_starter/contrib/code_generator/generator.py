import os
import logging
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

    def make_serializers(self):
        self._jinja2_to_py('serializers.jinja2', 'serializers.py')

    def make_urls(self):
        self._jinja2_to_py('urls.jinja2', 'urls.py')

    def make_viewsets(self):
        self._jinja2_to_py('viewsets.jinja2', 'viewsets.py')

    def make_all(self):
        self.make_init()
        self.make_admin()
        self.make_apps()
        self.make_serializers()
        self.make_urls()
        self.make_viewsets()
