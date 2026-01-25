from ninja import Router

from .wallet.apis import router as wallet_router
from .topups.apis import router as topups_router
from .webhooks.apis import router as webhooks_router

router = Router(tags=['billing'])
router.add_router('wallet', wallet_router)
router.add_router('topups', topups_router)
router.add_router('webhooks', webhooks_router)
