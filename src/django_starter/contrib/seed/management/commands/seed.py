import os
import logging

from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.apps import AppConfig
from django.conf import settings
from django_starter.contrib.code_generator.analyzer import get_app
from django_starter.contrib.code_generator.generator import Generator

logger = logging.getLogger('common')


class Command(BaseCommand):
    help = 'Seed module integrated with DjangoStarter to help you generate mock data for testing.\n\n' \
           'DjangoStarter内置的seed模块：可以帮助你生成用于测试的假数据。'

    def add_arguments(self, parser: CommandParser):
        parser.add_argument(
            'app_label',
            nargs=1,
            type=str,
            help='One or more application label'
        )

    def handle(self, *args, **options):
        logger.debug(options.__repr__())

        app_label = options['app_label'][0]

        logger.debug(f'app_label={app_label}')

        django_app = get_app(
            app_label=app_label,
            verbose_name=''
        )

        self.stdout.write(self.style.SUCCESS(f'Load django app info finished. {django_app}'))


        self.stdout.write(self.style.SUCCESS('Generating code finished.'))
