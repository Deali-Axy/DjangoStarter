from captcha.conf import settings
from captcha.models import CaptchaStore
from captcha.helpers import captcha_audio_url, captcha_image_url


class CaptchaItem(object):
    def __init__(self, key, image_url, audio_url):
        self.key = key
        self.image_url = image_url
        self.audio_url = audio_url


def refresh() -> CaptchaItem:
    """
    获取新的验证码

    :return:
    """
    key = CaptchaStore.pick()
    return CaptchaItem(
        key,
        captcha_image_url(key),
        captcha_audio_url(key) if settings.CAPTCHA_FLITE_PATH else None,
    )


def verify(key: str, code: str) -> bool:
    """
    检查输入的验证码是否正确

    :param key:
    :param code:
    :return:
    """
    # 清理过期的验证码记录
    CaptchaStore.remove_expired()
    try:
        CaptchaStore.objects.get(response=code, hashkey=key).delete()
        return True
    except CaptchaStore.DoesNotExist:
        return False
