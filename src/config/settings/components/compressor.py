from config.settings import BASE_DIR
from config.settings.components.common import DOCKER, DEBUG

COMPRESS_ENABLED = True

if DOCKER:
    COMPRESS_ROOT = BASE_DIR / 'static'
else:
    COMPRESS_ROOT = BASE_DIR / '..' / 'static-dist'
