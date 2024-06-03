from ninja import Router
from .auth.apis import router as auth_router
from .oauth2 import router as oauth2_router

router = Router(tags=['account'])
router.add_router('auth', auth_router)
router.add_router('oauth2', oauth2_router)
