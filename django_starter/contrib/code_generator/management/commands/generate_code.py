import os
import logging

from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.apps import AppConfig
from django.conf import settings
from django_starter.contrib.code_generator.analyzer import get_app
from django_starter.contrib.code_generator.generator import Generator

logger = logging.getLogger('common')


class Command(BaseCommand):
    help = 'Code Generator integrated with DjangoStarter help you generate CRUD code from models definition.\n\n' \
           'DjangoStarter内置的代码生成器：可以根据model定义自动生成CRUD代码。'

    def add_arguments(self, parser: CommandParser):
        parser.add_argument(
            'app_label',
            nargs=1,
            type=str,
            help='One or more application label'
        )
        parser.add_argument(
            'verbose_name',
            nargs=1,
            type=str,
            help='Verbose name of Django App'
        )

    def handle(self, *args, **options):
        logger.debug(options.__repr__())

        app_label = options['app_label'][0]
        verbose_name = options['verbose_name'][0]

        logger.debug(f'app_label={app_label}, verbose={verbose_name}')

        django_app = get_app(
            app_label=app_label,
            verbose_name=verbose_name
        )

        self.stdout.write(self.style.SUCCESS(f'Load django app info finished. {django_app}'))

        Generator(
            django_app=django_app,
            template_path=os.path.join(settings.BASE_DIR, 'django_starter', 'contrib', 'code_generator', 'templates')
        ).make_all()

        self.stdout.write(self.style.SUCCESS('Generating code finished.'))
