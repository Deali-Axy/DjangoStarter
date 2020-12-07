import os

from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.apps import AppConfig
from django.conf import settings
from contrib.code_generator.analyzer import get_app
from contrib.code_generator.generator import Generator


class Command(BaseCommand):
    help = 'Code Generator integrated with DjangoStarter help you generate CRUD code from models definition.\n\n' \
           'DjangoStarter内置的代码生成器：可以根据model定义自动生成CRUD代码。'

    def add_arguments(self, parser: CommandParser):
        parser.add_argument('app_label', help='One or more application label')
        parser.add_argument(
            '--verbose_name',
            type=str,
            required=True,
            help='verbose name of Django App.'
        )

    def handle(self, *args, **options):
        self.stdout.write('write')
        for app_label in args:
            django_app = get_app(
                app_label=app_label,
                verbose_name=options['verbose_name']
            )
            self.stdout.write(self.style.SUCCESS(django_app))
            Generator(
                django_app=django_app,
                template_path=os.path.join(settings.BASE_DIR, 'contrib', 'code_generator', 'templates')
            )
            self.stdout.write(app_label)
