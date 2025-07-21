import os
import logging

from django.core.management.base import BaseCommand, CommandError, CommandParser

from apps.demo.seed_data import seed_data_movies

logger = logging.getLogger('common')


class Command(BaseCommand):
    help = 'Seed module integrated with DjangoStarter to help you generate mock data for testing.\n\n' \
           'DjangoStarter内置的seed模块：可以帮助你生成用于测试的假数据。'

    def handle(self, *args, **options):
        logger.debug(options.__repr__())

        seed_data_movies()

        self.stdout.write(self.style.SUCCESS('Generating seeding data finished.'))
