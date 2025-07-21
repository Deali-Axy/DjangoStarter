import logging
from .models import Movie

movies = [
    Movie(
        title="The Matrix",
        description="A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
        year=1999,
        rating=9,
        genre="Science Fiction",
        director="The Wachowskis",
        actors="Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss"
    ),
    Movie(
        title="Inception",
        description="A thief who steals corporate secrets through dream-sharing technology is given a task to plant an idea into the mind of a CEO.",
        year=2010,
        rating=9,
        genre="Science Fiction, Action",
        director="Christopher Nolan",
        actors="Leonardo DiCaprio, Joseph Gordon-Levitt, Ellen Page"
    ),
    Movie(
        title="Parasite",
        description="A poor family schemes to become employed by a wealthy family by infiltrating their household and posing as unrelated, highly qualified individuals.",
        year=2019,
        rating=9,
        genre="Thriller, Drama",
        director="Bong Joon Ho",
        actors="Song Kang-ho, Lee Sun-kyun, Cho Yeo-jeong"
    ),
    Movie(
        title="Spirited Away",
        description="During her family's move to the suburbs, a 10-year-old girl enters a world of spirits and must find her way back to the human world.",
        year=2001,
        rating=10,
        genre="Animation, Fantasy",
        director="Hayao Miyazaki",
        actors="Rumi Hiiragi, Miyu Irino, Mari Natsuki"
    ),
    Movie(
        title="The Godfather",
        description="The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
        year=1972,
        rating=10,
        genre="Crime, Drama",
        director="Francis Ford Coppola",
        actors="Marlon Brando, Al Pacino, James Caan"
    )
]

logger = logging.getLogger(__name__)


def seed_data_movies():
    logger.info('delete all movies')
    Movie.objects.all().delete()
    logger.info('insert all movies seed data')
    Movie.objects.bulk_create(movies)
