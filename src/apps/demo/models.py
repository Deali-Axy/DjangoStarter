from django.db import models


# Create your models here.
class DemoItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Demo Items'
        verbose_name = 'Demo Item'
        db_table = 'demo_items'
