from ninja import Router
from django_starter.contrib.auth.api import router as auth_router
from django_starter.contrib.captcha.api import router as captcha_router

router = Router()

router.add_router('auth', auth_router)
router.add_router('captcha', captcha_router)
