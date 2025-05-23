from ninja import Router
from django_starter.contrib.captcha.apis import router as captcha_router
from django_starter.contrib.config.apis import router as config_router
from django_starter.contrib.monitoring.apis import router as monitoring_router

router = Router()

router.add_router('captcha', captcha_router)
router.add_router('config', config_router)
router.add_router('monitoring', monitoring_router)
