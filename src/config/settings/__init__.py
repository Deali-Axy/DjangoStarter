"""
This is a django-split-settings main file.
For more information read this:
https://github.com/sobolevn/django-split-settings
Default environment is `developement`.
To change settings file:
`DJANGO_ENV=production python manage.py runserver`
"""

from os import environ
from pathlib import Path
from split_settings.tools import optional, include

# Build paths inside the project like this: BASE_DIR.joinpath('some')
# `pathlib` is better than writing: dirname(dirname(dirname(__file__)))
BASE_DIR = Path(__file__).parent.parent.parent

ENV = environ.get('DJANGO_ENV') or 'development'

base_settings = [
    'components/*.py',

    # Select the right env:
    f'environments/{ENV}.py',
    # Optionally override some settings:
    optional('environments/local.py'),
]

# Include settings:
include(*base_settings)
