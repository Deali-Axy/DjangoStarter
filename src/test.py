if __name__ == '__main__':
    import os
    import django
    import pprint

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

    django.setup()

    from django.db import models
    from django_starter.contrib.seed import Seeder
    from apps.demo.models import TestModel

    seeder = Seeder()
    data = seeder.seed(TestModel)
    pprint.pprint(data)
    print('email', seeder.fake.email())

    # field = TestModel._meta.get_field('email_field')
    # print('internal type', field.get_internal_type())
    # print('type', type(field))
    # print('__class__', field.__class__, 'eq to models.EmailField?', field.__class__ == models.EmailField)
    # print('is sub class to models.EmailField?', issubclass(field.__class__, models.EmailField))
    # print('is sub class to models.CharField?', issubclass(field.__class__, models.CharField))
