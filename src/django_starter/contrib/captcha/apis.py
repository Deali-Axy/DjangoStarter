from ninja import Router
from django_starter.contrib import captcha

router = Router(tags=['djs-captcha'])


@router.get('refresh')
def refresh_captcha(request):
    captcha_item = captcha.refresh()
    return {
        "key": captcha_item.key,
        "image_url": captcha_item.image_url,
        "audio_url": captcha_item.audio_url,
    }
