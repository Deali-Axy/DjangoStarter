if __name__ == '__main__':
    import os
    import django
    import sys

    sys.path.append(r'D:\Code\0_Django\DjangoStarter')
    sys.path.append(r'D:\Code\0_Django\DjangoStarter\src')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

    django.setup()

    from django_starter.contrib.code_generator.analyzer import get_models

    get_models('demo')
