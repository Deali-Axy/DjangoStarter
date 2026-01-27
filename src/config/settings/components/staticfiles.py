import os

from config.settings import BASE_DIR, DEBUG
from config.settings.components.common import URL_PREFIX

STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static-dist')
STATIC_URL = f'/{URL_PREFIX}static/'

MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media')
MEDIA_URL = f'/{URL_PREFIX}media/'

# 静态文件配置 (CSS, JavaScript, Images)
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# 使用 ManifestStaticFilesStorage 来给静态文件添加哈希后缀，防止浏览器缓存问题
# 仅在非 DEBUG 模式下启用（通常在生产环境）
if not DEBUG:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
