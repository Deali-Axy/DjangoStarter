import os
import logging

from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.apps import AppConfig
from django.conf import settings
from django_starter.contrib.code_generator.analyzer import get_app
from django_starter.contrib.code_generator.generator import Generator

logger = logging.getLogger('common')


class Command(BaseCommand):
    help = ("DjangoStarter Code Generator: "
            "Automatically generates configuration (such as admin, app, urls, etc.), "
            "testing (both unit and integration tests), "
            "and interface (Ninja's schema and API) codes based on model definitions.\n"
            "DjangoStarter代码生成器："
            "根据模型定义自动生成配置（如admin、app、urls等）、"
            "测试（包括单元测试和集成测试）"
            "以及接口（使用Ninja的schema和API）代码。")

    def add_arguments(self, parser: CommandParser):
        parser.add_argument(
            'app_label',
            type=str,
            help='Application label.\n'
                 '应用标签，用于指定Django应用。'
        )
        parser.add_argument(
            'verbose_name',
            type=str,
            help='Verbose name of the Django App.\n'
                 'Django应用的详细名称。'
        )
        parser.add_argument(
            '--models',
            type=str,
            nargs='+',  # 允许输入多个模型名称
            help='Optional: Generates tests, schema and API code only for the specified models.\n'
                 '可选：仅为指定的模型生成测试, schema和API代码。',
            required=False
        )
        parser.add_argument(
            '--no-admin',
            action='store_true',
            help='Skip generating admin code.\n'
                 '跳过生成admin代码。'
        )
        parser.add_argument(
            '--no-apps',
            action='store_true',
            help='Skip generating apps code.\n'
                 '跳过生成apps代码。'
        )
        parser.add_argument(
            '--no-tests',
            action='store_true',
            help='Skip generating test code.\n'
                 '跳过生成测试代码。'
        )
        parser.add_argument(
            '--no-apis',
            action='store_true',
            help='Skip generating API and schema code.\n'
                 '跳过生成API和schema代码。'
        )

    def handle(self, *args, **options):
        logger.debug(options.__repr__())

        app_label = options.get('app_label')
        verbose_name = options.get('verbose_name')
        models = options.get('models', None)

        logger.debug(f'app_label={app_label}, verbose={verbose_name}')

        django_app = get_app(
            app_label=app_label,
            verbose_name=verbose_name
        )
        self.stdout.write(self.style.SUCCESS(f'Load django app info finished. {django_app}'))

        generator = Generator(
            django_app=django_app,
            template_path=os.path.join(settings.BASE_DIR, 'django_starter', 'contrib', 'code_generator', 'templates')
        )

        # 根据命令行参数决定生成哪些代码
        if models:
            logger.debug(f"Model name provided: {models}")
            if not options.get('no_tests'):
                generator.make_tests(models)
            if not options.get('no_apis'):
                generator.make_schemas_and_apis(models)
        else:
            logger.debug("No specific model name provided.")
            generator.make_init()
            if not options.get('no_admin'):
                generator.make_admin()
            if not options.get('no_apps'):
                generator.make_apps()
            if not options.get('no_apis'):
                generator.make_schemas_and_apis()
            if not options.get('no_tests'):
                generator.make_tests()

        self.stdout.write(self.style.SUCCESS('Generating code finished.'))
