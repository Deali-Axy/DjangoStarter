from django.contrib.auth.models import User
from django.db import models
from django_starter.db.models import ModelExt


# Create your models here.
class OAuthClaim(ModelExt):
    user = models.ForeignKey(User, db_constraint=False, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.user}-{self.name}'

    class Meta:
        db_table = 'django_starter_oauth_claim'
        verbose_name = 'OAuth Claim'
        verbose_name_plural = verbose_name

