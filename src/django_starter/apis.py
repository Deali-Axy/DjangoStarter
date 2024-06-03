from ninja import Router
from django_starter.contrib.captcha.api import router as captcha_router

router = Router()

router.add_router('captcha', captcha_router)
