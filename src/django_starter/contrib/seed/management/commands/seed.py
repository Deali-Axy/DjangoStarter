import os
import logging

from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.apps import apps
from django_starter.contrib.code_generator.analyzer import get_app
from django_starter.contrib.code_generator.generator import Generator
from django_starter.contrib.seed import Seeder

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

        parser.add_argument(
            'seed_data_count',
            nargs=1,
            type=int,
            help='Number of seeding data to generate'
        )

    def handle(self, *args, **options):
        logger.debug(options.__repr__())

        app_label = options['app_label'][0]
        seed_data_count = options['seed_data_count'][0]

        logger.debug(f'app_label: {app_label}, seed_data_count: {seed_data_count}')

        seeder = Seeder()

        app = apps.get_app_config(app_label)
        self.stdout.write(self.style.SUCCESS(f'Load django app info finished. {app_label}'))

        for model in app.get_models():
            instances = []
            for i in range(seed_data_count):
                data = seeder.seed(model)
                instances.append(model(**data))

            logger.debug(f'bulk_data length: {len(instances)}, inserting to model: {model.__name__}')
            model.objects.bulk_create(instances)

        self.stdout.write(self.style.SUCCESS('Generating seeding data finished.'))
