if __name__ == '__main__':
    import os
    import django
    import sys

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

    django.setup()

    from django_starter.contrib.seed import Seeder
    from apps.demo.models import Movie

    seeder = Seeder()
    data = seeder.seed(Movie)
    print(data)
