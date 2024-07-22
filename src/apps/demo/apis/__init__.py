from ninja import Router


from .movie.apis import router as movie_router

from .actor.apis import router as actor_router

from .music_album.apis import router as music_album_router

from .music.apis import router as music_router


router = Router(tags=['demo'])


router.add_router('movie', movie_router)

router.add_router('actor', actor_router)

router.add_router('music_album', music_album_router)

router.add_router('music', music_router)
