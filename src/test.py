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
    from apps.demo.models import Music

    seeder = Seeder()
    # data = seeder.seed(SeedTestModel)
    # pprint.pprint(data)
    #
    # from django_starter.contrib.code_generator import analyzer
    #
    # analyzer.get_models('demo')

    pprint.pprint(seeder.seed(Music))
