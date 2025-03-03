from django.utils.translation import gettext_lazy as _
from config.settings import BASE_DIR

# 国际化配置
LANGUAGE_CODE = 'zh-HAns'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False

LANGUAGES = [
    ('zh-hans', _('简体中文')),
    ('zh-hant', _('繁體中文')),
    ('en', _('English')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]
