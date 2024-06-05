if __name__ == '__main__':
    import os
    import django
    import pprint

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

    django.setup()

    from django.db import models
    from django.utils.text import slugify
    from django_starter.contrib.seed import Seeder
    from django_starter.contrib.seed.models import SeedTestModel

    seeder = Seeder()
    data = seeder.seed(SeedTestModel)
    pprint.pprint(data)

